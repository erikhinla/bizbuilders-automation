# 🚀 Quick Deployment Guide - Anaconda Landing Page

Deploy your Anaconda Dark Mode landing page to **Vercel** (recommended) or **Railway**.

---

## ✅ Option 1: Deploy to Vercel (Recommended - Fastest)

**Why Vercel?** Perfect for React/Vite apps, automatic HTTPS, global CDN, free tier.

### Step 1: Install Vercel CLI (if not installed)
```bash
npm i -g vercel
```

### Step 2: Login to Vercel
```bash
vercel login
```

### Step 3: Deploy
```bash
vercel
```

Follow the prompts:
- Set up and deploy? **Yes**
- Which scope? **Your account**
- Link to existing project? **No** (first time)
- Project name? **anaconda-landing** (or your choice)
- Directory? **./** (current directory)
- Override settings? **No**

### Step 4: Add Environment Variables

After deployment, go to [Vercel Dashboard](https://vercel.com/dashboard):
1. Click on your project
2. Go to **Settings** → **Environment Variables**
3. Add this variable:
   - **Key**: `VITE_SUPABASE_PROJECT_ID`
   - **Value**: Your Supabase project ID (e.g., `abcdefghijklmnop`)
   - **Environment**: Production, Preview, Development (check all)
4. Click **Save**

### Step 5: Redeploy
```bash
vercel --prod
```

Or trigger a redeploy in the Vercel dashboard: **Deployments** → Click latest → **Redeploy**

### Step 6: Get Your Live URL

Your site will be live at:
- Production: `https://anaconda-landing.vercel.app`
- Preview: `https://anaconda-landing-<hash>.vercel.app`

**✅ Done!** Your landing page is live.

---

## ✅ Option 2: Deploy to Railway

**Why Railway?** Good for full-stack apps, easy database integration, Docker support.

### Step 1: Install Railway CLI
```bash
npm i -g @railway/cli
```

### Step 2: Login to Railway
```bash
railway login
```

### Step 3: Initialize Project
```bash
railway init
```

Follow prompts:
- Create new project? **Yes**
- Project name? **anaconda-landing**
- Select template? **Empty Project** or **Nixpacks**

### Step 4: Deploy
```bash
railway up
```

Railway will:
- Auto-detect Vite/React
- Install dependencies
- Build the project
- Deploy it

### Step 5: Add Environment Variables

In Railway Dashboard:
1. Go to your project
2. Click **Variables** tab
3. Add variable:
   - **Key**: `VITE_SUPABASE_PROJECT_ID`
   - **Value**: Your Supabase project ID
4. Click **Add**

### Step 6: Generate Public Domain

1. Go to **Settings** → **Networking**
2. Click **Generate Domain**
3. Your site will be at: `https://anaconda-landing.up.railway.app`

### Step 7: Redeploy (if needed)

Railway auto-redeploys when you push to GitHub. Or manually:
```bash
railway up
```

**✅ Done!** Your landing page is live on Railway.

---

## 🌐 GitHub Auto-Deploy (Recommended)

Both platforms support automatic deployment from GitHub:

### For Vercel:
1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click **Add New Project**
3. Import from **GitHub**
4. Select your repository: `bizbuilders-automation`
5. Configure:
   - **Framework Preset**: Vite
   - **Root Directory**: `./`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
6. Add environment variable: `VITE_SUPABASE_PROJECT_ID`
7. Click **Deploy**

Now every `git push` to `main` will auto-deploy! 🚀

### For Railway:
1. Go to [Railway Dashboard](https://railway.app/dashboard)
2. Click **New Project**
3. Select **Deploy from GitHub repo**
4. Select your repository
5. Railway will auto-detect and deploy
6. Add environment variable: `VITE_SUPABASE_PROJECT_ID`
7. Generate domain in **Settings** → **Networking**

---

## 🔧 Environment Variables Required

### Required:
- `VITE_SUPABASE_PROJECT_ID` - Your Supabase project ID (for Voice Agent WebSocket)

### Optional (if you add backend later):
- `VITE_API_URL` - Backend API URL
- `VITE_ANTHROPIC_API_KEY` - Anthropic API key
- `VITE_OPENAI_API_KEY` - OpenAI API key

---

## 📋 Pre-Deployment Checklist

Before deploying:

- [ ] Test build locally: `npm run build`
- [ ] Verify `vercel.json` exists (already configured)
- [ ] Check `package.json` has build script: `"build": "vite build"`
- [ ] Set `VITE_SUPABASE_PROJECT_ID` in environment variables
- [ ] Test Voice Agent widget locally (if backend is running)
- [ ] Check all assets load correctly
- [ ] Test responsive design on mobile

---

## 🧪 Test Locally First

```bash
# Install dependencies (if not done)
npm install

# Run dev server
npm run dev

# Test production build
npm run build
npm run preview
```

Visit `http://localhost:5173` to see your landing page.

---

## 🐛 Troubleshooting

### Build Fails:
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Environment Variables Not Working:
- Make sure variable names start with `VITE_` (required for Vite)
- Redeploy after adding variables
- Check variable is set for correct environment (Production/Preview)

### Voice Agent Not Connecting:
- Verify `VITE_SUPABASE_PROJECT_ID` is set correctly
- Check WebSocket URL format: `wss://${projectId}.supabase.co/functions/v1/voice-agent`
- Check browser console for errors
- Verify Supabase Edge Function is deployed

### Styles Not Loading:
- Check `index.css` is imported in `main.jsx`
- Verify Tailwind CSS is configured in `tailwind.config.js`
- Check build output includes CSS files

---

## 🎯 Post-Deployment

1. **Test the live site**: Visit your deployed URL
2. **Test Voice Agent**: Click the phone icon, try connecting
3. **Test responsive design**: Open on mobile device
4. **Set up custom domain** (optional):
   - Vercel: Settings → Domains → Add domain
   - Railway: Settings → Networking → Add custom domain
5. **Monitor deployments**: Both platforms show deployment status

---

## 💡 Quick Commands Reference

```bash
# Vercel
vercel              # Deploy to preview
vercel --prod       # Deploy to production
vercel env ls       # List environment variables
vercel logs         # View deployment logs

# Railway
railway up          # Deploy
railway logs        # View logs
railway open        # Open project in browser
railway variables   # Manage environment variables
```

---

## 📞 Need Help?

- **Vercel Docs**: https://vercel.com/docs
- **Railway Docs**: https://docs.railway.app
- **Vite Deploy Guide**: https://vitejs.dev/guide/static-deploy.html

---

## ✅ Success Checklist

- [ ] Project deployed to Vercel or Railway
- [ ] Environment variable `VITE_SUPABASE_PROJECT_ID` set
- [ ] Site accessible at public URL
- [ ] Voice Agent widget loads (phone icon visible)
- [ ] Styles/appearance correct (dark theme)
- [ ] Mobile responsive design works
- [ ] GitHub auto-deploy configured (optional but recommended)

**🎉 Your Anaconda landing page is now live!**

