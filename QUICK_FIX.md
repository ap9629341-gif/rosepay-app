# 🚨 Quick Fix Guide

## Most Common Errors - Quick Fixes

### ❌ Error 1: "Cannot find module" or "Module not found"

**Fix**:
```bash
cd frontend
npm install
```

**Why**: Dependencies aren't installed yet.

---

### ❌ Error 2: "Network Error" or "Failed to fetch"

**Fix**: Start the backend first!
```bash
# In project root (not frontend folder)
python3 -m uvicorn main:app --reload
```

**Why**: Frontend can't connect if backend isn't running.

---

### ❌ Error 3: "Port already in use"

**Fix**: Kill the process using the port
```bash
# For port 5173 (frontend)
lsof -ti:5173 | xargs kill -9

# For port 8000 (backend)
lsof -ti:8000 | xargs kill -9
```

**Why**: Another instance is already running.

---

### ❌ Error 4: "401 Unauthorized"

**Fix**: Clear browser storage and login again
1. Open browser console (F12)
2. Run: `localStorage.clear()`
3. Refresh page
4. Login again

**Why**: Token expired or invalid.

---

### ❌ Error 5: "CORS policy" error

**Status**: ✅ Already fixed! CORS is configured in `main.py`

**If still happening**: Make sure backend is running and `main.py` has CORS middleware.

---

## Step-by-Step Setup (Do This First!)

### 1. Install Frontend Dependencies
```bash
cd frontend
npm install
```

**Wait for it to finish** - should see "added X packages"

### 2. Start Backend (Terminal 1)
```bash
# Go back to project root
cd ..
python3 -m uvicorn main:app --reload
```

**You should see**: `✅ RosePay API is ready!`

### 3. Start Frontend (Terminal 2)
```bash
cd frontend
npm run dev
```

**You should see**: `Local: http://localhost:5173`

### 4. Open Browser
Go to: `http://localhost:5173`

---

## Still Not Working?

### Check These:

1. **Backend running?**
   - Test: `curl http://127.0.0.1:8000/api/v1/health`
   - Should return: `{"status":"healthy"}`

2. **Frontend running?**
   - Check: `http://localhost:5173` opens in browser
   - Should show login page

3. **Browser console errors?**
   - Press F12 → Console tab
   - Look for red errors
   - Copy the error message

4. **All files exist?**
   ```bash
   ls frontend/src/config/api.js
   ls frontend/src/services/authService.js
   ls frontend/tailwind.config.js
   ```

---

## Tell Me The Exact Error

Please share:
1. **Error message** (copy/paste the exact text)
2. **Where it appears** (browser console, terminal, etc.)
3. **What you were doing** (trying to login, starting server, etc.)

Then I can give you the exact fix! 🎯
