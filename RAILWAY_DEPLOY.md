# Railway Deployment - Step by Step

## 🚂 Deploy Backend to Railway (Easiest Option)

### Step 1: Sign Up
1. Go to: **https://railway.app**
2. Click **"Start a New Project"**
3. Sign up with **GitHub** (easiest - connects to your repo)

### Step 2: Create Project
1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Find and select: **`erikhinla/bizbuilders-automation`**
4. Click **"Deploy Now"**

### Step 3: Configure Service
Railway will auto-detect Python, but you need to configure:

1. **Click on the service** that was created
2. Go to **"Settings"** tab
3. Set **"Start Command"**:
   ```
   python content_hub_api.py
   ```
4. Set **"Root Directory"**: (leave blank or `/`)

### Step 4: Add Environment Variables
1. Go to **"Variables"** tab
2. Click **"New Variable"**
3. Add these variables:

   ```
   OPENAI_API_KEY=sk-your-actual-key-here
   ANTHROPIC_API_KEY=sk-ant-your-key-here (optional)
   PORT=5000
   FLASK_DEBUG=False
   ```

### Step 5: Deploy
1. Railway will automatically deploy when you save
2. Wait for build to complete (2-3 minutes)
3. Go to **"Settings"** → **"Networking"**
4. Click **"Generate Domain"** to get your public URL
5. Your API will be at: `https://your-app-name.railway.app`

### Step 6: Update Frontend
1. Go to **Vercel Dashboard**: https://vercel.com
2. Select your project: **bizbuilders-automation**
3. Go to **Settings** → **Environment Variables**
4. Add new variable:
   - **Key**: `VITE_API_URL`
   - **Value**: `https://your-app-name.railway.app` (from Railway)
5. Go to **Deployments** tab
6. Click **"Redeploy"** on the latest deployment

### Step 7: Test
1. Visit your Vercel site
2. Go to `/hub/generator`
3. Generate content - it should connect to Railway backend!

## 💰 Railway Pricing

- **Free Tier**: $5 credit/month (usually enough for testing)
- **Hobby Plan**: $5/month (500 hours)
- **Pro Plan**: $20/month (unlimited)

## 🔧 Troubleshooting

### If deployment fails:
1. Check **"Deployments"** tab for error logs
2. Make sure `Procfile` exists in root
3. Verify Python version (Railway auto-detects)

### If API doesn't work:
1. Check Railway logs: **"Deployments"** → Click deployment → **"View Logs"**
2. Verify environment variables are set
3. Check the generated domain is correct

### If frontend can't connect:
1. Verify `VITE_API_URL` in Vercel matches Railway URL
2. Check CORS is enabled in Flask (it is by default)
3. Redeploy frontend after adding environment variable

## ✅ Success Checklist

- [ ] Railway project created
- [ ] Service deployed successfully
- [ ] Environment variables added
- [ ] Public domain generated
- [ ] Vercel environment variable updated
- [ ] Frontend redeployed
- [ ] Content generator works!

## 📞 Need Help?

Railway has great docs: https://docs.railway.app

Your backend will be live at: `https://your-app.railway.app`
Your frontend is at: `https://bizbuilders-automation-*.vercel.app`


