# 📋 STEP 5: Connect Frontend to Backend

## 🎯 What We're Doing
We're connecting your frontend (Vercel) to your backend (Render) so they can talk to each other!

---

## ✅ Current Status

I can see your backend is deploying on Render:
- **URL**: `https://rosepay-backend.onrender.com`
- **Status**: Building (wait for it to finish!)

---

## ⏳ Step 1: Wait for Backend to Finish Building

**On the Render page, you should see:**
- Status: "Building" (gray badge)
- Logs showing progress

**Wait until you see:**
- ✅ Status: "Live" (green badge)
- ✅ Or "Deployed successfully"

**This takes 3-5 minutes!**

**What's happening:**
1. Cloning code from GitHub ✅ (you see this in logs)
2. Installing packages (pip install)
3. Building the app
4. Starting the server
5. Health checks

---

## ✅ Step 2: Verify Backend is Working

Once status shows "Live":

1. **Copy your backend URL**: `https://rosepay-backend.onrender.com`
2. **Test it**: Open in browser
3. **You should see**: JSON response like `{"message": "RosePay - Wallet Payment API is running"}`

**If you see this, backend is working!** ✅

---

## 🔗 Step 3: Connect Frontend to Backend

Now we need to tell your frontend where the backend is!

### **3.1: Go to Vercel**
1. Open: **https://vercel.com**
2. Sign in
3. Find your **"rosepay-app"** project
4. Click on it

### **3.2: Update Environment Variable**
1. Go to **"Settings"** tab
2. Click **"Environment Variables"** (left sidebar)
3. Find **"VITE_API_URL"**
4. Click **"Edit"** (or the pencil icon)
5. **Value**: Change to your Render backend URL
   - Type: `https://rosepay-backend.onrender.com`
   - (Replace with your actual Render URL if different)
6. Click **"Save"**

**Why:**
- Frontend needs to know WHERE the backend is
- Currently it's empty or pointing to localhost
- We're changing it to your Render URL

**Learning:**
- Environment Variable = Setting that changes per environment
- Development: `http://localhost:8000`
- Production: `https://rosepay-backend.onrender.com`
- Same code works in both places!

---

### **3.3: Redeploy Frontend**
1. Go to **"Deployments"** tab
2. Find the latest deployment
3. Click **"..."** (three dots)
4. Click **"Redeploy"**
5. Wait 2-3 minutes

**Why:**
- Frontend was built with old environment variable (empty)
- We need to rebuild it with new backend URL
- Redeploy = Rebuild with new settings

---

## ✅ Step 4: Test Your App!

1. **Open your Vercel URL**: `https://rosepay-app.vercel.app`
2. **Try to register** a new user
3. **Try to login**
4. **Everything should work!** 🎉

**If it works:**
- ✅ Frontend and backend are connected!
- ✅ Your app is fully deployed!
- ✅ Users can use it!

---

## 🆘 Troubleshooting

### **Problem: Backend still "Building"**
- Wait a bit more (can take 5-10 minutes)
- Check logs for errors
- If stuck, check if there are error messages

### **Problem: Backend shows error**
- Check the logs in Render
- Look for error messages
- Common issues:
  - Missing environment variables
  - Wrong start command
  - Database connection issues

### **Problem: Frontend can't connect to backend**
- Check CORS_ORIGINS in Render includes your Vercel URL
- Check VITE_API_URL in Vercel is correct
- Make sure backend URL starts with `https://`

### **Problem: "CORS error" in browser**
- Backend CORS_ORIGINS must include frontend URL
- Check it's exactly: `https://rosepay-app.vercel.app`
- No trailing slash!

---

## 🎓 Summary

**What we did:**
1. ✅ Waited for backend to finish building
2. ✅ Verified backend is working
3. ✅ Updated frontend environment variable (VITE_API_URL)
4. ✅ Redeployed frontend
5. ✅ Tested the app

**Result:**
- Frontend (Vercel) ↔ Backend (Render) ✅
- Full app deployed and working! 🎉

---

## ✅ Ready?

**First: Wait for backend to show "Live" status**

**Then: Follow Step 3 to connect frontend!**

**Tell me when backend is "Live" and I'll help you connect!** 🚀
