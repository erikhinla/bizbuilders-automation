# 🔐 Environment Variable Setup Guide

## Required: VITE_SUPABASE_PROJECT_ID

This environment variable is needed for the Voice Agent widget to connect to your Supabase backend.

---

## Step 1: Get Your Supabase Project ID

### Option A: From Supabase Dashboard
1. Go to: https://supabase.com/dashboard
2. Select your project (or create a new one)
3. Go to **Settings** → **General**
4. Find **Reference ID** - this is your Project ID
5. Copy it (e.g., `abcdefghijklmnop`)

### Option B: From Your Supabase URL
If you know your Supabase URL, the Project ID is in it:
- URL format: `https://abcdefghijklmnop.supabase.co`
- Project ID is: `abcdefghijklmnop`

---

## Step 2: Set Environment Variable in Vercel

### Method 1: Via Vercel CLI (Quickest) ✅

```bash
# Set for all environments (Production, Preview, Development)
npx vercel env add VITE_SUPABASE_PROJECT_ID production preview development

# When prompted, paste your Supabase Project ID
```

### Method 2: Via Vercel Dashboard

1. Go to: https://vercel.com/dashboard
2. Click on your project: **bizbuilders-automation**
3. Go to: **Settings** → **Environment Variables**
4. Click: **Add New**
5. Fill in:
   - **Key**: `VITE_SUPABASE_PROJECT_ID`
   - **Value**: `your-project-id-here` (paste your Supabase Project ID)
   - **Environments**: Check all three boxes:
     - ☑ Production
     - ☑ Preview  
     - ☑ Development
6. Click: **Save**

---

## Step 3: Redeploy

After setting the environment variable, you need to redeploy:

### Via CLI:
```bash
npx vercel --prod
```

### Via Dashboard:
1. Go to **Deployments** tab
2. Click the **3 dots** on the latest deployment
3. Click **Redeploy**
4. Wait for deployment to complete

---

## Step 4: Verify It Works

1. Visit your live site: https://bizbuilders-automation-s4kxnfv9w-erik-bizbuilders-projects.vercel.app
2. Look for the phone icon in the bottom right corner
3. Click it to open the Voice Agent widget
4. Click **"Start Call"** - it should connect!

---

## Troubleshooting

### Variable Not Working?
- Make sure variable name is exactly: `VITE_SUPABASE_PROJECT_ID` (case-sensitive)
- Verify it's set for all environments (Production, Preview, Development)
- Redeploy after adding the variable
- Check browser console for errors (F12 → Console)

### Can't Find Supabase Project ID?
1. Make sure you're logged into Supabase dashboard
2. Check if you have an active project
3. If not, create a new project at: https://supabase.com/dashboard/new

### Voice Agent Still Not Connecting?
- Verify your Supabase Edge Function is deployed:
  - Function path: `functions/v1/voice-agent`
- Check WebSocket connection in browser console
- Verify Project ID is correct (no spaces, correct format)

---

## Test Locally First (Optional)

Before deploying, test locally:

1. Create `.env.local` file in project root:
```bash
VITE_SUPABASE_PROJECT_ID=your-project-id-here
```

2. Run dev server:
```bash
npm run dev
```

3. Test Voice Agent widget locally at: http://localhost:5173

---

## ✅ Checklist

- [ ] Got Supabase Project ID
- [ ] Added `VITE_SUPABASE_PROJECT_ID` to Vercel
- [ ] Set for all environments (Production, Preview, Development)
- [ ] Redeployed the site
- [ ] Tested Voice Agent widget on live site
- [ ] Verified connection works

---

## 🆘 Need Help?

- **Vercel Docs**: https://vercel.com/docs/concepts/projects/environment-variables
- **Supabase Docs**: https://supabase.com/docs
- **Check deployment logs**: `npx vercel logs` or Vercel Dashboard → Deployments

