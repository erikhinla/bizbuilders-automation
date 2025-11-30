# ⚡ Quick Environment Variable Setup

## Option 1: Interactive Script (Easiest) ✅

Just run this command and follow the prompts:

```bash
./setup-env.sh
```

The script will:
1. Ask for your Supabase Project ID
2. Set it for all environments (Production, Preview, Development)
3. Optionally redeploy your site

---

## Option 2: Manual CLI Setup

If you prefer to do it manually:

```bash
# Add the environment variable
npx vercel env add VITE_SUPABASE_PROJECT_ID production preview development

# When prompted, paste your Supabase Project ID

# Redeploy
npx vercel --prod
```

---

## Option 3: Via Vercel Dashboard

1. Go to: https://vercel.com/dashboard
2. Click on: **bizbuilders-automation**
3. Go to: **Settings** → **Environment Variables**
4. Click: **Add New**
5. Fill in:
   - **Key**: `VITE_SUPABASE_PROJECT_ID`
   - **Value**: Your Supabase Project ID
   - **Environments**: Check all three (Production, Preview, Development)
6. Click: **Save**
7. Go to **Deployments** tab → Click **Redeploy** on latest deployment

---

## 🆔 How to Get Your Supabase Project ID

### Method 1: From Dashboard
1. Go to: https://supabase.com/dashboard
2. Select your project
3. Go to **Settings** → **General**
4. Find **Reference ID** - that's your Project ID

### Method 2: From URL
Your Supabase URL looks like: `https://abcdefghijklmnop.supabase.co`
The Project ID is: `abcdefghijklmnop` (the part before `.supabase.co`)

---

## ✅ After Setup

1. ✅ Environment variable is set
2. ✅ Site is redeployed
3. ✅ Test the Voice Agent widget:
   - Visit your site
   - Click the phone icon (bottom right)
   - Click "Start Call"
   - It should connect!

---

## 🐛 Troubleshooting

**Variable not working?**
- Make sure it's set for all environments (Production, Preview, Development)
- Redeploy after adding the variable
- Check browser console for errors (F12)

**Can't find Supabase Project ID?**
- Make sure you're logged into Supabase
- Create a project if you don't have one: https://supabase.com/dashboard/new
- The Project ID is visible in your project settings

