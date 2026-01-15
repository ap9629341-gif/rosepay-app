# 🚀 How to Start the Application

## The Error You're Seeing

**Error**: `ERR_CONNECTION_REFUSED` on `localhost:5173`

**What it means**: The frontend development server is **not running**.

**Solution**: Start the frontend server! ✅

---

## Step-by-Step: Start Everything

### **Step 1: Start Backend (Terminal 1)**

Open a terminal and run:

```bash
# Make sure you're in the project root directory
cd /Users/adarshpal/payment_app

# Start the backend
python3 -m uvicorn main:app --reload
```

**You should see**:
```
✅ Database initialized!
✅ RosePay API is ready!
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**Keep this terminal open!** ⬆️

---

### **Step 2: Start Frontend (Terminal 2)**

Open a **NEW terminal window** and run:

```bash
# Navigate to frontend directory
cd /Users/adarshpal/payment_app/frontend

# Install dependencies (only needed first time)
npm install

# Start the frontend server
npm run dev
```

**You should see**:
```
  VITE v7.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

**Keep this terminal open too!** ⬆️

---

### **Step 3: Open Browser**

Once both servers are running:

1. Open Chrome (or any browser)
2. Go to: `http://localhost:5173`
3. You should see the **Login page**! 🎉

---

## Quick Commands Reference

### Start Backend:
```bash
cd /Users/adarshpal/payment_app
python3 -m uvicorn main:app --reload
```

### Start Frontend:
```bash
cd /Users/adarshpal/payment_app/frontend
npm install  # Only first time
npm run dev
```

---

## Troubleshooting

### ❌ "npm: command not found"
**Fix**: Install Node.js from https://nodejs.org

### ❌ "Port 5173 already in use"
**Fix**: Kill the process:
```bash
lsof -ti:5173 | xargs kill -9
```

### ❌ "Port 8000 already in use"
**Fix**: Kill the process:
```bash
lsof -ti:8000 | xargs kill -9
```

### ❌ "Cannot find module"
**Fix**: Install dependencies:
```bash
cd frontend
npm install
```

---

## What Should Happen

1. ✅ Backend running on `http://127.0.0.1:8000`
2. ✅ Frontend running on `http://localhost:5173`
3. ✅ Browser shows login page (not error page)

---

## Still Having Issues?

Make sure:
- ✅ Both terminals are open and running
- ✅ No error messages in either terminal
- ✅ You're using the correct URLs
- ✅ Node.js is installed (`node --version`)

Then try again! 🚀
