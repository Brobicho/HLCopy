"""
Configuration management for HLCopy trading bot.

Handles loading and validating configuration from environment variables
and provides typed configuration objects.
"""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


@dataclass
class TradingConfig:
    """Trading-specific configuration."""
    
    wallet_address: str
    trade_amount_usd: float
    refresh_interval: int
    slippage_tolerance: float
    vaults_file: str
    
    def __post_init__(self):
        """Validate configuration values."""
        if self.trade_amount_usd <= 0:
            raise ValueError("Trade amount must be positive")
        
        if self.refresh_interval < 1:
            raise ValueError("Refresh interval must be at least 1 second")
        
        if not (0 < self.slippage_tolerance <= 1):
            raise ValueError("Slippage tolerance must be between 0 and 1")
        
        if not self.wallet_address.startswith("0x"):
            raise ValueError("Invalid wallet address format")


@dataclass
class HyperliquidConfig:
    """Hyperliquid API configuration."""
    
    secret_key: str
    account_address: str
    network: str = "mainnet"
    
    def __post_init__(self):
        """Validate configuration values."""
        if not self.secret_key.startswith("0x"):
            raise ValueError("Invalid secret key format")
        
        if self.account_address and not self.account_address.startswith("0x"):
            raise ValueError("Invalid account address format")
        
        if self.network not in ("mainnet", "testnet"):
            raise ValueError("Network must be 'mainnet' or 'testnet'")


class Config:
    """Main configuration manager."""
    
    def __init__(self, env_file: str = ".env"):
        """
        Initialize configuration from environment file.
        
        Args:
            env_file: Path to environment file
        """
        # Load environment variables
        if Path(env_file).exists():
            load_dotenv(env_file)
        else:
            raise FileNotFoundError(
                f"Environment file '{env_file}' not found. "
                "Please create one based on .env.example"
            )
        
        # Load configurations
        self.hyperliquid = self._load_hyperliquid_config()
        self.trading = self._load_trading_config()
    
    def _load_hyperliquid_config(self) -> HyperliquidConfig:
        """Load Hyperliquid API configuration."""
        secret_key = os.getenv("HL_SECRET_KEY")
        if not secret_key:
            raise ValueError(
                "HL_SECRET_KEY not found in environment. "
                "Please set it in your .env file"
            )
        
        account_address = os.getenv("HL_ACCOUNT_ADDRESS", "")
        network = os.getenv("HL_NETWORK", "mainnet")
        
        return HyperliquidConfig(
            secret_key=secret_key,
            account_address=account_address,
            network=network
        )
    
    def _load_trading_config(self) -> TradingConfig:
        """Load trading configuration."""
        wallet_address = os.getenv("MY_WALLET_ADDRESS")
        if not wallet_address:
            raise ValueError(
                "MY_WALLET_ADDRESS not found in environment. "
                "Please set it in your .env file"
            )
        
        trade_amount = float(os.getenv("TRADE_AMOUNT_USD", "15"))
        refresh_interval = int(os.getenv("REFRESH_INTERVAL_SECONDS", "3"))
        slippage = float(os.getenv("SLIPPAGE_TOLERANCE", "0.1"))
        vaults_file = os.getenv("VAULTS_FILE", "copy_vaults.txt")
        
        return TradingConfig(
            wallet_address=wallet_address,
            trade_amount_usd=trade_amount,
            refresh_interval=refresh_interval,
            slippage_tolerance=slippage,
            vaults_file=vaults_file
        )
