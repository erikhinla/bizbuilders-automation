# Backend API Deployment Guide

## 🚀 Quick Deploy Options

### Option 1: Railway (Easiest - Recommended)

1. **Sign up at**: https://railway.app
2. **Create new project** → "Deploy from GitHub repo"
3. **Select your repo**: `erikhinla/bizbuilders-automation`
4. **Configure**:
   - Root Directory: `/` (or leave default)
   - Build Command: (leave empty - not needed for Python)
   - Start Command: `python content_hub_api.py`
5. **Add Environment Variables**:
   ```
   OPENAI_API_KEY=sk-your-key
   ANTHROPIC_API_KEY=sk-ant-your-key
   PORT=5000
   ```
6. **Deploy** - Railway auto-detects Python and installs dependencies

**Cost**: Free tier available, ~$5/month for production

---

### Option 2: Render

1. **Sign up at**: https://render.com
2. **New** → **Web Service**
3. **Connect GitHub repo**
4. **Configure**:
   - Name: `bizbuilders-content-api`
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python content_hub_api.py`
   - Port: `5000`
5. **Add Environment Variables** (same as above)
6. **Deploy**

**Cost**: Free tier available

---

### Option 3: Heroku

1. **Install Heroku CLI**: https://devcenter.heroku.com/articles/heroku-cli
2. **Login**: `heroku login`
3. **Create app**: 
   ```bash
   cd /Users/erikhowerbush/Documents/bizbuilders/ai-pitch-accelerator/bizbuilders-automation
   heroku create bizbuilders-content-api
   ```
4. **Set environment variables**:
   ```bash
   heroku config:set OPENAI_API_KEY=sk-your-key
   heroku config:set ANTHROPIC_API_KEY=sk-ant-your-key
   ```
5. **Create Procfile**:
   ```bash
   echo "web: python content_hub_api.py" > Procfile
   ```
6. **Deploy**:
   ```bash
   git add Procfile
   git commit -m "Add Procfile"
   git push heroku main
   ```

**Cost**: Free tier discontinued, ~$7/month

---

### Option 4: DigitalOcean App Platform

1. **Sign up at**: https://www.digitalocean.com
2. **Create App** → **GitHub**
3. **Select repo** and configure:
   - Type: Web Service
   - Build Command: `pip install -r requirements.txt`
   - Run Command: `python content_hub_api.py`
   - Port: `5000`
4. **Add Environment Variables**
5. **Deploy**

**Cost**: ~$5/month

---

## 🔧 Update Flask API for Production

The API needs to be updated to work in production. Update `content_hub_api.py`:

```python
# At the bottom, change:
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
```

---

## 📝 Create Procfile (for Heroku/Railway)

Create `Procfile` in root:
```
web: python content_hub_api.py
```

---

## 🔗 Update Frontend API URL

After deploying backend, update frontend environment variable in Vercel:

1. Go to Vercel Dashboard → Your Project → Settings → Environment Variables
2. Add: `VITE_API_URL=https://your-backend-url.com`
3. Redeploy frontend

Or update `src/services/api.js` to use production URL by default.

---

## ✅ Quick Deploy Script

I can create a deployment script for you. Which platform do you prefer?

