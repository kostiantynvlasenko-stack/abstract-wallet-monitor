"""
Slack notification module for wallet alerts.

Handles all Slack DM communications including low balance alerts,
recovery notifications, and status tables.
"""

import os
import logging
from typing import List

import requests

from config import SLACK_USER_ID, THRESHOLD_ETH, CHECK_INTERVAL_MINUTES
from monitor import WalletStatus


log = logging.getLogger(__name__)

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")


def send_slack_dm(message: str) -> bool:
    """
    Send direct message to configured Slack user.
    
    Args:
        message: Formatted message text (supports Slack mrkdwn)
        
    Returns:
        True if sent successfully, False otherwise
    """
    if not SLACK_BOT_TOKEN:
        log.error("SLACK_BOT_TOKEN not configured!")
        return False
    
    url = "https://slack.com/api/chat.postMessage"
    
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "channel": SLACK_USER_ID,
        "text": message,
        "unfurl_links": False,
        "unfurl_media": False
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        data = response.json()
        
        if data.get("ok"):
            log.info("Slack message sent successfully")
            return True
        else:
            log.error(f"Slack API error: {data.get('error')}")
            return False
            
    except requests.RequestException as e:
        log.error(f"Slack request failed: {e}")
        return False


def send_low_alert(status: WalletStatus) -> bool:
    """Send low balance alert for a wallet."""
    message = f"""🔴 *НИЗЬКИЙ БАЛАНС*

*Гаманець:* {status.name}
*Адреса:* `{status.address}`
*Баланс:* {status.balance_eth:.5f} ETH
*Поріг:* {THRESHOLD_ETH} ETH

⚠️ Потрібне поповнення!"""
    
    return send_slack_dm(message)


def send_recovery_alert(status: WalletStatus) -> bool:
    """Send balance recovered alert for a wallet."""
    message = f"""✅ *БАЛАНС ВІДНОВЛЕНО*

*Гаманець:* {status.name}
*Адреса:* `{status.address}`
*Баланс:* {status.balance_eth:.5f} ETH

Гаманець знову в нормі."""
    
    return send_slack_dm(message)


def send_status_table(statuses: List[WalletStatus]) -> bool:
    """Send current status table for all wallets."""
    lines = ["📊 *СТАТУС ГАМАНЦІВ* (Abstract)\n", "```"]
    lines.append("| Гаманець                    | Баланс (ETH) | Статус |")
    lines.append("|-----------------------------|--------------|--------|")
    
    for s in statuses:
        status_icon = "🔴" if s.is_low else "✅"
        name_padded = s.name[:27].ljust(27)
        balance_str = f"{s.balance_eth:.5f}".rjust(12)
        lines.append(f"| {name_padded} | {balance_str} | {status_icon}     |")
    
    lines.append("```")
    lines.append(f"\nПоріг: {THRESHOLD_ETH} ETH")
    lines.append(f"Наступна перевірка: через {CHECK_INTERVAL_MINUTES} хв")
    
    return send_slack_dm("\n".join(lines))


def send_rpc_error_alert() -> bool:
    """Send RPC connectivity error alert after prolonged failures."""
    message = """⚠️ *ПОМИЛКА МОНІТОРИНГУ*

Не вдалося підключитися до Abstract RPC протягом 15 хвилин.
Моніторинг тимчасово не працює.

Перевірте статус мережі або RPC endpoint."""
    
    return send_slack_dm(message)
