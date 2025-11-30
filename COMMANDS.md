# Terminal Commands Reference

## 📁 Root Folder

**All commands must be run from this directory:**
```
/Users/erikhowerbush/Documents/bizbuilders/ai-pitch-accelerator/bizbuilders-automation
```

## 🚀 Quick Navigation

```bash
# Navigate to project root
cd /Users/erikhowerbush/Documents/bizbuilders/ai-pitch-accelerator/bizbuilders-automation

# Or if you're already in a subdirectory, go up to root
cd ~/Documents/bizbuilders/ai-pitch-accelerator/bizbuilders-automation
```

## 📦 Installation Commands

### Install Python Dependencies
```bash
cd /Users/erikhowerbush/Documents/bizbuilders/ai-pitch-accelerator/bizbuilders-automation
pip install -r requirements.txt
```

### Install Node Dependencies
```bash
cd /Users/erikhowerbush/Documents/bizbuilders/ai-pitch-accelerator/bizbuilders-automation
npm install
```

## 🏃 Running Commands

### Start Backend API (Terminal 1)
```bash
cd /Users/erikhowerbush/Documents/bizbuilders/ai-pitch-accelerator/bizbuilders-automation
python content_hub_api.py
```
*Runs on http://localhost:5000*

### Start Frontend Dev Server (Terminal 2)
```bash
cd /Users/erikhowerbush/Documents/bizbuilders/ai-pitch-accelerator/bizbuilders-automation
npm run dev
```
*Runs on http://localhost:5173*

### Build for Production
```bash
cd /Users/erikhowerbush/Documents/bizbuilders/ai-pitch-accelerator/bizbuilders-automation
npm run build
```

## 🧪 Testing Commands

### Test Content Generation
```bash
cd /Users/erikhowerbush/Documents/bizbuilders/ai-pitch-accelerator/bizbuilders-automation
python test_content_generation.py
```

### Test Content Hub
```bash
cd /Users/erikhowerbush/Documents/bizbuilders/ai-pitch-accelerator/bizbuilders-automation
python content_generation_hub.py
```

## 📝 Configuration

### Create Config File
```bash
cd /Users/erikhowerbush/Documents/bizbuilders/ai-pitch-accelerator/bizbuilders-automation
cp config.json.example config.json
# Then edit config.json with your API keys
```

### Set Environment Variables
```bash
export OPENAI_API_KEY="sk-your-key"
export ANTHROPIC_API_KEY="sk-ant-your-key"
export VITE_API_URL="http://localhost:5000"
```

## 🎥 Video Assets

### Add Video Background
```bash
cd /Users/erikhowerbush/Documents/bizbuilders/ai-pitch-accelerator/bizbuilders-automation
# Place your video file here:
# public/videos/background.mp4
```

## 📊 Database

### View Database (if using SQLite browser)
```bash
cd /Users/erikhowerbush/Documents/bizbuilders/ai-pitch-accelerator/bizbuilders-automation
sqlite3 content_hub.db
```

## 🔍 Useful Commands

### Check if ports are in use
```bash
# Check port 5000 (backend)
lsof -i :5000

# Check port 5173 (frontend)
lsof -i :5173
```

### Kill process on port
```bash
# Kill process on port 5000
kill -9 $(lsof -t -i:5000)

# Kill process on port 5173
kill -9 $(lsof -t -i:5173)
```

## 📁 Project Structure

```
/Users/erikhowerbush/Documents/bizbuilders/ai-pitch-accelerator/bizbuilders-automation/
├── src/                    # React source files
├── public/                 # Static assets (videos, images)
├── content_generation_hub.py  # Main Python script
├── content_hub_api.py      # Flask API
├── requirements.txt        # Python dependencies
├── package.json           # Node dependencies
└── config.json            # Configuration (create from .example)
```

## 💡 Pro Tips

1. **Always check you're in the right directory** before running commands
2. **Use two terminals** - one for backend, one for frontend
3. **Check the port** if something isn't working
4. **Video files** go in `public/videos/` directory
5. **Config file** should never be committed to git

