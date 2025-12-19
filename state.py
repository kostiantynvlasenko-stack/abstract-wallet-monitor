"""
In-memory state store for alert tracking.

Tracks which wallets have been alerted to avoid duplicate notifications.
State resets on application restart - this is acceptable because worst
case is one duplicate alert on restart.
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class AlertState:
    """Tracks whether alerts have been sent for a wallet."""
    address: str
    alerted_low: bool = False


class StateStore:
    """
    In-memory state store for alert tracking.
    
    Manages:
    - Per-wallet alert state (has low balance alert been sent?)
    - RPC failure counter (for detecting prolonged outages)
    """
    
    def __init__(self):
        self._states: Dict[str, AlertState] = {}
        self._rpc_fail_count: int = 0
    
    def get(self, address: str) -> AlertState:
        """
        Get alert state for address.
        
        Creates default state (alerted_low=False) if not exists.
        """
        if address not in self._states:
            self._states[address] = AlertState(address=address)
        return self._states[address]
    
    def set(self, address: str, alerted_low: bool) -> None:
        """Update alert state for address."""
        self._states[address] = AlertState(
            address=address,
            alerted_low=alerted_low
        )
    
    def increment_rpc_fail(self) -> int:
        """
        Increment RPC failure counter.
        
        Returns new count for threshold checking.
        """
        self._rpc_fail_count += 1
        return self._rpc_fail_count
    
    def reset_rpc_fail(self) -> None:
        """Reset RPC failure counter on successful cycle."""
        self._rpc_fail_count = 0
    
    def get_rpc_fail_count(self) -> int:
        """Get current RPC failure count."""
        return self._rpc_fail_count


# Global singleton instance
state_store = StateStore()
