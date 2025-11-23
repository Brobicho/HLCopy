"""
Trading operations and position management for HLCopy bot.

Handles all trading logic including position opening, closing, and monitoring.
"""

from typing import Dict, List, Optional

from hyperliquid.exchange import Exchange
from hyperliquid.info import Info

from logger import logger


class PositionManager:
    """Manages position queries and operations."""
    
    def __init__(self, info: Info):
        """
        Initialize position manager.
        
        Args:
            info: Hyperliquid Info instance
        """
        self.info = info
    
    def get_positions(self, wallet: str) -> List[Dict]:
        """
        Get all positions for a wallet address.
        
        Args:
            wallet: Wallet address
            
        Returns:
            List of position dictionaries with type ('long'/'short') added
        """
        try:
            user_state = self.info.user_state(wallet)
            positions = []
            
            for asset_position in user_state["assetPositions"]:
                position = asset_position["position"]
                # Determine position type based on size
                position["type"] = "long" if float(position["szi"]) > 0 else "short"
                positions.append(position)
            
            return positions
            
        except Exception as e:
            logger.error(f"Failed to fetch positions for {wallet}", exc_info=e)
            return []
    
    def has_coin_position(self, positions: List[Dict], coin: str) -> bool:
        """
        Check if a coin exists in positions list.
        
        Args:
            positions: List of positions
            coin: Coin symbol
            
        Returns:
            True if coin is in positions
        """
        return any(pos["coin"] == coin for pos in positions)
    
    def get_position_by_coin(self, positions: List[Dict], coin: str) -> Optional[Dict]:
        """
        Get position for specific coin.
        
        Args:
            positions: List of positions
            coin: Coin symbol
            
        Returns:
            Position dict or None if not found
        """
        for pos in positions:
            if pos["coin"] == coin:
                return pos
        return None


class PriceCalculator:
    """Handles price queries and position size calculations."""
    
    def __init__(self, exchange: Exchange):
        """
        Initialize price calculator.
        
        Args:
            exchange: Hyperliquid Exchange instance
        """
        self.exchange = exchange
    
    def get_coin_price(self, coin: str) -> Optional[float]:
        """
        Get current market price for a coin.
        
        Args:
            coin: Coin symbol
            
        Returns:
            Current price or None if unavailable
        """
        try:
            mids = self.exchange.info.all_mids()
            if coin not in mids:
                logger.warning(f"Price not available for {coin}")
                return None
            return float(mids[coin])
        except Exception as e:
            logger.error(f"Failed to fetch price for {coin}", exc_info=e)
            return None
    
    def calculate_position_size(self, usd_amount: float, coin: str) -> Optional[float]:
        """
        Calculate position size based on USD amount.
        
        Args:
            usd_amount: Amount in USD
            coin: Coin symbol
            
        Returns:
            Position size in coin units or None if error
        """
        price = self.get_coin_price(coin)
        if price is None:
            return None
        
        # Determine decimal precision based on price
        if price >= 10000:
            decimals = 5
        elif price >= 1000:
            decimals = 2
        elif price >= 100:
            decimals = 1
        else:
            decimals = 0
        
        return round(usd_amount / price, decimals)


class TradeExecutor:
    """Executes trading operations."""
    
    def __init__(self, exchange: Exchange, slippage_tolerance: float = 0.1):
        """
        Initialize trade executor.
        
        Args:
            exchange: Hyperliquid Exchange instance
            slippage_tolerance: Slippage tolerance for trades
        """
        self.exchange = exchange
        self.slippage_tolerance = slippage_tolerance
    
    def open_position(
        self,
        coin: str,
        leverage: int,
        is_long: bool,
        size: float
    ) -> bool:
        """
        Open a new trading position.
        
        Args:
            coin: Coin symbol
            leverage: Leverage multiplier
            is_long: True for long, False for short
            size: Position size
            
        Returns:
            True if successful, False otherwise
        """
        try:
            position_type = "LONG" if is_long else "SHORT"
            logger.trade_open(
                f"Opening {position_type} on {coin} | Size: {size} | Leverage: {leverage}x"
            )
            
            # Place market order
            order_result = self.exchange.market_open(
                coin, is_long, size, None, self.slippage_tolerance
            )
            
            if order_result["status"] == "ok":
                success = False
                for status in order_result["response"]["data"]["statuses"]:
                    if "filled" in status:
                        filled = status["filled"]
                        logger.success(
                            f"Order #{filled['oid']} filled: "
                            f"{filled['totalSz']} @ ${filled['avgPx']}"
                        )
                        success = True
                    elif "error" in status:
                        logger.error(f"Order error: {status['error']}")
                        return False
                
                if not success:
                    return False
            else:
                logger.error(f"Failed to open position: {order_result}")
                return False
            
            # Update leverage
            try:
                self.exchange.update_leverage(leverage, coin)
                logger.settings(f"Leverage set to {leverage}x for {coin}")
            except Exception as e:
                logger.warning(f"Could not set leverage: {e}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to open position on {coin}", exc_info=e)
            return False
    
    def close_position(self, coin: str) -> bool:
        """
        Close a specific position.
        
        Args:
            coin: Coin symbol to close
            
        Returns:
            True if successful, False otherwise
        """
        try:
            result = self.exchange.market_close(coin)
            logger.trade_close(f"Closed position on {coin}")
            return True
        except Exception as e:
            logger.error(f"Failed to close position on {coin}", exc_info=e)
            return False
