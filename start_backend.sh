#!/bin/bash
# Start the backend server

echo "🚀 Starting RosePay Backend..."
echo ""

cd /Users/adarshpal/payment_app

echo "📍 Location: $(pwd)"
echo ""

# Check if Python dependencies are installed
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo "📦 Installing Python dependencies..."
    pip3 install -r requirements.txt
    echo ""
fi

echo "✅ Starting FastAPI server..."
echo "   Backend will be available at: http://127.0.0.1:8000"
echo "   API docs at: http://127.0.0.1:8000/docs"
echo ""

python3 -m uvicorn main:app --reload
