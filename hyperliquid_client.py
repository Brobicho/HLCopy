"""
Hyperliquid API Setup Utilities

This module provides utility functions for setting up and configuring
connections to the Hyperliquid exchange API using environment variables.
"""

import os
from typing import Optional, Tuple

import eth_account
from dotenv import load_dotenv
from eth_account.signers.local import LocalAccount
from hyperliquid.exchange import Exchange
from hyperliquid.info import Info
from hyperliquid.utils import constants


# Load environment variables from .env file
load_dotenv()


def get_base_url(network: str = "mainnet") -> str:
    """
    Get the Hyperliquid API base URL based on network.
    
    Args:
        network: Network to connect to ('mainnet' or 'testnet')
        
    Returns:
        Base URL for the specified network
    """
    if network.lower() == "testnet":
        return constants.TESTNET_API_URL
    return constants.MAINNET_API_URL


def setup(
    base_url: Optional[str] = None,
    skip_ws: bool = False,
    account_address: Optional[str] = None
) -> Tuple[str, Info, Exchange]:
    """
    Set up Hyperliquid exchange connection using environment variables.
    
    Args:
        base_url: Optional API base URL. If None, uses HL_NETWORK from env
        skip_ws: Whether to skip WebSocket connection
        account_address: Optional account address override
        
    Returns:
        Tuple of (address, Info instance, Exchange instance)
        
    Raises:
        ValueError: If required environment variables are missing
        Exception: If account has no equity
    """
    # Get configuration from environment variables
    secret_key = os.getenv("HL_SECRET_KEY")
    if not secret_key:
        raise ValueError(
            "HL_SECRET_KEY not found in environment variables. "
            "Please create a .env file based on .env.example"
        )
    
    address = os.getenv("HL_ACCOUNT_ADDRESS", "")
    
    # Create account from private key
    account: LocalAccount = eth_account.Account.from_key(secret_key)
    
    # Use account address if not provided in env
    if not address:
        address = account.address
    
    # Override with provided account address if given
    if account_address is not None:
        address = account_address
    
    # Determine base URL
    if base_url is None:
        network = os.getenv("HL_NETWORK", "mainnet")
        base_url = get_base_url(network)
    
    # Initialize API clients
    info = Info(base_url, skip_ws)
    
    # Verify account has equity
    user_state = info.user_state(address)
    spot_user_state = info.spot_user_state(address)
    margin_summary = user_state["marginSummary"]
    
    if float(margin_summary["accountValue"]) == 0 and len(spot_user_state["balances"]) == 0:
        url = info.base_url.split(".", 1)[1]
        error_string = (
            f"Account {address} has no equity on {url}.\n"
            "If this address is your API wallet, update HL_ACCOUNT_ADDRESS "
            "to specify your actual account address."
        )
        raise Exception(error_string)
    
    exchange = Exchange(account, base_url, account_address=address)
    return address, info, exchange