"""
Abstract Wallet Monitor - Entry Point

Monitors ETH balances on Abstract L2 network and sends
Slack DM alerts when balances fall below threshold.
"""

import schedule
import time
import logging

from config import WALLETS, CHECK_INTERVAL_MINUTES, THRESHOLD_ETH
from monitor import fetch_all_balances
from alerter import (
    send_low_alert,
    send_recovery_alert,
    send_status_table,
    send_rpc_error_alert
)
from state import state_store


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-5s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
log = logging.getLogger(__name__)


def check_all_wallets() -> None:
    """
    Main monitoring cycle - runs every CHECK_INTERVAL_MINUTES.
    
    Fetches balances for all wallets, compares with previous state,
    and sends alerts on state changes.
    """
    log.info("Starting balance check cycle")
    
    statuses = fetch_all_balances(WALLETS)
    
    if not statuses:
        # All RPC calls failed
        fail_count = state_store.increment_rpc_fail()
        log.error(f"All balance checks failed. Consecutive failures: {fail_count}")
        
        if fail_count == 3:  # Alert after 15 minutes of failures
            send_rpc_error_alert()
        return
    
    # At least some wallets succeeded - reset fail counter
    state_store.reset_rpc_fail()
    
    # Process each wallet status
    for status in statuses:
        previous_state = state_store.get(status.address)
        
        if status.is_low and not previous_state.alerted_low:
            # Balance just dropped below threshold
            log.warning(f"{status.name}: {status.balance_eth:.5f} ETH 🔴 LOW - Sending alert")
            send_low_alert(status)
            state_store.set(status.address, alerted_low=True)
            
        elif not status.is_low and previous_state.alerted_low:
            # Balance just recovered above threshold
            log.info(f"{status.name}: {status.balance_eth:.5f} ETH ✅ RECOVERED - Sending alert")
            send_recovery_alert(status)
            state_store.set(status.address, alerted_low=False)
            
        else:
            # No state change
            icon = "🔴" if status.is_low else "✅"
            log.info(f"{status.name}: {status.balance_eth:.5f} ETH {icon}")
    
    log.info(f"Cycle complete. Next check in {CHECK_INTERVAL_MINUTES} min")


def main() -> None:
    """Application entry point."""
    log.info("=" * 50)
    log.info("Abstract Wallet Monitor starting...")
    log.info(f"Monitoring {len(WALLETS)} wallets")
    log.info(f"Threshold: {THRESHOLD_ETH} ETH")
    log.info(f"Check interval: {CHECK_INTERVAL_MINUTES} minutes")
    log.info("=" * 50)
    
    # Run initial check
    check_all_wallets()
    
    # Send startup status table
    statuses = fetch_all_balances(WALLETS)
    if statuses:
        send_status_table(statuses)
    
    # Schedule recurring checks
    schedule.every(CHECK_INTERVAL_MINUTES).minutes.do(check_all_wallets)
    
    log.info("Scheduler started. Press Ctrl+C to stop.")
    
    # Main loop
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
