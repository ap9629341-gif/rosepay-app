# 📋 STEP 3B: Configure Vercel Deployment

## 🎯 What We're Doing
We're telling Vercel HOW to build and deploy your frontend. Think of it like giving instructions to a builder!

---

## ✅ Step-by-Step Configuration (With Explanations)

### **Step 1: Project Name**
**What you see:** A field that says "Project Name" with `rosepay-app` already filled

**What to do:** 
- ✅ **Leave it as is** (`rosepay-app` is perfect)

**Why:**
- This is just a name for your project on Vercel
- It doesn't affect your website URL
- You can change it later if needed

---

### **Step 2: Framework Preset**
**What you see:** "Framework Preset" showing "FastAPI"

**What to do:**
- ⚠️ **CHANGE THIS!** Click on it
- Select **"Vite"** from the dropdown
- (If you don't see Vite, select "Other" or "Create React App")

**Why:**
- Vercel detected FastAPI (your backend), but we're deploying FRONTEND
- Frontend uses Vite (the build tool for React)
- Vercel needs to know which build tool to use

**Learning:**
- Different tools build code differently
- Vite is specifically for React/Vue apps
- FastAPI is for Python backends (we'll deploy that separately)

---

### **Step 3: Root Directory (VERY IMPORTANT!)**
**What you see:** "Root Directory" showing `./` with an "Edit" button

**What to do:**
1. Click the **"Edit"** button next to Root Directory
2. Delete `./`
3. Type: `frontend`
4. Press Enter or click outside

**Why this is CRITICAL:**
- Your project structure looks like this:
  ```
  payment_app/
    ├── frontend/     ← Your React app is HERE
    ├── backend/     ← Your Python code is HERE
    └── main.py
  ```
- Vercel needs to know WHERE your frontend code is
- `./` means "root folder" (wrong - that has both frontend and backend)
- `frontend` means "the frontend folder" (correct!)

**Learning:**
- Root Directory = Starting point for building
- If wrong, Vercel will look in wrong place and fail
- This is like telling someone "the files are in the blue folder, not the red one"

---

### **Step 4: Build and Output Settings**
**What you see:** A section "> Build and Output Settings" (might be collapsed)

**What to do:**
1. Click to expand "Build and Output Settings"
2. Check these fields:

**Build Command:**
- Should say: `npm run build`
- ✅ **Leave it as is** (this builds your React app)

**Output Directory:**
- Should say: `dist`
- ✅ **Leave it as is** (this is where Vite puts built files)

**Install Command:**
- Should say: `npm install`
- ✅ **Leave it as is** (this installs dependencies)

**Why:**
- **Build Command**: Tells Vercel HOW to build your app
  - `npm run build` runs the build script in package.json
  - This converts React code → HTML/CSS/JS files
  
- **Output Directory**: Tells Vercel WHERE the built files are
  - Vite puts built files in `dist/` folder
  - Vercel needs to know where to find them
  
- **Install Command**: Tells Vercel HOW to install dependencies
  - `npm install` downloads all packages (React, Axios, etc.)
  - Must run before building

**Learning:**
- Building = Converting source code → production code
- Output = Final files that browsers can use
- Install = Getting all the libraries your app needs

---

### **Step 5: Environment Variables**
**What you see:** A section "> Environment Variables" (might be collapsed)

**What to do:**
1. Click to expand "Environment Variables"
2. Click **"Add"** button
3. Fill in:
   - **Key**: `VITE_API_URL`
   - **Value**: **Leave EMPTY for now** (we'll add it after backend is deployed)
4. Click **"Add"** to save

**Why:**
- **Environment Variables** = Settings that change between environments
- **VITE_API_URL** = Where your frontend will find the backend API
- **Now**: Empty (frontend will use localhost during build)
- **Later**: We'll set it to your Railway backend URL

**Learning:**
- Development: API at `http://localhost:8000`
- Production: API at `https://your-backend.railway.app`
- Environment variables let same code work in both places
- `VITE_` prefix tells Vite to make it available in your React code

**How it works:**
```javascript
// In your code (api.js):
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
// If VITE_API_URL is set, use it. Otherwise, use localhost.
```

---

### **Step 6: Deploy!**
**What you see:** A big black button at the bottom saying **"Deploy"**

**What to do:**
1. Double-check:
   - ✅ Framework: Vite (or Other)
   - ✅ Root Directory: `frontend`
   - ✅ Environment Variable: `VITE_API_URL` (empty value)
2. Click the **"Deploy"** button
3. Wait 2-3 minutes

**What happens:**
1. Vercel pulls code from GitHub
2. Runs `npm install` (installs packages)
3. Runs `npm run build` (builds your app)
4. Puts files in `dist/` folder online
5. Creates a URL for your website

**Why it takes time:**
- Installing packages: 30-60 seconds
- Building React app: 30-60 seconds
- Uploading files: 10-20 seconds
- Total: 2-3 minutes

---

## ✅ What You Should See After Deploying

1. **"Building..."** message
2. Progress logs (installing, building, etc.)
3. **"Congratulations!"** message
4. Your URL: `rosepay-app-xxxxx.vercel.app`

---

## 🎓 Summary of What We Did

1. **Set Framework** → Told Vercel to use Vite (React build tool)
2. **Set Root Directory** → Told Vercel where your frontend code is
3. **Set Build Settings** → Told Vercel how to build your app
4. **Set Environment Variable** → Prepared for backend connection
5. **Deployed** → Put your app online!

---

## 🆘 Troubleshooting

### **Problem: Build fails**
- Check Root Directory is `frontend` (not `./`)
- Check Framework is Vite (not FastAPI)
- Look at build logs for error messages

### **Problem: "Cannot find module"**
- Root Directory might be wrong
- Make sure it's `frontend` exactly

### **Problem: Website shows blank page**
- Check build logs
- Make sure build completed successfully
- Environment variable might be needed (we'll add it later)

---

## ✅ Ready?

**Follow the steps above!**

**Most Important:**
- ⚠️ **Root Directory MUST be `frontend`**
- ⚠️ **Framework should be Vite** (not FastAPI)

**When deployment finishes, tell me:**
- "Deployment done"
- Or give me your Vercel URL

**Then we'll move to Step 4: Deploy Backend!** 🚀
