# HLCopy Quick Start Guide

## Initial Setup (5 minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
# Copy example environment file
cp .env.example .env

# Edit with your credentials
nano .env  # or vim, code, etc.
```

**Required values in .env:**
- `HL_SECRET_KEY` - Your private key
- `HL_ACCOUNT_ADDRESS` - Your account address
- `MY_WALLET_ADDRESS` - Wallet to trade from
- `TRADE_AMOUNT_USD` - Amount per trade (start with 15)

### 3. Set Up Vaults to Copy
```bash
# Add vault addresses (one per line)
echo "0x90f4174d630c02c425ba27986b76410e6ee37434" > copy_vaults.txt
```

### 4. Run the Bot
```bash
python open.py
```

## Common Commands

### Run in Background
```bash
# Using screen (recommended)
screen -S hlcopy
python open.py
# Press Ctrl+A then D to detach
# screen -r hlcopy  # to reattach

# Using nohup
nohup python open.py > bot.log 2>&1 &

# Check logs
tail -f bot.log
```

### Stop the Bot
```bash
# If running in foreground
Ctrl+C

# If running in background
killall python  # or find specific PID
```

### Update Vault List (Hot Reload)
```bash
# Just edit the file - bot will detect changes automatically
nano copy_vaults.txt
```

## Troubleshooting

### "HL_SECRET_KEY not found"
- Make sure you created `.env` file (not just `.env.example`)
- Check that `.env` has the required variables

### "Import Error: tabulate"
```bash
pip install -r requirements.txt
```

### "No equity" Error
- Ensure your account has funds
- Verify `HL_ACCOUNT_ADDRESS` is correct
- Check you're on the right network (mainnet/testnet)

### Position Not Opening
- Check slippage tolerance (increase if needed)
- Verify you have sufficient margin
- Check bot logs for specific error messages
