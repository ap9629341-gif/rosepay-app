#!/bin/bash

# Deployment Helper Script
# This script helps you prepare your code for deployment

echo "🚀 RosePay Deployment Helper"
echo "=============================="
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing Git repository..."
    git init
    echo "✅ Git initialized!"
else
    echo "✅ Git already initialized"
fi

# Check if .gitignore exists
if [ ! -f ".gitignore" ]; then
    echo "📝 Creating .gitignore..."
    cat > .gitignore << EOF
# Python
__pycache__/
*.py[cod]
*.db
*.sqlite
.env
venv/
env/

# Frontend
frontend/node_modules/
frontend/dist/
frontend/.vite/

# IDE
.vscode/
.idea/
EOF
    echo "✅ .gitignore created!"
else
    echo "✅ .gitignore exists"
fi

# Check git status
echo ""
echo "📊 Current Git Status:"
git status --short | head -10

echo ""
echo "📋 Next Steps:"
echo "1. Review changes: git status"
echo "2. Add all files: git add ."
echo "3. Commit: git commit -m 'Ready for deployment'"
echo "4. Create GitHub repo at: https://github.com/new"
echo "5. Push: git remote add origin https://github.com/YOUR_USERNAME/rosepay-app.git"
echo "6. Push: git push -u origin main"
echo ""
echo "Then follow: STEP_BY_STEP_DEPLOY.md"
