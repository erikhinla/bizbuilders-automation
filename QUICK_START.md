# Quick Start Guide

## 📁 Root Folder Location

**All commands should be run from:**
```
/Users/erikhowerbush/Documents/bizbuilders/ai-pitch-accelerator/bizbuilders-automation
```

Or if you're already in the project directory:
```bash
cd /Users/erikhowerbush/Documents/bizbuilders/ai-pitch-accelerator/bizbuilders-automation
```

## 🚀 Setup Commands

### 1. Install Python Dependencies
```bash
cd /Users/erikhowerbush/Documents/bizbuilders/ai-pitch-accelerator/bizbuilders-automation
pip install -r requirements.txt
```

### 2. Install Node Dependencies
```bash
cd /Users/erikhowerbush/Documents/bizbuilders/ai-pitch-accelerator/bizbuilders-automation
npm install
```

### 3. Start Backend API
```bash
cd /Users/erikhowerbush/Documents/bizbuilders/ai-pitch-accelerator/bizbuilders-automation
python content_hub_api.py
```
*Runs on http://localhost:5000*

### 4. Start Frontend (in a new terminal)
```bash
cd /Users/erikhowerbush/Documents/bizbuilders/ai-pitch-accelerator/bizbuilders-automation
npm run dev
```
*Runs on http://localhost:5173*

## 📍 Access Points

- **Landing Page**: http://localhost:5173/
- **Dashboard**: http://localhost:5173/hub/dashboard
- **API**: http://localhost:5000

## ⚙️ Configuration

Create `config.json` (copy from `config.json.example`):
```bash
cd /Users/erikhowerbush/Documents/bizbuilders/ai-pitch-accelerator/bizbuilders-automation
cp config.json.example config.json
# Then edit config.json with your API keys
```

Or set environment variables:
```bash
export OPENAI_API_KEY="sk-your-key"
export ANTHROPIC_API_KEY="sk-ant-your-key"
```

