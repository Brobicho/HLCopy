"""
Hyperliquid Copy Trading Bot

A professional copy trading bot that monitors specified vault addresses
and automatically replicates their trading positions on Hyperliquid exchange.
"""

import sys
import time
from pathlib import Path
from typing import Dict, List

from tabulate import tabulate

import hyperliquid_client
from config import Config
from logger import logger
from trading import PositionManager, PriceCalculator, TradeExecutor


class CopyTradingBot:
    """Main copy trading bot class for managing position replication."""
    
    def __init__(self, config: Config):
        """
        Initialize the copy trading bot.
        
        Args:
            config: Configuration object
        """
        self.config = config
        
        # Initialize Hyperliquid connection
        self.address, self.info, self.exchange = hyperliquid_client.setup(skip_ws=True)
        
        # Initialize trading components
        self.position_manager = PositionManager(self.info)
        self.price_calculator = PriceCalculator(self.exchange)
        self.trade_executor = TradeExecutor(
            self.exchange,
            config.trading.slippage_tolerance
        )
        
        # State management
        self.my_positions: List[Dict] = []
        self.copy_vaults: List[str] = []
        self.old_vaults: List[str] = []
        self.all_copy_positions: List[Dict] = []
        

    
    def print_positions_table(self):
        """Print formatted table of current positions."""
        if not self.my_positions:
            logger.chart("No open positions")
            return
        
        table_data = []
        for pos in self.my_positions:
            coin = pos["coin"]
            size = float(pos["szi"])
            pnl_pct = (
                float(pos["unrealizedPnl"]) / float(pos["positionValue"]) * 100
            )
            value = float(pos["positionValue"])
            leverage = pos["leverage"]["value"]
            
            table_data.append([
                coin,
                f"{size:+.4f}",
                f"{pnl_pct:+.2f}%",
                f"${value:,.2f}",
                f"{leverage}x"
            ])
        
        headers = ["Coin", "Size", "PnL", "Value (USD)", "Leverage"]
        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
        
        print("\n📋 Copying vaults:")
        for vault in self.copy_vaults:
            print(f"   • {vault}")
        print()
    
    def load_copy_vaults(self) -> List[str]:
        """
        Load vault addresses from file.
        
        Returns:
            List of vault addresses
        """
        vaults_file = self.config.trading.vaults_file
        try:
            with open(vaults_file, 'r') as f:
                vaults = [line.strip() for line in f if line.strip()]
            return vaults
        except FileNotFoundError:
            logger.warning(f"{vaults_file} not found. Creating empty file.")
            Path(vaults_file).touch()
            return []
        except Exception as e:
            logger.error(f"Failed to load vaults file", exc_info=e)
            return []
    
    def run(self):
        """Main bot loop - monitor and copy positions."""
        logger.startup("Starting Hyperliquid Copy Trading Bot")
        logger.wallet(f"Trading wallet: {self.config.trading.wallet_address}")
        logger.money(f"Trade amount: ${self.config.trading.trade_amount_usd}")
        logger.update(f"Refresh interval: {self.config.trading.refresh_interval}s\n")
        
        # Initial load
        self.copy_vaults = self.load_copy_vaults()
        self.old_vaults = self.copy_vaults[:]
        self.my_positions = self.position_manager.get_positions(
            self.config.trading.wallet_address
        )
        
        self.print_positions_table()
        
        try:
            while True:
                # Reload vaults list (allows runtime updates)
                self.copy_vaults = self.load_copy_vaults()
                
                if self.copy_vaults != self.old_vaults:
                    logger.update("Copy vaults list updated")
                    self.all_copy_positions = []
                    self.old_vaults = self.copy_vaults[:]
                
                # Aggregate positions from all vaults
                self.all_copy_positions = []
                for vault in self.copy_vaults:
                    vault_positions = self.position_manager.get_positions(vault)
                    for position in vault_positions:
                        # Add if not already tracked
                        if not self.position_manager.has_coin_position(
                            self.all_copy_positions, position['coin']
                        ):
                            self.all_copy_positions.append(position)
                    
                    # Check for new positions to open
                    for position in vault_positions:
                        if not self.position_manager.has_coin_position(
                            self.my_positions, position['coin']
                        ):
                            logger.separator()
                            logger.new_position("NEW POSITION DETECTED")
                            logger.separator()
                            print(f"   Coin: {position['coin']}")
                            print(f"   Type: {position['type'].upper()}")
                            print(f"   Size: {position['szi']}")
                            logger.separator()
                            print()
                            
                            # Determine leverage
                            if (
                                'leverage' in position and
                                position['leverage'].get('type') == 'cross'
                            ):
                                leverage = int(position['leverage']['value'])
                            else:
                                logger.info("Leverage not found, defaulting to 1x")
                                leverage = 1
                            
                            # Calculate and open position
                            size = self.price_calculator.calculate_position_size(
                                self.config.trading.trade_amount_usd,
                                position['coin']
                            )
                            
                            if size:
                                self.trade_executor.open_position(
                                    position['coin'],
                                    leverage,
                                    position['type'] == 'long',
                                    size
                                )
                                time.sleep(1)
                
                # Close positions that are no longer in any vault
                for my_position in self.my_positions[:]:
                    if not self.position_manager.has_coin_position(
                        self.all_copy_positions, my_position['coin']
                    ):
                        logger.trade_close(f"Closing position on {my_position['coin']}")
                        self.trade_executor.close_position(my_position['coin'])
                
                # Refresh positions and display
                self.my_positions = self.position_manager.get_positions(
                    self.config.trading.wallet_address
                )
                logger.clear_screen()
                self.print_positions_table()
                logger.waiting("Waiting for updates...")
                
                time.sleep(self.config.trading.refresh_interval)
                
        except KeyboardInterrupt:
            logger.info("\n\nBot stopped by user", emoji="🛑")
            sys.exit(0)
        except Exception as e:
            logger.critical("\n\nFatal error occurred", exc_info=e)
            sys.exit(1)


def main():
    """Main entry point."""
    try:
        # Load configuration
        config = Config()
        
        # Create and run bot
        bot = CopyTradingBot(config)
        bot.run()
        
    except FileNotFoundError as e:
        logger.error(str(e))
        sys.exit(1)
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.critical("Failed to start bot", exc_info=e)
        sys.exit(1)


if __name__ == "__main__":
    main()

