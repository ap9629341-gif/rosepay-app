#!/bin/bash
# Script to rename the project folder to fix the colon/spaces issue

echo "🔧 Fixing folder name issue..."
echo ""

# Check if we can rename
if [ -d "/Users/adarshpal/payment_app:  " ]; then
    echo "Found folder: payment_app:  "
    echo ""
    echo "⚠️  WARNING: This will rename your project folder!"
    echo "   From: payment_app:  "
    echo "   To:   payment_app"
    echo ""
    read -p "Continue? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cd /Users/adarshpal
        mv "payment_app:  " payment_app
        echo "✅ Folder renamed successfully!"
        echo ""
        echo "Now run:"
        echo "  cd payment_app/frontend"
        echo "  npm run dev"
    else
        echo "Cancelled."
    fi
else
    echo "Folder not found or already renamed."
fi
