# 🔧 Fix Railway Deployment - Step by Step

## 🚨 Current Issue
Both `anaconda-brows` and `bizbuilders-automation` Railway projects aren't deployed correctly.

---

## ✅ Step-by-Step Fix for `bizbuilders-automation` Backend

### Option 1: Fix via Railway Dashboard (Easiest)

#### Step 1: Delete and Recreate (If Needed)
1. Go to: https://railway.app/dashboard
2. If the project exists but is broken:
   - Option A: Delete it and recreate
   - Option B: Fix the existing one (see below)

#### Step 2: Create/Select Project
1. Go to: https://railway.app/dashboard
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose: **`erikhinla/bizbuilders-automation`** (or your repo)
5. Click **"Deploy Now"**

#### Step 3: Configure Service Settings
1. Click on the service that was created
2. Go to **"Settings"** tab
3. Set these values:
   - **Build Command:** `pip install -r requirements.txt` (or leave empty - Nixpacks auto-detects)
   - **Start Command:** `gunicorn content_hub_api:app --bind 0.0.0.0:$PORT`
   - **Root Directory:** `/` (leave default)
   - **Watch Paths:** (leave empty)

#### Step 4: Add Environment Variables
1. Go to **"Variables"** tab
2. Click **"New Variable"** for each:
   
   **Required:**
   ```
   PORT = 5000
   ```
   
   **API Keys (Required for Content Generator):**
   ```
   OPENAI_API_KEY = sk-your-actual-openai-key-here
   ANTHROPIC_API_KEY = sk-ant-your-actual-anthropic-key-here
   FLASK_DEBUG = False
   ```

   **Note:** Railway automatically sets `PORT` from the environment, but you can set it manually too.

#### Step 5: Generate Public Domain
1. Go to **"Settings"** → **"Networking"**
2. Click **"Generate Domain"**
3. Copy the generated URL (e.g., `https://bizbuilders-automation-production.up.railway.app`)
4. **Save this URL** - you'll need it for Vercel!

#### Step 6: Check Deployment
1. Go to **"Deployments"** tab
2. Watch for the build to complete
3. Status should show: **"Active"** ✅
4. Check **"Logs"** tab for any errors

---

### Option 2: Fix via Railway CLI

#### Step 1: Login to Railway
```bash
railway login
```

#### Step 2: Link to Existing Project (or Create New)
```bash
# Link to existing project
railway link

# Or create new project
railway init
```

#### Step 3: Set Environment Variables
```bash
# Set required variables
railway variables set PORT=5000
railway variables set FLASK_DEBUG=False
railway variables set OPENAI_API_KEY=sk-your-key-here
railway variables set ANTHROPIC_API_KEY=sk-ant-your-key-here
```

#### Step 4: Deploy
```bash
railway up
```

#### Step 5: Generate Domain
```bash
railway domain
```

Or in Railway Dashboard → Settings → Networking → Generate Domain

---

## 🔍 Troubleshooting Common Issues

### Issue 1: "No module named 'gunicorn'"
**Fix:** Make sure `gunicorn==21.2.0` is in `requirements.txt` ✅ (Already added)

### Issue 2: "Port already in use" or "Address already in use"
**Fix:** Railway automatically sets `$PORT` - make sure Start Command uses `$PORT`, not hardcoded `5000`

### Issue 3: "ModuleNotFoundError: No module named 'content_generation_hub'"
**Fix:** Make sure `content_generation_hub.py` is in the root directory and deployed

### Issue 4: Build fails during pip install
**Fix:** Check `requirements.txt` for version conflicts. Current file looks good.

### Issue 5: API not accessible
**Fix:**
1. Check Railway generated a public domain
2. Test: `curl https://your-railway-url.railway.app/api/health`
3. Should return: `{"status": "healthy", ...}`

---

## ✅ Verification Steps

### 1. Test Backend Health
Once deployed, test the API:
```bash
# Replace with your Railway URL
curl https://your-railway-url.railway.app/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "ai_configured": true
}
```

### 2. Check Deployment Logs
In Railway Dashboard → Your Project → **Logs** tab
Look for:
- ✅ "Starting Content Generation Hub API..."
- ✅ "API available at http://0.0.0.0:5000"
- ❌ Any error messages

### 3. Test Content Generation Endpoint
```bash
curl -X POST https://your-railway-url.railway.app/api/content/generate \
  -H "Content-Type: application/json" \
  -d '{"title": "Test", "content_type": "blog_post"}'
```

---

## 🔗 Connect Frontend to Backend

Once Railway backend is working:

### Step 1: Get Railway Backend URL
Copy from Railway Dashboard → Settings → Networking → Domain

### Step 2: Add to Vercel Environment Variables
```bash
# Replace with your actual Railway URL
echo "https://your-railway-url.railway.app" | npx vercel env add VITE_API_URL production preview development
```

Or via Vercel Dashboard:
1. Go to: https://vercel.com/dashboard
2. Select: **bizbuilders-automation**
3. Go to: **Settings** → **Environment Variables**
4. Add: `VITE_API_URL` = `https://your-railway-url.railway.app`
5. Check all environments (Production, Preview, Development)
6. Click **Save**

### Step 3: Redeploy Frontend
```bash
npx vercel --prod
```

---

## 📋 Quick Checklist

- [ ] Railway project created/recreated
- [ ] Start Command set to: `gunicorn content_hub_api:app --bind 0.0.0.0:$PORT`
- [ ] Environment variables added (PORT, OPENAI_API_KEY, ANTHROPIC_API_KEY, FLASK_DEBUG)
- [ ] Public domain generated in Railway
- [ ] Deployment successful (status: Active)
- [ ] Health check works: `/api/health` returns 200
- [ ] VITE_API_URL added to Vercel
- [ ] Frontend redeployed
- [ ] Content generator works!

---

## 🆘 Still Not Working?

### Check Logs
```bash
# Via CLI
railway logs

# Or in Dashboard
Railway Dashboard → Your Project → Logs tab
```

### Common Fixes:
1. **Restart Service:** Railway Dashboard → Your Project → Settings → Restart
2. **Redeploy:** Railway Dashboard → Your Project → Deployments → Redeploy
3. **Check Build Logs:** Look at the build phase for errors
4. **Verify Files:** Make sure `content_hub_api.py`, `requirements.txt`, and `Procfile` are in repo

---

## 🎯 Next Steps After Fix

1. ✅ Backend deployed and working
2. ✅ Get Railway backend URL
3. ✅ Add `VITE_API_URL` to Vercel
4. ✅ Redeploy frontend
5. ✅ Test content generator at: https://bizbuilders-automation-hcod3i6rg-erik-bizbuilders-projects.vercel.app/hub/generator

---

## 📞 Quick Commands Reference

```bash
# Railway CLI
railway login              # Login to Railway
railway status             # Check project status
railway variables          # View environment variables
railway variables set KEY=value  # Set variable
railway logs               # View deployment logs
railway up                 # Deploy
railway domain             # Get domain

# Vercel CLI
npx vercel env ls          # List environment variables
npx vercel env add VITE_API_URL production  # Add env var
npx vercel --prod          # Deploy to production
```

