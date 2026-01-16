# 🔑 STEP 2A: Create Personal Access Token

## 🎯 What We're Doing
GitHub needs a special password (called a "token") to let you upload code. We're creating that now!

---

## ✅ Step-by-Step Instructions (On This Page)

### **1. Note Field (What's this token for?)**
- You'll see a text box labeled "Note"
- Type: `deployment-token`
- Or type: `rosepay-app-deployment`
- (This is just a name to remember what it's for)

### **2. Expiration**
- You'll see a dropdown that says "30 days"
- **Leave it as is** (30 days is fine)
- Or change to "90 days" if you want it to last longer

### **3. Select Scopes (IMPORTANT!)**
- Scroll down to "Select scopes"
- You'll see checkboxes
- **Find the checkbox for `repo`**
- **CHECK the box** next to `repo`
  - It says: "Full control of private repositories"
  - When you check it, it will automatically check some smaller boxes below it - that's fine!

### **4. Generate Token**
- Scroll all the way down
- You'll see a green button: **"Generate token"**
- Click it!

### **5. COPY THE TOKEN! (VERY IMPORTANT!)**
- After clicking, you'll see a page with a long code
- It looks like: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
- **COPY THIS TOKEN NOW!**
  - Click on it to select all
  - Press `Command + C` to copy
  - ⚠️ **You can only see it once!** If you leave this page, you can't see it again!
  - **Save it somewhere safe** (like a text file or notes app)

---

## ✅ What to Do After Creating Token

Once you have the token copied:

1. **Go back to Terminal** (the black/white window)
2. **Run the push command again:**
   ```bash
   git push -u origin main
   ```
3. **When it asks for username**: Type `ap9629341-gif`
4. **When it asks for password**: 
   - **DON'T type your GitHub password!**
   - **Paste the token** you just copied (Command + V)
   - Press Enter

---

## 🆘 Troubleshooting

### **Problem: Can't find `repo` checkbox**
- Scroll down in the "Select scopes" section
- Look for the first checkbox that says `repo`
- It's usually at the top of the scopes list

### **Problem: Token page disappeared**
- Don't worry! Just create a new one
- Go back to: https://github.com/settings/tokens/new
- Follow the steps again

### **Problem: Token doesn't work**
- Make sure you copied the ENTIRE token (it's long!)
- Make sure you checked the `repo` checkbox
- Try creating a new token

---

## ✅ Ready?

**Complete these steps on the GitHub page:**
1. ✅ Type note: `deployment-token`
2. ✅ Check the `repo` checkbox
3. ✅ Click "Generate token"
4. ✅ Copy the token
5. ✅ Go back to Terminal
6. ✅ Run `git push -u origin main`
7. ✅ When asked for password, paste the token

**When done, tell me: "Token created and pushed" or "Step 2 done"** 😊
