# 🚀 START HERE - Frontend Setup

## ⚠️ IMPORTANT: Use Relative Paths!

Your folder name has special characters, so **always use relative paths**.

## ✅ Correct Way (Copy These Commands)

```bash
# 1. Make sure you're in project root (should see main.py, models.py)
pwd

# 2. Go to frontend folder (RELATIVE PATH!)
cd frontend

# 3. Verify you're in the right place
pwd
# Should show: .../payment_app:  /frontend

ls
# Should see: package.json, src/, etc.

# 4. Install dependencies
npm install

# 5. Start server
npm run dev
```

## ❌ Wrong Way (Don't Do This!)

```bash
# DON'T use absolute paths!
cd /Users/adarshpal/payment_app/frontend  ❌

# DON'T run npm in root directory!
npm install  ❌ (when you're in root, not frontend folder)
```

## 🎯 Quick Start

If you're in the project root:

```bash
cd frontend && npm install && npm run dev
```

This does all three steps at once!
