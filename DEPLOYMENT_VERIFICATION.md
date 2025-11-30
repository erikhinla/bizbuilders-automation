# ✅ Deployment Verification Checklist

## 🔗 Your Live Sites

### Landing Page (Anaconda Dark Mode)
**Production URL:**
👉 **https://bizbuilders-automation-hcod3i6rg-erik-bizbuilders-projects.vercel.app**

**Content Generator:**
👉 **https://bizbuilders-automation-hcod3i6rg-erik-bizbuilders-projects.vercel.app/hub/generator**

**Dashboard:**
👉 **https://bizbuilders-automation-hcod3i6rg-erik-bizbuilders-projects.vercel.app/hub/dashboard**

---

## ✅ Railway Deployment Checklist

### [ ] Railway Project Created
**Verify:**
1. Go to: https://railway.app/dashboard
2. Check if you have a project named `bizbuilders-automation` (or similar)
3. **Status:** ✅ **Need to verify**

**How to check:**
```bash
# Via CLI
railway status

# Or visit dashboard
https://railway.app/dashboard
```

---

### [ ] Service Deployed Successfully
**Verify:**
1. In Railway Dashboard → Your Project → Deployments tab
2. Look for latest deployment with status: **"Active"** or **"Running"**
3. Check deployment logs for any errors
4. **Status:** ❓ **Check Railway Dashboard**

**Check deployment:**
```bash
# View deployments
railway logs

# Or visit Railway dashboard
https://railway.app/dashboard → Your Project → Deployments
```

---

### [ ] Environment Variables Added
**Required Variables for Backend:**
- `OPENAI_API_KEY` - Your OpenAI API key
- `ANTHROPIC_API_KEY` - Your Anthropic API key (optional)
- `PORT=5000` - Flask port
- `FLASK_DEBUG=False` - Production mode

**Verify in Railway:**
1. Go to: https://railway.app/dashboard
2. Select your project → **Variables** tab
3. Check if all required variables are set
4. **Status:** ❓ **Check Railway Dashboard**

**Via CLI:**
```bash
railway variables
```

---

### [ ] Public Domain Generated
**Verify:**
1. In Railway Dashboard → Your Project → **Settings** → **Networking**
2. Check if a domain is generated (e.g., `https://your-app-name.railway.app`)
3. Copy the domain URL
4. **Status:** ❓ **Check Railway Dashboard**

**Generate domain if missing:**
1. Railway Dashboard → Settings → Networking
2. Click **"Generate Domain"**
3. Your API will be at: `https://your-app-name.up.railway.app`

---

### [ ] Vercel Environment Variable Updated
**Required Variable:**
- `VITE_API_URL` - Your Railway backend URL (e.g., `https://your-app-name.railway.app`)

**Verify in Vercel:**
1. Go to: https://vercel.com/dashboard
2. Select project: **bizbuilders-automation**
3. Go to: **Settings** → **Environment Variables**
4. Check if `VITE_API_URL` is set to your Railway backend URL
5. **Status:** ❓ **May need to add this**

**Check via CLI:**
```bash
npx vercel env ls
```

**Add if missing:**
```bash
# Replace with your Railway domain
echo "https://your-app-name.railway.app" | npx vercel env add VITE_API_URL production preview development
```

---

### [ ] Frontend Redeployed
**Verify:**
1. Check latest Vercel deployment:
   - https://vercel.com/dashboard → bizbuilders-automation → Deployments
2. Latest deployment should be successful (green checkmark)
3. **Current Status:** ✅ **Deployed** (Latest: 6 days ago)
   - URL: https://bizbuilders-automation-hcod3i6rg-erik-bizbuilders-projects.vercel.app

**Redeploy if needed:**
```bash
npx vercel --prod
```

---

### [ ] Content Generator Works!
**Test the Content Generator:**
1. Visit: https://bizbuilders-automation-hcod3i6rg-erik-bizbuilders-projects.vercel.app/hub/generator
2. Try generating content
3. Check if it connects to Railway backend
4. **Status:** ❓ **Test it now!**

**If it doesn't work:**
- Check browser console (F12) for errors
- Verify `VITE_API_URL` is set correctly in Vercel
- Check Railway backend is running and accessible
- Verify Railway backend URL is correct

---

## 🔍 Quick Verification Commands

### Check Railway Status
```bash
# Login (if needed)
railway login

# Check projects
railway status

# View logs
railway logs

# View variables
railway variables
```

### Check Vercel Status
```bash
# List deployments
npx vercel ls

# View environment variables
npx vercel env ls

# View logs
npx vercel logs [deployment-url]
```

---

## 🌐 All Your Live URLs

### Frontend (Vercel)
- **Landing Page:** https://bizbuilders-automation-hcod3i6rg-erik-bizbuilders-projects.vercel.app
- **Dashboard:** https://bizbuilders-automation-hcod3i6rg-erik-bizbuilders-projects.vercel.app/hub/dashboard
- **Content Generator:** https://bizbuilders-automation-hcod3i6rg-erik-bizbuilders-projects.vercel.app/hub/generator
- **Content Queue:** https://bizbuilders-automation-hcod3i6rg-erik-bizbuilders-projects.vercel.app/hub/content
- **Trends:** https://bizbuilders-automation-hcod3i6rg-erik-bizbuilders-projects.vercel.app/hub/trends
- **Settings:** https://bizbuilders-automation-hcod3i6rg-erik-bizbuilders-projects.vercel.app/hub/settings

### Backend (Railway)
- **API URL:** `https://your-railway-app-name.railway.app` (Check Railway Dashboard)
- **API Health Check:** `https://your-railway-app-name.railway.app/health` (if implemented)

---

## 📝 Next Steps

1. **If Railway project doesn't exist:**
   - Follow: `RAILWAY_DEPLOY.md` guide
   - Or visit: https://railway.app/dashboard → New Project

2. **If backend not deployed:**
   - Deploy `content_hub_api.py` to Railway
   - Set environment variables
   - Generate public domain

3. **If frontend can't connect to backend:**
   - Add `VITE_API_URL` in Vercel
   - Redeploy frontend
   - Test content generator

4. **To set custom domain (anacondabrows.com):**
   - In Vercel Dashboard → Settings → Domains
   - Add domain: `anacondabrows.com`
   - Update DNS records as instructed
   - SSL will be auto-configured

---

## ✅ Quick Status Check

Run these to verify everything:

```bash
# 1. Check Railway
railway status

# 2. Check Vercel deployments
npx vercel ls

# 3. Check Vercel env vars
npx vercel env ls

# 4. Test backend (replace with your Railway URL)
curl https://your-railway-app.railway.app/health

# 5. Test frontend
curl https://bizbuilders-automation-hcod3i6rg-erik-bizbuilders-projects.vercel.app
```

