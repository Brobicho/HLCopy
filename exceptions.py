"""
Custom exceptions for HLCopy trading bot.

Defines specific exception types for better error handling and debugging.
"""


class HLCopyException(Exception):
    """Base exception for all HLCopy errors."""
    pass


class ConfigurationError(HLCopyException):
    """Raised when there's a configuration error."""
    pass


class TradingError(HLCopyException):
    """Raised when a trading operation fails."""
    pass


class PositionError(TradingError):
    """Raised when there's an issue with position management."""
    pass


class PriceError(TradingError):
    """Raised when price data is unavailable or invalid."""
    pass


class VaultError(HLCopyException):
    """Raised when there's an issue with vault operations."""
    pass


class ConnectionError(HLCopyException):
    """Raised when connection to Hyperliquid fails."""
    pass
