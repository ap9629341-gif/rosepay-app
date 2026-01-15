# ⚡ Quick Deploy Guide - 15 Minutes

## 🎯 Goal: Get Your App Live for FREE

---

## Step 1: Deploy Frontend (5 min)

### Option A: Vercel (Recommended)
```bash
cd frontend
npm install -g vercel
vercel login
vercel --prod
```

**That's it!** You get a URL like: `your-app.vercel.app`

### Option B: Netlify
1. Go to https://netlify.com
2. Drag & drop `frontend/dist` folder
3. Done!

---

## Step 2: Deploy Backend (10 min)

### Using Railway (FREE)

1. **Sign up**: https://railway.app (use GitHub)
2. **New Project** → "Deploy from GitHub"
3. **Add Database** → PostgreSQL
4. **Set Environment Variables**:
   ```
   DATABASE_URL=postgresql://... (auto-filled)
   JWT_SECRET=your-secret-key
   ```
5. **Deploy** → Railway does the rest!

**You get**: `your-app.railway.app`

---

## Step 3: Connect Frontend to Backend

### Update Frontend Config
In Vercel project → Settings → Environment Variables:
```
VITE_API_URL=https://your-app.railway.app
```

Redeploy frontend.

---

## ✅ Done!

**Your app is live at**: `your-app.vercel.app`

**Cost**: $0/month ✅

**Users can access**: Just share the URL!

---

## 🔗 How Users Will Come

1. **You share the URL**: `your-app.vercel.app`
2. **They visit in browser**: Works on phone/computer
3. **They use the app**: Register, login, use features!

**That's it!** No app store needed for web apps!

---

## 💡 Pro Tips

- **Custom domain**: Buy `yourname.com` ($12/year) → Connect to Vercel
- **Share on social**: "Check out my app: your-app.vercel.app"
- **Add to portfolio**: Show your work!

---

**Ready? Let's deploy!** 🚀
