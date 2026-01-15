# 🔧 Troubleshooting Guide

## Common Errors and Fixes

### 1. **Package.json Syntax Error** ✅ FIXED
**Error**: `Unexpected token` or JSON parse error
**Fix**: Removed duplicate `devDependencies` section

### 2. **Frontend Dependencies Not Installed**

**Error**: `Cannot find module 'react'` or similar

**Fix**:
```bash
cd frontend
npm install
```

**What this does**: Installs all required packages (React, Axios, Tailwind, etc.)

---

### 3. **Backend Not Running**

**Error**: `Network Error` or `Failed to fetch` in browser console

**Fix**:
```bash
# In project root directory
python3 -m uvicorn main:app --reload
```

**Check**: Backend should be running on `http://127.0.0.1:8000`

---

### 4. **CORS Errors**

**Error**: `Access to XMLHttpRequest has been blocked by CORS policy`

**Status**: ✅ Already fixed in `main.py` - CORS middleware is added

**If still happening**, check `main.py` has:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

### 5. **Port Already in Use**

**Error**: `Port 5173 is already in use` or `Port 8000 is already in use`

**Fix**:
- **Frontend**: Kill the process using port 5173, or change port in `vite.config.js`
- **Backend**: Kill the process using port 8000, or change port: `uvicorn main:app --port 8001`

**Kill process on Mac/Linux**:
```bash
# Find process
lsof -ti:5173  # or 8000 for backend

# Kill it
kill -9 $(lsof -ti:5173)
```

---

### 6. **Module Not Found Errors**

**Error**: `Cannot find module '../config/api'` or similar

**Fix**: Check file structure matches:
```
frontend/src/
├── config/
│   └── api.js
├── services/
│   └── authService.js
└── ...
```

**Solution**: Make sure all files exist and paths are correct

---

### 7. **Tailwind CSS Not Working**

**Error**: Styles not applying, buttons look plain

**Fix**:
1. Check `tailwind.config.js` exists
2. Check `postcss.config.js` exists
3. Check `src/index.css` has:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

4. Restart dev server: `npm run dev`

---

### 8. **Authentication Token Issues**

**Error**: `401 Unauthorized` on every request

**Fix**:
1. Clear browser localStorage:
   - Open browser console (F12)
   - Run: `localStorage.clear()`
   - Refresh page

2. Login again to get new token

3. Check token format in browser console:
   ```javascript
   localStorage.getItem('token')
   ```
   Should return a JWT token string

---

### 9. **React Router Errors**

**Error**: `useNavigate() may be used only in the context of a Router component`

**Fix**: Make sure `App.jsx` wraps everything in `<BrowserRouter>`

**Check**: `main.jsx` should render `<App />` which has the router

---

### 10. **Import Errors**

**Error**: `Failed to resolve import` or `Module not found`

**Common causes**:
1. **Missing file**: Check file exists at the path
2. **Wrong path**: Check import path is correct
3. **Case sensitivity**: File names are case-sensitive on Linux/Mac

**Example fix**:
```javascript
// Wrong
import api from '../Config/api';  // Wrong case

// Correct
import api from '../config/api';  // Correct case
```

---

### 11. **Build Errors**

**Error**: `npm run build` fails

**Common fixes**:
1. Delete `node_modules` and reinstall:
   ```bash
   rm -rf node_modules package-lock.json
   npm install
   ```

2. Clear Vite cache:
   ```bash
   rm -rf node_modules/.vite
   ```

3. Check for syntax errors in all `.jsx` files

---

### 12. **API Endpoint Errors**

**Error**: `404 Not Found` when calling API

**Check**:
1. Backend is running
2. API URL is correct in `src/config/api.js`:
   ```javascript
   const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';
   ```
3. Endpoint exists in backend (check `api/v1/routes_*.py` files)

---

## Quick Diagnostic Steps

### Step 1: Check Backend
```bash
# Test backend health
curl http://127.0.0.1:8000/api/v1/health

# Should return: {"status": "healthy"}
```

### Step 2: Check Frontend
```bash
cd frontend
npm run dev
# Should start on http://localhost:5173
```

### Step 3: Check Browser Console
1. Open browser (F12)
2. Go to Console tab
3. Look for red errors
4. Check Network tab for failed requests

### Step 4: Check Files Exist
```bash
# Check key files exist
ls frontend/src/config/api.js
ls frontend/src/services/authService.js
ls frontend/tailwind.config.js
ls frontend/postcss.config.js
```

---

## Still Having Issues?

1. **Check error message carefully** - It usually tells you what's wrong
2. **Check browser console** - Most errors show there
3. **Check terminal output** - Both frontend and backend terminals
4. **Verify all files exist** - Use the file structure guide
5. **Restart everything**:
   - Stop both servers (Ctrl+C)
   - Clear browser cache
   - Restart backend
   - Restart frontend

---

## Getting Help

If you're still stuck, provide:
1. **Error message** (exact text)
2. **Where it happens** (browser console, terminal, etc.)
3. **What you were doing** (login, register, etc.)
4. **Browser and OS** (Chrome on Mac, etc.)
