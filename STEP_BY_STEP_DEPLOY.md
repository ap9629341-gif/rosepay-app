# 🚀 Step-by-Step Deployment Guide

## Let's Deploy Your App Together!

---

## 📋 Prerequisites Check

Before we start, make sure you have:
- ✅ GitHub account (we'll create one if needed)
- ✅ Code ready to deploy
- ✅ 15 minutes of time

---

## PART 1: Prepare Your Code for GitHub

### Step 1.1: Initialize Git (if not done)

Open terminal in your project folder and run:

```bash
cd /Users/adarshpal/payment_app
git init
git add .
git commit -m "Initial commit - RosePay app"
```

### Step 1.2: Create GitHub Repository

1. Go to https://github.com
2. Sign in (or create account - FREE)
3. Click **"+"** → **"New repository"**
4. Name it: `rosepay-app` (or any name)
5. Make it **Public** (or Private, your choice)
6. **DON'T** check "Initialize with README"
7. Click **"Create repository"**

### Step 1.3: Push Code to GitHub

GitHub will show you commands. Run these in terminal:

```bash
git remote add origin https://github.com/YOUR_USERNAME/rosepay-app.git
git branch -M main
git push -u origin main
```

**Replace `YOUR_USERNAME` with your GitHub username!**

---

## PART 2: Deploy Frontend to Vercel (5 minutes)

### Step 2.1: Go to Vercel

1. Open: https://vercel.com
2. Click **"Sign Up"**
3. Choose **"Continue with GitHub"**
4. Authorize Vercel to access GitHub

### Step 2.2: Create New Project

1. Click **"Add New..."** → **"Project"**
2. You'll see your GitHub repos
3. Find **"rosepay-app"** (or your repo name)
4. Click **"Import"**

### Step 2.3: Configure Project

Vercel will auto-detect React, but check these settings:

- **Framework Preset**: Vite (should be auto-detected)
- **Root Directory**: `frontend` (IMPORTANT!)
- **Build Command**: `npm run build` (auto-filled)
- **Output Directory**: `dist` (auto-filled)

### Step 2.4: Add Environment Variable

1. Scroll down to **"Environment Variables"**
2. Click **"Add"**
3. Key: `VITE_API_URL`
4. Value: `https://your-backend.railway.app` (we'll get this in Part 3)
5. **For now, leave it empty or use**: `http://localhost:8000`

### Step 2.5: Deploy!

1. Click **"Deploy"**
2. Wait 2-3 minutes
3. **You'll get a URL like**: `rosepay-app.vercel.app` ✅

**Save this URL!** We'll need it later.

---

## PART 3: Deploy Backend to Railway (10 minutes)

### Step 3.1: Go to Railway

1. Open: https://railway.app
2. Click **"Start a New Project"**
3. Choose **"Login with GitHub"**
4. Authorize Railway

### Step 3.2: Create New Project

1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Find your **"rosepay-app"** repo
4. Click **"Deploy Now"**

### Step 3.3: Add PostgreSQL Database

1. In your Railway project, click **"+ New"**
2. Select **"Database"**
3. Choose **"PostgreSQL"**
4. Railway creates database automatically ✅

### Step 3.4: Get Database URL

1. Click on the **PostgreSQL** service
2. Go to **"Variables"** tab
3. Find **"DATABASE_URL"**
4. **Copy this URL** (looks like: `postgresql://...`)

**Save this!** We'll use it next.

### Step 3.5: Set Environment Variables

1. Click on your **backend service** (not database)
2. Go to **"Variables"** tab
3. Click **"New Variable"**
4. Add these one by one:

```
DATABASE_URL = (paste the PostgreSQL URL from step 3.4)
JWT_SECRET = your-super-secret-key-change-this-12345
RAZORPAY_KEY_ID = (your Razorpay key - if you have one)
RAZORPAY_KEY_SECRET = (your Razorpay secret - if you have one)
CORS_ORIGINS = https://your-frontend.vercel.app
```

**Important**: Replace `your-frontend.vercel.app` with your actual Vercel URL from Part 2!

### Step 3.6: Configure Service

1. Click on your backend service
2. Go to **"Settings"** tab
3. Scroll to **"Deploy"**
4. Make sure:
   - **Root Directory**: (leave empty or set to `/`)
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Step 3.7: Deploy!

1. Railway will auto-deploy when you push to GitHub
2. Or click **"Deploy"** button
3. Wait 3-5 minutes
4. Check **"Logs"** tab to see progress

### Step 3.8: Get Backend URL

1. Once deployed, go to **"Settings"**
2. Find **"Domains"** section
3. Railway gives you a URL like: `your-app.up.railway.app`
4. **Copy this URL!** ✅

---

## PART 4: Connect Frontend to Backend

### Step 4.1: Update Frontend Environment Variable

1. Go back to **Vercel**
2. Go to your project
3. Click **"Settings"**
4. Go to **"Environment Variables"**
5. Find `VITE_API_URL`
6. Click **"Edit"**
7. Update value to: `https://your-backend.railway.app`
8. Click **"Save"**

### Step 4.2: Redeploy Frontend

1. In Vercel, go to **"Deployments"**
2. Click **"..."** on latest deployment
3. Click **"Redeploy"**
4. Wait 2 minutes

---

## PART 5: Update Backend CORS

### Step 5.1: Update CORS Environment Variable

1. Go back to **Railway**
2. Go to your backend service
3. **"Variables"** tab
4. Find `CORS_ORIGINS`
5. Update to: `https://your-frontend.vercel.app`
6. Railway auto-redeploys

---

## ✅ Done! Your App is Live!

### Your URLs:
- **Frontend**: `https://your-app.vercel.app`
- **Backend**: `https://your-backend.railway.app`

### Test It:
1. Open frontend URL in browser
2. Try registering a user
3. Try logging in
4. Everything should work! 🎉

---

## 🆘 Troubleshooting

### Frontend not loading?
- Check Vercel deployment logs
- Verify build succeeded
- Check environment variables

### Backend errors?
- Check Railway logs
- Verify DATABASE_URL is correct
- Check all environment variables

### CORS errors?
- Verify CORS_ORIGINS includes your frontend URL
- Check backend logs
- Make sure URLs match exactly

---

## 🎉 Success!

Your app is now live on the internet!

**Share it**: Give users your Vercel URL!

**Cost**: $0/month ✅

**Time taken**: ~15 minutes ✅

---

## 📞 Need Help?

If you get stuck at any step, let me know which step and I'll help you!
