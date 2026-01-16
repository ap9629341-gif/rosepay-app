# 📋 STEP 4: Deploy Backend to Railway

## 🎯 What We're Doing
We're putting your backend (the brain of your app) online. This is where your database and API live.

---

## 🧠 Why We Need Backend

**Think of it like this:**
- **Frontend (Vercel)** = The restaurant dining room (what customers see)
- **Backend (Railway)** = The kitchen (where food is prepared, orders are processed)

**What Backend Does:**
1. **Stores Data** - User accounts, wallets, transactions (in database)
2. **Processes Requests** - When user logs in, backend checks password
3. **Handles Business Logic** - Transfers money, creates payment links
4. **Provides API** - Frontend talks to backend to get/send data

**Without Backend:**
- ❌ Can't login (no database to check passwords)
- ❌ Can't create wallets (no place to store them)
- ❌ Can't transfer money (no logic to process it)

**With Backend:**
- ✅ Users can register and login
- ✅ Can create wallets and add money
- ✅ Can transfer money, create payment links
- ✅ Everything works!

---

## 🚂 Why Railway?

**Railway** is perfect for Python/FastAPI backends because:
1. **FREE Tier** - $5 credit/month (enough for testing)
2. **Includes Database** - PostgreSQL included (no separate setup)
3. **Easy Setup** - Connects to GitHub automatically
4. **Python Support** - Perfect for FastAPI

**Think of Railway as:**
- A server that runs your Python code 24/7
- A database that stores all your data
- An API endpoint that your frontend can call

---

## ✅ Step-by-Step Instructions

### **Step 1: Go to Railway**
1. Open a new browser tab
2. Go to: **https://railway.app**
3. Wait for the page to load

**Why:** Railway is where we'll host your backend

---

### **Step 2: Sign Up / Sign In**
1. Click **"Start a New Project"** or **"Login"** button
2. Choose **"Login with GitHub"**
3. Click **"Authorize Railway"** (if asked)
4. This connects Railway to your GitHub account

**Why:** Railway needs access to your GitHub to get your code

**Learning:**
- OAuth = Secure way to give one service access to another
- Railway can now read your GitHub repositories
- This is safe - Railway only accesses what you allow

---

### **Step 3: Create New Project**
1. After logging in, you'll see a dashboard
2. Click **"New Project"** button (usually top right or center)
3. A menu will appear
4. Select **"Deploy from GitHub repo"**

**Why:** We want Railway to get code from your GitHub repository

**Learning:**
- Project = A container for your app
- Railway can deploy from GitHub, Docker, or upload files
- We're using GitHub because code is already there

---

### **Step 4: Select Your Repository**
1. You'll see a list of your GitHub repositories
2. Find **"rosepay-app"** (or `ap9629341-gif/rosepay-app`)
3. Click on it to select
4. Railway will start deploying automatically

**What happens:**
- Railway pulls code from GitHub
- Detects it's a Python project
- Starts setting up the environment

**Why:** Railway needs to know which repository to deploy

---

### **Step 5: Wait for Initial Setup**
1. You'll see Railway working
2. It might show "Building..." or "Deploying..."
3. Wait 1-2 minutes
4. Don't worry if it fails initially - we need to configure it!

**Why:** Railway is trying to run your code, but needs configuration first

---

### **Step 6: Add PostgreSQL Database**
**This is IMPORTANT!** Your app needs a database to store data.

1. In your Railway project, you'll see your service
2. Click the **"+ New"** button (usually on the left sidebar or top)
3. A menu will appear
4. Select **"Database"**
5. Choose **"PostgreSQL"**
6. Wait for it to create (30-60 seconds)

**Why PostgreSQL?**
- **SQLite** (what you used locally) = File on your computer
- **PostgreSQL** = Professional database server
- **Why change?** SQLite doesn't work well for production (multiple users, reliability)

**Learning:**
- Database = Organized storage for data
- PostgreSQL = Industry-standard database
- Railway creates it automatically - no manual setup!

**What you'll see:**
- A new service appears: "PostgreSQL"
- It has a green dot (means it's running)

---

### **Step 7: Get Database URL**
1. Click on the **"PostgreSQL"** service (the database you just created)
2. Go to the **"Variables"** tab
3. You'll see a list of environment variables
4. Find **"DATABASE_URL"**
5. **COPY the value** (it looks like: `postgresql://postgres:password@host:port/railway`)

**Why:**
- Your Python code needs to know WHERE the database is
- DATABASE_URL = Address of your database
- We'll give this to your backend so it can connect

**Learning:**
- Environment Variable = Configuration that changes per environment
- Local: Database is a file (`wallet_app.db`)
- Production: Database is a server (PostgreSQL URL)
- Same code works in both places!

**⚠️ IMPORTANT:** Save this URL somewhere! You'll need it in the next step.

---

### **Step 8: Configure Backend Service**
1. Click on your **backend service** (the one with Python/FastAPI icon, not PostgreSQL)
2. Go to **"Variables"** tab
3. Click **"New Variable"** button

**Why:** We need to tell your backend:
- Where the database is
- Secret keys for security
- Where frontend is (for CORS)

---

### **Step 9: Add Environment Variables**
Add these variables **one by one**:

#### **Variable 1: DATABASE_URL**
1. Click **"New Variable"**
2. **Key**: Type `DATABASE_URL`
3. **Value**: Paste the PostgreSQL URL you copied in Step 7
4. Click **"Add"**

**Why:**
- Tells your backend WHERE to find the database
- Without this, backend can't connect to database
- This is the connection string

**Learning:**
- Connection String = Address + credentials to connect
- Format: `postgresql://username:password@host:port/database`
- Railway generates this automatically

---

#### **Variable 2: JWT_SECRET**
1. Click **"New Variable"** again
2. **Key**: Type `JWT_SECRET`
3. **Value**: Type any random string, like: `my-super-secret-key-12345-change-this`
4. Click **"Add"**

**Why:**
- JWT = JSON Web Token (used for authentication)
- Secret = Key to sign/verify tokens
- **Why important:** Without this, anyone could create fake login tokens!

**Learning:**
- JWT = Secure way to identify logged-in users
- Secret = Like a password to create tokens
- Should be long and random (hard to guess)

**Security Note:**
- In production, use a very long random string
- Never share this secret!
- If leaked, change it immediately

---

#### **Variable 3: CORS_ORIGINS**
1. Click **"New Variable"** again
2. **Key**: Type `CORS_ORIGINS`
3. **Value**: Type your Vercel URL: `https://rosepay-app.vercel.app`
   - (Replace with your actual Vercel URL if different)
4. Click **"Add"**

**Why:**
- CORS = Cross-Origin Resource Sharing
- **Problem:** Browsers block requests from different domains
- **Solution:** Backend must allow requests from frontend domain
- **Without this:** Frontend can't talk to backend (browser blocks it)

**Learning:**
- Same-Origin Policy = Security feature in browsers
- Prevents malicious websites from accessing your API
- CORS = Way to allow specific domains
- We're allowing our Vercel frontend to access Railway backend

**Example:**
```
Frontend (Vercel): https://rosepay-app.vercel.app
Backend (Railway): https://your-backend.railway.app
Browser: "Are these the same? No! Block the request!"
Backend: "It's okay, I allow requests from rosepay-app.vercel.app"
Browser: "Okay, request allowed!"
```

---

### **Step 10: Configure Start Command**
1. Still in your backend service
2. Go to **"Settings"** tab
3. Scroll to **"Deploy"** section
4. Find **"Start Command"** field
5. Type: `uvicorn main:app --host 0.0.0.0 --port $PORT`

**Why:**
- Railway needs to know HOW to start your app
- `uvicorn` = Server that runs FastAPI
- `main:app` = Run the `app` from `main.py` file
- `--host 0.0.0.0` = Listen on all network interfaces (not just localhost)
- `--port $PORT` = Use Railway's assigned port (Railway sets this automatically)

**Learning:**
- Start Command = What to run when service starts
- `0.0.0.0` = Accept connections from anywhere (needed for internet)
- `$PORT` = Environment variable Railway provides (changes per deployment)

**Without this:** Railway doesn't know how to run your Python app!

---

### **Step 11: Get Backend URL**
1. Still in backend service **"Settings"** tab
2. Scroll to **"Domains"** section
3. You'll see a URL like: `your-app.up.railway.app`
4. **COPY THIS URL!** ✅

**Why:**
- This is your backend's address on the internet
- Frontend needs this to make API calls
- We'll give this to frontend in the next step

**Learning:**
- Domain = Address on the internet
- Railway gives you a free subdomain
- You can add custom domain later (like `api.yourname.com`)

---

### **Step 12: Deploy!**
1. Railway should auto-deploy when you add variables
2. If not, go to **"Deployments"** tab
3. Click **"Redeploy"** button
4. Wait 2-3 minutes

**What happens:**
1. Railway pulls latest code from GitHub
2. Installs Python dependencies (`pip install -r requirements.txt`)
3. Runs database migrations (creates tables)
4. Starts your FastAPI server
5. Makes it accessible on the internet

**Why it takes time:**
- Installing packages: 30-60 seconds
- Building: 10-20 seconds
- Starting server: 10-20 seconds
- Health checks: 30 seconds
- Total: 2-3 minutes

---

## ✅ How to Know You're Done

You're done when:
- ✅ PostgreSQL database is running (green dot)
- ✅ Backend service is running (green dot)
- ✅ All environment variables are set
- ✅ You have your backend URL (like `your-app.up.railway.app`)
- ✅ No error messages in logs

---

## 🆘 Troubleshooting

### **Problem: Build fails**
- Check all environment variables are set
- Check Start Command is correct
- Look at logs for error messages

### **Problem: "Cannot connect to database"**
- Check DATABASE_URL is correct (copied from PostgreSQL service)
- Make sure PostgreSQL service is running (green dot)

### **Problem: "CORS error" in frontend**
- Check CORS_ORIGINS matches your Vercel URL exactly
- Make sure it starts with `https://`
- No trailing slash!

---

## 🎓 Summary of What We Did

1. **Created Railway Project** → Container for your backend
2. **Added PostgreSQL Database** → Storage for your data
3. **Set DATABASE_URL** → Tells backend where database is
4. **Set JWT_SECRET** → Security key for authentication
5. **Set CORS_ORIGINS** → Allows frontend to access backend
6. **Set Start Command** → Tells Railway how to run your app
7. **Got Backend URL** → Address of your API on internet
8. **Deployed** → Backend is now live!

---

## ✅ Ready?

**Follow the steps above!**

**Most Important:**
- ⚠️ **Add PostgreSQL database FIRST**
- ⚠️ **Copy DATABASE_URL from PostgreSQL service**
- ⚠️ **Set all 3 environment variables**
- ⚠️ **Set Start Command**
- ⚠️ **Copy your backend URL**

**When done, tell me:**
- "Step 4 done"
- Or give me your Railway backend URL

**Then we'll connect frontend to backend in Step 5!** 🚀
