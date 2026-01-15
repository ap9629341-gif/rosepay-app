#!/bin/bash
# Start the frontend server

echo "🚀 Starting RosePay Frontend..."
echo ""

cd /Users/adarshpal/payment_app/frontend

echo "📍 Location: $(pwd)"
echo ""

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
    echo ""
fi

echo "✅ Starting Vite development server..."
echo "   Frontend will be available at: http://localhost:5173"
echo ""

npm run dev
