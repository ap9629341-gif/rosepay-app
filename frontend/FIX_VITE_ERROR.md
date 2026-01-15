# 🔧 Fix: "vite: command not found"

## What's Happening

You're getting: `sh: vite: command not found`

**Why**: Even though vite is installed, the shell can't find it.

## ✅ Solution 1: Use npx (Recommended)

Instead of `npm run dev`, try:

```bash
npx vite
```

**What npx does**: Runs the local version of vite from node_modules

## ✅ Solution 2: Reinstall Dependencies

Sometimes node_modules gets corrupted. Try:

```bash
# Delete node_modules
rm -rf node_modules package-lock.json

# Reinstall everything
npm install

# Then try again
npm run dev
```

## ✅ Solution 3: Use Full Path

```bash
./node_modules/.bin/vite
```

## ✅ Solution 4: Update package.json Script

Change the script to use npx explicitly.
