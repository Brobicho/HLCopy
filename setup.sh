#!/usr/bin/env bash
# HLCopy Setup Script
# Automates the initial setup process

set -e  # Exit on error

echo "🚀 HLCopy Setup Script"
echo "======================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    echo "Please install Python 3.8+ and try again"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✅ Found Python $PYTHON_VERSION"
echo ""

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ Error: pip3 is not installed"
    echo "Please install pip3 and try again"
    exit 1
fi

echo "📦 Installing dependencies..."
pip3 install -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file with your actual credentials!"
    echo "   Required fields:"
    echo "   - HL_SECRET_KEY"
    echo "   - HL_ACCOUNT_ADDRESS"
    echo "   - MY_WALLET_ADDRESS"
    echo ""
else
    echo "ℹ️  .env file already exists, skipping..."
    echo ""
fi

# Create copy_vaults.txt if it doesn't exist
if [ ! -f copy_vaults.txt ]; then
    echo "📝 Creating copy_vaults.txt..."
    touch copy_vaults.txt
    echo "✅ copy_vaults.txt created"
    echo ""
    echo "⚠️  IMPORTANT: Add vault addresses to copy_vaults.txt (one per line)!"
    echo ""
else
    echo "ℹ️  copy_vaults.txt already exists, skipping..."
    echo ""
fi

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env with your credentials: nano .env"
echo "2. Add vault addresses: nano copy_vaults.txt"
echo "3. Run the bot: python3 open.py"
echo ""
echo "📚 For more information, see:"
echo "   - QUICKSTART.md for quick start guide"
echo "   - README.md for comprehensive documentation"
echo ""
