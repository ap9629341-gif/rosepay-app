#!/bin/bash
# Script to start the frontend development server

echo "🚀 Starting RosePay Frontend..."
echo ""

# Check if we're in the right directory
if [ ! -d "frontend" ]; then
    echo "❌ Error: 'frontend' directory not found!"
    echo "   Make sure you're in the project root directory."
    exit 1
fi

# Navigate to frontend directory
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies first..."
    npm install
    echo ""
fi

# Start the development server
echo "✅ Starting Vite development server..."
echo "   Frontend will be available at: http://localhost:5173"
echo ""
npm run dev
