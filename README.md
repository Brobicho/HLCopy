<div align="center">

# HLCopy - Hyperliquid Copy Trading Bot

![Build](https://img.shields.io/badge/build-passing-brightgreen?style=for-the-badge) 
![Status](https://img.shields.io/badge/status-operational-brightgreen?style=for-the-badge)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

*Automated copy trading bot for Hyperliquid DEX - Monitor vault positions and replicate trades in real-time*

</div>

---

## 📋 About

HLCopy is a professional-grade automated copy trading bot for the Hyperliquid decentralized exchange. It monitors specified vault addresses and automatically replicates their trading positions to your account, enabling you to follow successful traders without manual intervention.

### ✨ Features

- 🔄 **Real-time Position Monitoring** - Continuously tracks vault positions with configurable refresh intervals
- 📊 **Automated Trade Replication** - Instantly copies new positions from monitored vaults
- 💰 **Flexible Position Sizing** - Configure USD amount per trade with automatic size calculation
- ⚙️ **Dynamic Leverage Management** - Automatically matches leverage settings from source positions
- 🎯 **Smart Position Closing** - Closes positions when they're exited by monitored vaults
- 🔒 **Secure Configuration** - Environment variable-based secrets management
- 🛡️ **Error Handling** - Robust error handling and recovery mechanisms
- 🔄 **Hot Reload** - Update vault list without restarting the bot
- 📝 **Comprehensive Logging** - Clear status updates with indicators

## ⚙️ Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Hyperliquid account with API access
- Private key for your trading wallet

### Quick Setup

```bash
# Clone the repository
git clone https://github.com/Brobicho/hlcopy.git
cd hlcopy

# Run automated setup script
./setup.sh

# Edit configuration files
nano .env              # Add your credentials
nano copy_vaults.txt   # Add vault addresses to copy
```

### Manual Setup

#### Step 1: Clone the Repository

```bash
git clone https://github.com/Brobicho/hlcopy.git
cd hlcopy
```

#### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

#### Step 3: Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your credentials
nano .env  # or use your preferred editor
```

#### Step 4: Set Up Vault List

Create or edit `copy_vaults.txt` with vault addresses to copy (one per line):

```
0x90f4174d630c02c425ba27986b76410e6ee37434
0xYourSecondVaultAddressHere
0xYourThirdVaultAddressHere
```

## 🚀 Usage

### Basic Usage

```bash
python open.py
```

### Running in Background

```bash
# Using nohup
nohup python open.py > bot.log 2>&1 &

# Using screen
screen -S hlcopy
python open.py
# Press Ctrl+A, then D to detach

# Using tmux
tmux new -s hlcopy
python open.py
# Press Ctrl+B, then D to detach
```

### Stopping the Bot

Press `Ctrl+C` to gracefully stop the bot.

## ⚙️ Configuration

### Environment Variables (.env)

| Variable | Description | Example | Required |
|----------|-------------|---------|----------|
| `HL_SECRET_KEY` | Your Hyperliquid private key | `0x123...` | ✅ |
| `HL_ACCOUNT_ADDRESS` | Your Hyperliquid account address | `0xabc...` | ✅ |
| `MY_WALLET_ADDRESS` | Wallet address to trade from | `0xdef...` | ✅ |
| `TRADE_AMOUNT_USD` | USD amount per trade | `15` | ✅ |
| `REFRESH_INTERVAL_SECONDS` | Check interval in seconds | `3` | ❌ |
| `HL_NETWORK` | Network (mainnet/testnet) | `mainnet` | ❌ |
| `SLIPPAGE_TOLERANCE` | Slippage tolerance (%) | `0.1` | ❌ |

### Vault Configuration (copy_vaults.txt)

Add vault addresses you want to copy, one per line:

```text
0x90f4174d630c02c425ba27986b76410e6ee37434
0x1234567890abcdef1234567890abcdef12345678
```

**Note:** You can edit this file while the bot is running - changes will be detected automatically.

## 📊 Understanding the Output

```
╒════════╤═══════════╤═════════╤═══════════════╤══════════╕
│ Coin   │ Size      │ PnL     │ Value (USD)   │ Leverage │
╞════════╪═══════════╪═════════╪═══════════════╪══════════╡
│ BTC    │ +0.0050   │ +2.45%  │ $215.30       │ 5x       │
│ ETH    │ -0.1200   │ -1.23%  │ $180.50       │ 3x       │
╘════════╧═══════════╧═════════╧═══════════════╧══════════╛

📋 Copying vaults:
   • 0x90f4174d630c02c425ba27986b76410e6ee37434
   • 0x1234567890abcdef1234567890abcdef12345678

⏳ Waiting for updates...
```

### Status Indicators

- 🚀 Bot started
- 📈 Opening position
- ✅ Order filled successfully
- 🔒 Closing position
- 🆕 New position detected
- ⚠️ Warning message
- ❌ Error occurred
- ⏳ Waiting for updates

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.