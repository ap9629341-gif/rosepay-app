# 📋 Complete Render Configuration

## 🎯 What We're Doing
We're finishing the setup of your backend on Render. You've already created the PostgreSQL database - great! Now we need to configure the web service.

---

## ✅ Step-by-Step (On This Page)

### **Step 1: Check Service Details (Top Section)**
Look at the top of the page. You should see:
- **Name**: Should say something like "rosepay-backend" or "web-service"
- **Region**: Should be selected (e.g., "Oregon (US West)")
- **Branch**: Should be `main`

**If these aren't set:**
- Scroll up to find these fields
- Set them if needed

---

### **Step 2: Instance Type (Skip This)**
You'll see "Pro Max" and "Pro Ultra" options.

**What to do:**
- ✅ **IGNORE these** - They're paid plans
- ✅ **Scroll down** - We want the FREE tier (it's below or in a different section)

**Why:**
- Free tier is usually selected by default
- Or it's in a different section (like "Free" or "Starter")
- Pro plans cost money - we don't need them!

---

### **Step 3: Environment Variables (You're Here!)**
You're in the right section! I can see you have:
- `DATABASE_URL` field (good!)
- `NAME_OF_VARIABLE` field (we need to change this)

**What to do:**

#### **Variable 1: DATABASE_URL**
1. In the **DATABASE_URL** row:
   - **Left field** (Key): Should already say `DATABASE_URL` ✅
   - **Right field** (Value): 
     - If you already pasted your PostgreSQL URL, great! ✅
     - If it says "value", click in that field
     - Paste your PostgreSQL database URL (the one you copied from the database you created)
     - It should look like: `postgresql://...`

**Why:**
- This tells your backend WHERE the database is
- Without this, your app can't connect to the database
- This is the connection string from your PostgreSQL service

---

#### **Variable 2: JWT_SECRET**
1. Look at the second row with `NAME_OF_VARIABLE`
2. Click in the **left field** (where it says "NAME_OF_VARIABLE")
3. Delete "NAME_OF_VARIABLE"
4. Type: `JWT_SECRET`
5. Click in the **right field** (Value)
6. Type: `my-super-secret-key-12345-change-this`
   - (Or any random string - this is for security)

**Why:**
- JWT = JSON Web Token (used for user authentication)
- Secret = Key to create/verify login tokens
- **Security**: Without this, anyone could create fake login tokens!

**Learning:**
- When user logs in, backend creates a "token" (like a ticket)
- Token is signed with this secret
- Frontend sends token with every request
- Backend verifies token using this secret
- If secret is wrong, tokens won't work!

---

#### **Variable 3: CORS_ORIGINS**
1. Click the **"+ Add Environment Variable"** button (at the bottom)
2. A new row will appear
3. In the **left field** (Key): Type `CORS_ORIGINS`
4. In the **right field** (Value): Type `https://rosepay-app.vercel.app`
   - (Replace with your actual Vercel URL if different)

**Why:**
- CORS = Cross-Origin Resource Sharing
- **Problem**: Browsers block requests from different domains
- **Solution**: Backend must allow requests from frontend domain
- **Without this**: Frontend can't talk to backend (browser blocks it!)

**Learning:**
- Your frontend is at: `rosepay-app.vercel.app`
- Your backend will be at: `your-backend.onrender.com`
- Browser sees different domains → Blocks request
- CORS_ORIGINS tells backend: "It's okay, allow requests from rosepay-app.vercel.app"
- Browser checks with backend → Backend says "allowed" → Request works!

---

### **Step 4: Scroll to Build & Deploy Settings**
Scroll down past the Environment Variables section.

You should see sections like:
- **Build Command**
- **Start Command**
- Or **"Advanced"** section (click to expand)

**What to look for:**

#### **Build Command:**
- Should say: `pip install -r requirements.txt`
- If empty, type: `pip install -r requirements.txt`

**Why:**
- This installs all Python packages your app needs
- `pip` = Python package installer
- `-r requirements.txt` = Install packages listed in requirements.txt file
- Runs BEFORE your app starts

**Learning:**
- Your app needs libraries (FastAPI, SQLAlchemy, etc.)
- These are listed in `requirements.txt`
- Build command downloads and installs them
- Without this, your app won't have the libraries it needs!

---

#### **Start Command:**
- Should say: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- If empty, type: `uvicorn main:app --host 0.0.0.0 --port $PORT`

**Why:**
- `uvicorn` = Server that runs FastAPI apps
- `main:app` = Run the `app` from `main.py` file
- `--host 0.0.0.0` = Listen on all network interfaces (not just localhost)
- `--port $PORT` = Use Render's assigned port (Render sets this automatically)

**Learning:**
- Start Command = What to run when service starts
- `0.0.0.0` = Accept connections from anywhere (needed for internet)
- `localhost` = Only accept from same computer (won't work on internet!)
- `$PORT` = Environment variable Render provides (changes per deployment)

**Without this:** Render doesn't know how to run your Python app!

---

### **Step 5: Check Root Directory**
Look for **"Root Directory"** field.

**What to do:**
- If you see this field, leave it **empty** or type `.`
- This means "use the root of the repository"

**Why:**
- Your `main.py` is in the root folder
- Render needs to know where to look
- `.` = Current directory (root of repo)

---

### **Step 6: Deploy!**
1. Scroll to the bottom of the page
2. Look for a button like:
   - **"Create Web Service"**
   - **"Deploy"**
   - **"Save"**
3. Click it!
4. Wait 3-5 minutes

**What happens:**
1. Render pulls code from GitHub
2. Runs build command (`pip install -r requirements.txt`)
3. Installs all packages
4. Runs start command (`uvicorn main:app...`)
5. Starts your FastAPI server
6. Makes it accessible on the internet

**Why it takes time:**
- Pulling code: 10-20 seconds
- Installing packages: 60-90 seconds
- Building: 10-20 seconds
- Starting server: 10-20 seconds
- Health checks: 30-60 seconds
- Total: 3-5 minutes

---

## ✅ What You Should See After Deploying

1. **"Deploying..."** or **"Building..."** message
2. Progress logs showing:
   - "Cloning repository..."
   - "Installing dependencies..."
   - "Starting service..."
3. **"Live"** status with green dot
4. A URL like: `rosepay-backend.onrender.com`

---

## 🎓 Summary of What We Did

1. **Set DATABASE_URL** → Tells backend where database is
2. **Set JWT_SECRET** → Security key for authentication
3. **Set CORS_ORIGINS** → Allows frontend to access backend
4. **Set Build Command** → Installs Python packages
5. **Set Start Command** → Tells Render how to run your app
6. **Deployed** → Backend is now live!

---

## 🆘 Troubleshooting

### **Problem: "Required" error on NAME_OF_VARIABLE**
- Delete that row (click trash icon)
- Or change it to a real variable name (like JWT_SECRET)

### **Problem: Can't find Build/Start Command fields**
- Scroll down more
- Look for "Advanced" section and expand it
- Or they might be in a different tab

### **Problem: Build fails**
- Check Build Command is: `pip install -r requirements.txt`
- Check Start Command is: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- Check DATABASE_URL is correct

### **Problem: "Cannot connect to database"**
- Verify DATABASE_URL is from your PostgreSQL service
- Make sure PostgreSQL service is running (green dot)

---

## ✅ Ready?

**Complete the steps above on this page!**

**Most Important:**
- ✅ Set DATABASE_URL (you already have this!)
- ✅ Set JWT_SECRET
- ✅ Set CORS_ORIGINS
- ✅ Set Build Command: `pip install -r requirements.txt`
- ✅ Set Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- ✅ Click "Create Web Service" or "Deploy"

**When deployment finishes, tell me:**
- "Deployment done"
- Or give me your Render backend URL

**Then we'll connect frontend to backend in Step 5!** 🚀
