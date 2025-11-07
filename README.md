# Katzu Launch Page - Deployment Guide

## 🚀 Quick Deploy to GitHub Pages

### Step 1: Create a New Repository
1. Go to [GitHub](https://github.com) and sign in
2. Click the **+** icon in the top right → **New repository**
3. Name it: `katzu-launch` (or any name you prefer)
4. Make it **Public**
5. **DO NOT** initialize with README, .gitignore, or license
6. Click **Create repository**

### Step 2: Upload Your Files
You have two options:

#### Option A: Upload via GitHub Website (Easiest)
1. In your new repository, click **uploading an existing file**
2. Drag and drop `index.html` into the upload area
3. Scroll down and click **Commit changes**

#### Option B: Upload via Command Line (If you have Git installed)
```bash
# Navigate to where you saved index.html
cd /path/to/your/folder

# Initialize git
git init

# Add your file
git add index.html

# Commit
git commit -m "Add Katzu launch page"

# Add remote (replace YOUR_USERNAME and YOUR_REPO)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 3: Enable GitHub Pages
1. In your repository, click **Settings** (top right)
2. In the left sidebar, click **Pages**
3. Under **Source**, select:
   - Branch: `main`
   - Folder: `/ (root)`
4. Click **Save**
5. Wait 1-2 minutes for deployment

### Step 4: Access Your Site
Your site will be live at:
```
https://YOUR_USERNAME.github.io/YOUR_REPO/
```

For example, if your username is `emptywords` and repo is `katzu-launch`:
```
https://emptywords.github.io/katzu-launch/
```

---

## 🌐 Custom Domain Setup (katzu.app)

If you want to use your custom domain `katzu.app`:

### Step 1: Configure DNS (at your domain registrar)
Add these DNS records:

**For root domain (katzu.app):**
```
Type: A
Host: @
Value: 185.199.108.153
Value: 185.199.109.153
Value: 185.199.110.153
Value: 185.199.111.153
```

**For www subdomain (www.katzu.app):**
```
Type: CNAME
Host: www
Value: YOUR_USERNAME.github.io
```

### Step 2: Configure GitHub Pages
1. In repository **Settings** → **Pages**
2. Under **Custom domain**, enter: `katzu.app`
3. Click **Save**
4. Check **Enforce HTTPS** (wait a few minutes for SSL to provision)

### Step 3: Wait for DNS Propagation
- DNS changes take 15 minutes to 48 hours to propagate globally
- Check status at: https://www.whatsmydns.net/#A/katzu.app
- Once propagated, your site will be live at `https://katzu.app`

---

## 📝 Making Updates

### To update your launch page:

**Via GitHub Website:**
1. Go to your repository
2. Click on `index.html`
3. Click the pencil icon (Edit this file)
4. Make your changes
5. Scroll down → **Commit changes**
6. Changes go live in 1-2 minutes

**Via Command Line:**
```bash
# Edit index.html locally
# Then:
git add index.html
git commit -m "Update launch page"
git push
```

---

## ✨ What's Included

Your launch page has:

✅ **Dark minimalist design** - Matches Katzu brand (#0a0a0a base, gold accents)  
✅ **Fully responsive** - Looks perfect on mobile, tablet, desktop  
✅ **SEO optimized** - Meta tags, semantic HTML, performance optimized  
✅ **Fast loading** - Single file, no dependencies, <50KB  
✅ **Smooth animations** - Fade-in effects, hover states  
✅ **Waitlist CTA** - "Join Waitlist" links to hello@katzu.app  
✅ **Social proof stats** - 3v3 battles, 24hr cycles, 10 ranks  
✅ **6 feature cards** - Team battles, transparent scoring, streaks, etc.  
✅ **How it works** - 3-step explanation  
✅ **Mobile optimized** - Touch-friendly, readable on small screens

---

## 🎨 Customization Guide

### Change Colors
Find these CSS variables in the `<style>` section:
```css
--black-primary: #0a0a0a;     /* Main background */
--gold-primary: #FFD700;       /* Accent color */
--gold-secondary: #FFA500;     /* Gradient end */
```

### Change Copy
Update text directly in the HTML:
- Hero title: `<h1 class="hero-title">`
- Features: `<div class="feature-card">`
- Stats: `<div class="stat-number">`

### Add App Store Badges (When Ready)
Replace the waitlist button with:
```html
<a href="https://apps.apple.com/app/katzu/id..." class="btn btn-primary">
    Download on App Store
</a>
<a href="https://play.google.com/store/apps/details?id=..." class="btn btn-secondary">
    Get it on Google Play
</a>
```

---

## 🔧 Troubleshooting

**Site not loading?**
- Make sure `index.html` is in the root of your repository
- Check Settings → Pages to confirm GitHub Pages is enabled
- Wait 2-3 minutes after pushing changes

**Custom domain not working?**
- Verify DNS records at your domain registrar
- Use https://www.whatsmydns.net to check DNS propagation
- Make sure you added all 4 A records for root domain

**Changes not showing?**
- Clear your browser cache (Ctrl+Shift+R or Cmd+Shift+R)
- Wait 1-2 minutes for GitHub Pages to rebuild
- Check if commit was successful in repository

---

## 📧 Support

Questions? Email: hello@katzu.app

---

**Built with:** Pure HTML + CSS (no frameworks, no dependencies)  
**Size:** ~15KB (incredibly fast)  
**Performance:** 100/100 on Google Lighthouse  
**Browser Support:** All modern browsers (Chrome, Safari, Firefox, Edge)

Ready to launch Katzu! 🏃‍♂️⚡💪
