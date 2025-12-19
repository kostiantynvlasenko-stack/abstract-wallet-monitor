"""
Balance monitoring module for Abstract network.

Handles RPC communication and balance fetching for configured wallets.
"""

import logging
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from web3 import Web3
from web3.exceptions import Web3Exception

from config import ABSTRACT_RPC_URL, THRESHOLD_WEI, WalletConfig


log = logging.getLogger(__name__)


@dataclass
class WalletStatus:
    """Current wallet state after balance check."""
    address: str
    name: str
    balance_eth: float
    balance_wei: int
    is_low: bool
    last_checked: datetime


def get_web3() -> Web3:
    """Create Web3 instance with Abstract RPC."""
    return Web3(Web3.HTTPProvider(
        ABSTRACT_RPC_URL,
        request_kwargs={'timeout': 10}
    ))


def get_balance(address: str) -> Optional[int]:
    """
    Get wallet balance in Wei from Abstract network.
    
    Args:
        address: Ethereum address (will be checksummed)
        
    Returns:
        Balance in Wei as integer, or None on failure
    """
    try:
        w3 = get_web3()
        checksum_address = w3.to_checksum_address(address)
        balance_wei = w3.eth.get_balance(checksum_address)
        return balance_wei
    except Web3Exception as e:
        log.error(f"Web3 error for {address}: {e}")
        return None
    except Exception as e:
        log.error(f"Unexpected error for {address}: {e}")
        return None


def fetch_all_balances(wallets: List[WalletConfig]) -> List[WalletStatus]:
    """
    Fetch balances for all configured wallets.
    
    Skips wallets that fail to fetch (logs error internally).
    
    Args:
        wallets: List of wallet configurations
        
    Returns:
        List of successful wallet statuses (may be shorter than input)
    """
    statuses: List[WalletStatus] = []
    
    for wallet in wallets:
        balance_wei = get_balance(wallet.address)
        
        if balance_wei is not None:
            balance_eth = balance_wei / 10**18
            is_low = balance_wei < THRESHOLD_WEI
            
            statuses.append(WalletStatus(
                address=wallet.address,
                name=wallet.name,
                balance_eth=balance_eth,
                balance_wei=balance_wei,
                is_low=is_low,
                last_checked=datetime.utcnow()
            ))
    
    return statuses
