# 🚀 Start Frontend Server - Quick Guide

## The Problem

**Error**: `ERR_CONNECTION_REFUSED` on `localhost:5173`

**Why**: The frontend development server is **not running**.

## ✅ Solution: Start the Frontend Server

### Step 1: Open Terminal

Open a terminal window.

### Step 2: Navigate to Frontend Folder

```bash
cd /Users/adarshpal/payment_app/frontend
```

### Step 3: Start the Server

```bash
npm run dev
```

**You should see:**
```
VITE v7.x.x  ready in xxx ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

### Step 4: Open Browser

Once you see the "Local: http://localhost:5173/" message, open your browser and go to:

**http://localhost:5173**

You should see the **Login page**! 🎉

---

## 🔧 If You Get Errors

### Error: "vite: command not found"

**Fix:**
```bash
cd /Users/adarshpal/payment_app/frontend
npm install
npm run dev
```

### Error: "Cannot find module"

**Fix:**
```bash
cd /Users/adarshpal/payment_app/frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Error: "Port 5173 already in use"

**Fix:**
```bash
# Kill the process using port 5173
lsof -ti:5173 | xargs kill -9

# Then start again
npm run dev
```

---

## ✅ Quick Start Command

If you're in the project root:

```bash
cd /Users/adarshpal/payment_app/frontend && npm run dev
```

---

## 📋 Remember

**You need TWO terminals running:**

1. **Terminal 1**: Backend (`python3 -m uvicorn main:app --reload`)
2. **Terminal 2**: Frontend (`npm run dev`)

Both must be running for the app to work!

---

## 🎯 After Starting

1. ✅ Frontend server shows: `Local: http://localhost:5173/`
2. ✅ Open browser to: `http://localhost:5173`
3. ✅ You should see the Login page!
