"""
Configuration module for Abstract Wallet Monitor.

Contains wallet registry, thresholds, and network constants.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class WalletConfig:
    """Static wallet configuration."""
    name: str
    address: str


# === WALLETS TO MONITOR ===
WALLETS: List[WalletConfig] = [
    WalletConfig(
        name="Settler Wallet",
        address="0xA3f8c5E0037f9f70b38d5140542432f40BcE71CB"
    ),
    WalletConfig(
        name="Organizer Admin Wallet #1",
        address="0xcd835fa14e546f55b0e4b4fcfccce6dc756ae3d5"
    ),
    WalletConfig(
        name="Organizer Admin Wallet #2",
        address="0x08c83c4bf828c846f062d8bc6ddb02101e67e81c"
    ),
    WalletConfig(
        name="Organizer Admin Wallet #3",
        address="0x519e8a7c7c195d98068bbd849169c476892b662d"
    ),
    WalletConfig(
        name="Organizer Admin Wallet #4",
        address="0xcff06e5c3838c8fabf5b53f8a69ef943f94e07f3"
    ),
    WalletConfig(
        name="Organizer Admin Wallet #5",
        address="0x662dd356442943a34a83ad0f18067875dfc72474"
    ),
]

# === THRESHOLD ===
THRESHOLD_ETH: float = 0.0015
THRESHOLD_WEI: int = 1_500_000_000_000_000  # 0.0015 * 10^18

# === SCHEDULER ===
CHECK_INTERVAL_MINUTES: int = 5

# === ABSTRACT NETWORK ===
ABSTRACT_RPC_URL: str = "https://api.mainnet.abs.xyz"
ABSTRACT_CHAIN_ID: int = 2741

# === SLACK ===
SLACK_USER_ID: str = "U08KVLZQVUN"  # Kostya Vlasenko - DM recipient
# SLACK_BOT_TOKEN loaded from environment variable in alerter.py
