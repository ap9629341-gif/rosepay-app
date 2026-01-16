# 📋 STEP 2: Push Your Code to GitHub

## 🎯 What We're Doing
We're uploading your code from your computer to GitHub. This is like uploading photos to Google Drive!

---

## ✅ Step-by-Step Instructions

### **1. Open Terminal**
- On your Mac, press `Command + Space` (to open Spotlight)
- Type: `Terminal`
- Press `Enter`
- A black/white window will open - this is Terminal!

### **2. Go to Your Project Folder**
In Terminal, type this command and press Enter:

```bash
cd /Users/adarshpal/payment_app
```

**What this does**: Takes you to your project folder

### **3. Connect to GitHub**
Now we'll connect your local code to GitHub. Type this command (replace with YOUR username):

```bash
git remote add origin https://github.com/ap9629341-gif/rosepay-app.git
```

**Press Enter**

**What this does**: Tells your computer where to send the code

### **4. Set Main Branch**
Type this command:

```bash
git branch -M main
```

**Press Enter**

**What this does**: Names your branch "main"

### **5. Push Code to GitHub**
This is the big one! Type this command:

```bash
git push -u origin main
```

**Press Enter**

**What will happen**:
- It might ask for your GitHub username: Type `ap9629341-gif`
- It might ask for password: **DON'T use your GitHub password!**
  - Instead, use a **Personal Access Token**
  - (I'll help you create one if needed)

---

## 🔑 If It Asks for Password

GitHub doesn't accept passwords anymore. You need a **Personal Access Token**.

### **How to Create Token:**

1. **Open a new browser tab**
2. **Go to**: https://github.com/settings/tokens
3. **Click**: "Generate new token" → "Generate new token (classic)"
4. **Name it**: `deployment-token`
5. **Select**: `repo` (check the box)
6. **Scroll down** → Click "Generate token"
7. **COPY the token** (it looks like: `ghp_xxxxxxxxxxxx`)
   - ⚠️ **You can only see it once!** Copy it now!
8. **Go back to Terminal**
9. **When it asks for password**: Paste the token (not your password!)

---

## ✅ How to Know You're Done

You're done when you see:
- ✅ Messages like "Writing objects", "Counting objects"
- ✅ A message like "To https://github.com/ap9629341-gif/rosepay-app.git"
- ✅ "Branch 'main' set up to track remote branch 'main'"
- ✅ No error messages

---

## 🆘 Troubleshooting

### **Problem: "remote origin already exists"**
Run this first:
```bash
git remote remove origin
```
Then try Step 3 again.

### **Problem: "Authentication failed"**
- Make sure you're using a Personal Access Token (not password)
- Check the token has `repo` permission

### **Problem: "Permission denied"**
- Check your GitHub username is correct: `ap9629341-gif`
- Make sure the repository exists on GitHub

---

## 📸 What You Should See

After `git push`, you should see:
```
Enumerating objects: 122, done.
Counting objects: 100% (122/122), done.
Writing objects: 100% (122/122), done.
To https://github.com/ap9629341-gif/rosepay-app.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

---

## ✅ Ready?

**Run the commands above in Terminal!**

**If you get stuck, tell me:**
- What you see on your screen
- Any error messages
- Where you're stuck

**When done, tell me: "Step 2 done"** and I'll give you Step 3! 😊
