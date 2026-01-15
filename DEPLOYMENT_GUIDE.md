# 🚀 Deployment Guide - Deploy to Production

## 💰 Cost Overview

### **FREE Options (Recommended for Start)**
- ✅ **Vercel** - Frontend hosting (FREE forever)
- ✅ **Netlify** - Frontend hosting (FREE forever)
- ✅ **Railway** - Backend + Database (FREE tier: $5 credit/month)
- ✅ **Render** - Backend + Database (FREE tier available)
- ✅ **Supabase** - Database (FREE tier: 500MB)

### **Paid Options (When You Scale)**
- **Heroku** - $7/month per dyno (no free tier anymore)
- **AWS** - Pay as you go (can be expensive)
- **DigitalOcean** - $6/month minimum

---

## 🎯 Recommended FREE Setup

### **Best FREE Stack:**
1. **Frontend**: Vercel (FREE)
2. **Backend**: Railway (FREE tier)
3. **Database**: Railway PostgreSQL (FREE tier)

**Total Cost: $0/month** ✅

---

## 📋 Step-by-Step Deployment

### **Part 1: Deploy Frontend (Vercel) - FREE**

#### Step 1: Prepare Frontend
```bash
cd frontend
npm run build
```

#### Step 2: Create Vercel Account
1. Go to https://vercel.com
2. Sign up with GitHub (FREE)
3. Click "New Project"

#### Step 3: Deploy
1. Import your GitHub repo (or drag & drop `frontend` folder)
2. Vercel auto-detects React
3. Click "Deploy"
4. **Done!** You get a URL like: `your-app.vercel.app`

**Time: 5 minutes** ⏱️

---

### **Part 2: Deploy Backend (Railway) - FREE**

#### Step 1: Create Railway Account
1. Go to https://railway.app
2. Sign up with GitHub (FREE)
3. You get $5 free credit/month

#### Step 2: Create New Project
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your repo

#### Step 3: Add PostgreSQL Database
1. Click "New" → "Database" → "PostgreSQL"
2. Railway creates database automatically
3. Copy database URL (looks like: `postgresql://...`)

#### Step 4: Set Environment Variables
In Railway project settings, add:
```
DATABASE_URL=postgresql://... (from step 3)
JWT_SECRET=your-secret-key-here
RAZORPAY_KEY_ID=your-key
RAZORPAY_KEY_SECRET=your-secret
```

#### Step 5: Deploy
1. Railway auto-detects Python
2. Sets start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
3. Click "Deploy"
4. **Done!** You get a URL like: `your-app.railway.app`

**Time: 10 minutes** ⏱️

---

### **Part 3: Update Frontend API URL**

#### Update Frontend Config
1. Go to Vercel project settings
2. Add environment variable:
   ```
   VITE_API_URL=https://your-backend.railway.app
   ```
3. Update `frontend/src/config/api.js`:
   ```javascript
   const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
   ```
4. Redeploy frontend

---

## 🌐 How Users Will Access Your App

### **Option 1: Free Subdomain (Easiest)**
- **Frontend**: `your-app.vercel.app`
- **Backend**: `your-backend.railway.app`
- **Users visit**: `your-app.vercel.app`
- **Cost**: FREE ✅

### **Option 2: Custom Domain (Professional)**
1. Buy domain from Namecheap/GoDaddy ($10-15/year)
2. Connect to Vercel (FREE)
3. Users visit: `yourdomain.com`
4. **Cost**: $10-15/year only

---

## 📊 Deployment Comparison

| Platform | Frontend | Backend | Database | Cost |
|----------|----------|---------|----------|------|
| **Vercel** | ✅ | ❌ | ❌ | FREE |
| **Netlify** | ✅ | ❌ | ❌ | FREE |
| **Railway** | ❌ | ✅ | ✅ | FREE tier |
| **Render** | ✅ | ✅ | ✅ | FREE tier |
| **Heroku** | ❌ | ✅ | ✅ | $7/month |
| **AWS** | ✅ | ✅ | ✅ | Pay as you go |

---

## 🎯 Quick Start: Deploy in 15 Minutes

### **Step 1: Frontend (5 min)**
```bash
# Build frontend
cd frontend
npm run build

# Deploy to Vercel
npx vercel --prod
```

### **Step 2: Backend (10 min)**
1. Push code to GitHub
2. Connect Railway to GitHub
3. Add PostgreSQL database
4. Set environment variables
5. Deploy!

---

## 🔧 Required Changes for Production

### **1. Update Database (SQLite → PostgreSQL)**

#### Install PostgreSQL driver:
```bash
pip install psycopg2-binary
```

#### Update `database.py`:
```python
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Use PostgreSQL in production, SQLite in development
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./wallet_app.db")

if DATABASE_URL.startswith("postgresql"):
    # PostgreSQL
    engine = create_engine(DATABASE_URL)
else:
    # SQLite (development)
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

### **2. Update CORS in `main.py`**
```python
# Allow your production frontend URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Development
        "https://your-app.vercel.app",  # Production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### **3. Create `Procfile` (for Railway/Heroku)**
Create file: `Procfile`
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

### **4. Create `runtime.txt` (for Railway)**
Create file: `runtime.txt`
```
python-3.11
```

---

## 📱 How Users Will Find Your App

### **1. Share the URL**
- Give them: `https://your-app.vercel.app`
- They can bookmark it
- Works on mobile too!

### **2. Custom Domain**
- Buy: `rosepay.com` ($12/year)
- Connect to Vercel
- Users visit: `rosepay.com`

### **3. Share on Social Media**
- Post: "Check out my payment app: rosepay.com"
- Share in groups
- Add to portfolio

---

## 💡 Free Tier Limits

### **Vercel (Frontend)**
- ✅ Unlimited deployments
- ✅ 100GB bandwidth/month
- ✅ FREE forever

### **Railway (Backend)**
- ✅ $5 free credit/month
- ✅ Enough for ~500 hours of runtime
- ✅ Perfect for testing/small apps

### **Render (Alternative)**
- ✅ FREE tier available
- ✅ 750 hours/month
- ✅ Auto-sleeps after inactivity

---

## 🚨 Important Notes

### **1. Environment Variables**
Never commit secrets to GitHub!
- Use platform's environment variables
- Keep `.env` in `.gitignore`

### **2. Database Migration**
- SQLite → PostgreSQL: Data won't transfer automatically
- You'll need to export/import or start fresh

### **3. HTTPS**
- Vercel & Railway provide FREE SSL
- Your app is secure automatically!

---

## ✅ Deployment Checklist

- [ ] Build frontend (`npm run build`)
- [ ] Deploy frontend to Vercel
- [ ] Create Railway account
- [ ] Add PostgreSQL database
- [ ] Set environment variables
- [ ] Deploy backend to Railway
- [ ] Update frontend API URL
- [ ] Test deployed app
- [ ] Share URL with users!

---

## 🎉 After Deployment

### **Your App Will Be:**
- ✅ Live on the internet
- ✅ Accessible from anywhere
- ✅ Secure (HTTPS)
- ✅ Fast (CDN)
- ✅ FREE!

### **Share It:**
- "Check out my payment app: your-app.vercel.app"
- Add to portfolio
- Show to friends/family
- Post on social media

---

## 🆘 Troubleshooting

### **Frontend not loading?**
- Check Vercel deployment logs
- Verify API URL is correct
- Check CORS settings

### **Backend errors?**
- Check Railway logs
- Verify environment variables
- Check database connection

### **Database issues?**
- Verify DATABASE_URL is correct
- Check PostgreSQL is running
- Review connection string format

---

## 📚 Next Steps

1. **Deploy now** - Follow steps above
2. **Test thoroughly** - Make sure everything works
3. **Share with users** - Give them the URL
4. **Monitor** - Check logs regularly
5. **Scale** - Upgrade when needed

---

**Ready to deploy? Let's do it!** 🚀
