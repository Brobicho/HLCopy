"""
Logging utilities for HLCopy trading bot.

Provides consistent logging with emoji indicators and color support.
"""

import sys
from datetime import datetime
from enum import Enum
from typing import Optional


class LogLevel(Enum):
    """Log level enumeration."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class Logger:
    """Custom logger with emoji support."""
    
    # Emoji mappings for different log types
    EMOJIS = {
        LogLevel.DEBUG: "🔍",
        LogLevel.INFO: "ℹ️",
        LogLevel.SUCCESS: "✅",
        LogLevel.WARNING: "⚠️",
        LogLevel.ERROR: "❌",
        LogLevel.CRITICAL: "🚨"
    }
    
    def __init__(self, name: str = "HLCopy", use_emojis: bool = True):
        """
        Initialize logger.
        
        Args:
            name: Logger name
            use_emojis: Whether to use emoji indicators
        """
        self.name = name
        self.use_emojis = use_emojis
    
    def _log(self, level: LogLevel, message: str, emoji_override: Optional[str] = None):
        """
        Internal logging method.
        
        Args:
            level: Log level
            message: Log message
            emoji_override: Optional emoji to use instead of default
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        emoji = emoji_override if emoji_override else self.EMOJIS.get(level, "")
        
        if self.use_emojis and emoji:
            log_msg = f"{emoji}  {message}"
        else:
            log_msg = f"[{level.value}] {message}"
        
        # Write to appropriate stream
        stream = sys.stderr if level in (LogLevel.ERROR, LogLevel.CRITICAL) else sys.stdout
        print(log_msg, file=stream)
    
    def debug(self, message: str):
        """Log debug message."""
        self._log(LogLevel.DEBUG, message)
    
    def info(self, message: str, emoji: Optional[str] = None):
        """Log info message."""
        self._log(LogLevel.INFO, message, emoji)
    
    def success(self, message: str, emoji: Optional[str] = None):
        """Log success message."""
        self._log(LogLevel.SUCCESS, message, emoji)
    
    def warning(self, message: str):
        """Log warning message."""
        self._log(LogLevel.WARNING, message)
    
    def error(self, message: str, exc_info: Optional[Exception] = None):
        """
        Log error message.
        
        Args:
            message: Error message
            exc_info: Optional exception for additional context
        """
        if exc_info:
            message = f"{message}: {exc_info}"
        self._log(LogLevel.ERROR, message)
    
    def critical(self, message: str, exc_info: Optional[Exception] = None):
        """
        Log critical message.
        
        Args:
            message: Critical message
            exc_info: Optional exception for additional context
        """
        if exc_info:
            message = f"{message}: {exc_info}"
        self._log(LogLevel.CRITICAL, message)
    
    # Specialized logging methods with custom emojis
    
    def startup(self, message: str):
        """Log startup message."""
        self.info(message, emoji="🚀")
    
    def trade_open(self, message: str):
        """Log trade opening."""
        self.info(message, emoji="📈")
    
    def trade_close(self, message: str):
        """Log trade closing."""
        self.info(message, emoji="🔒")
    
    def new_position(self, message: str):
        """Log new position detection."""
        self.info(message, emoji="🆕")
    
    def waiting(self, message: str):
        """Log waiting status."""
        self.info(message, emoji="⏳")
    
    def update(self, message: str):
        """Log update."""
        self.info(message, emoji="🔄")
    
    def money(self, message: str):
        """Log money-related info."""
        self.info(message, emoji="💰")
    
    def wallet(self, message: str):
        """Log wallet-related info."""
        self.info(message, emoji="💼")
    
    def chart(self, message: str):
        """Log chart/stats info."""
        self.info(message, emoji="📊")
    
    def settings(self, message: str):
        """Log settings info."""
        self.info(message, emoji="⚙️")
    
    @staticmethod
    def clear_screen():
        """Clear the terminal screen."""
        print("\033c", end="")
    
    @staticmethod
    def separator(char: str = "=", length: int = 50):
        """Print a separator line."""
        print(char * length)
    
    def section_header(self, title: str):
        """
        Print a formatted section header.
        
        Args:
            title: Section title
        """
        self.separator()
        print(f"  {title.upper()}")
        self.separator()


# Global logger instance
logger = Logger()
