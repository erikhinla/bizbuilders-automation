# Tech Stack Overview

## 🎯 Content Generation Hub

### Backend (Python)

**Core Language:**
- **Python 3.8+** - Main programming language

**AI/ML Libraries:**
- **OpenAI SDK** (`openai>=1.0.0`) - GPT-4, GPT-3.5 for content generation
- **Anthropic API** (via `requests`) - Claude AI as alternative to OpenAI

**Web Framework:**
- **Flask 3.0+** - REST API server
- **Flask-CORS 4.0+** - Cross-origin resource sharing for frontend integration

**Database:**
- **SQLite3** (built-in) - Lightweight database for content, trends, and logs
  - No additional installation needed
  - File-based, easy to backup and migrate

**Task Scheduling:**
- **Schedule** (`schedule>=1.2.0`) - Python job scheduling for automated content generation

**HTTP Client:**
- **Requests** (`requests>=2.31.0`) - HTTP library for API calls (Anthropic, webhooks, etc.)

**Standard Library:**
- `dataclasses` - Data structures for content pieces and trends
- `typing` - Type hints for better code quality
- `json` - JSON serialization
- `datetime` - Date/time handling
- `threading` - Background task execution

---

## 🎨 Frontend (React)

**Framework:**
- **React 18.2+** - UI library
- **React DOM 18.2+** - React rendering

**Build Tool:**
- **Vite 5.0+** - Fast build tool and dev server
- **@vitejs/plugin-react** - React plugin for Vite

**Styling:**
- **Tailwind CSS 3.4+** - Utility-first CSS framework
- **PostCSS 8.4+** - CSS processing
- **Autoprefixer 10.4+** - Automatic vendor prefixes

**UI Components:**
- **Lucide React** - Icon library
- **Framer Motion 10.16+** - Animation library
- **React Helmet Async 2.0+** - SEO meta tag management

**Utilities:**
- **clsx 2.0+** - Conditional className utility

**TypeScript Support:**
- **@types/react** - TypeScript definitions for React
- **@types/react-dom** - TypeScript definitions for React DOM

---

## 🗄️ Data Storage

**Primary Database:**
- **SQLite3** - File-based relational database
  - `content_hub.db` - Main content database
  - Stores: content pieces, trends, generation logs

**Configuration:**
- **JSON** - Configuration files (`config.json`)
- **Environment Variables** - API keys and secrets

---

## 🔌 APIs & Integrations

**AI Services:**
- **OpenAI API** - GPT-4, GPT-3.5 for content generation
- **Anthropic API** - Claude (Sonnet) as alternative

**REST API:**
- **Flask REST API** - Custom API endpoints
  - Content management
  - Trend management
  - Generation triggers
  - Statistics

**Future Integrations (from existing code):**
- **Notion API** - Content hub integration
- **Activepieces** - Workflow automation
- **Postiz API** - Social media publishing
- **Twitter/X API** - Trend monitoring
- **Webhooks** - n8n, Activepieces integration

---

## 🛠️ Development Tools

**Python:**
- Standard library modules
- Virtual environment support (`venv/`)

**Node.js:**
- **npm** - Package manager
- **Node 18+** - Runtime for frontend build

**Version Control:**
- **Git** - Source control

---

## 📦 Deployment

**Frontend:**
- **Vercel** - React app hosting (configured)
- **Netlify** - Alternative hosting option
- **Cloudflare Pages** - Alternative hosting option
- **Static hosting** - Any static file host

**Backend:**
- **Python 3.8+** required
- Can run on:
  - Local machine
  - Cloud servers (AWS EC2, DigitalOcean, Linode)
  - Docker containers
  - Serverless (with modifications)

**Database:**
- **SQLite3** - File-based (easy to backup)
- Can migrate to PostgreSQL/MySQL if needed

---

## 🔐 Security & Configuration

**Environment Management:**
- Environment variables (`.env`)
- JSON configuration files
- API key management

**Security:**
- CORS enabled for API
- API key authentication
- `.gitignore` configured for secrets

---

## 📊 Architecture Summary

```
┌─────────────────────────────────────────┐
│         Frontend (React + Vite)         │
│  - React 18                             │
│  - Tailwind CSS                         │
│  - Vite Build Tool                      │
└──────────────┬──────────────────────────┘
               │ HTTP/REST
┌──────────────▼──────────────────────────┐
│      API Server (Flask)                 │
│  - Flask 3.0                            │
│  - Flask-CORS                           │
│  - REST Endpoints                       │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│   Content Generation Hub (Python)       │
│  - OpenAI/Anthropic Integration         │
│  - Content Generation Logic             │
│  - Schedule Management                  │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│      Database (SQLite3)                 │
│  - Content Pieces                       │
│  - Trends                               │
│  - Generation Logs                      │
└─────────────────────────────────────────┘
```

---

## 🚀 Quick Tech Stack Summary

**Backend:**
- Python 3.8+
- Flask (API)
- SQLite3 (Database)
- OpenAI/Anthropic (AI)
- Schedule (Automation)

**Frontend:**
- React 18
- Vite
- Tailwind CSS
- Framer Motion

**Deployment:**
- Vercel (Frontend)
- Any Python host (Backend)
- SQLite (Database)

---

## 📝 Installation Requirements

**Python:**
```bash
pip install -r requirements.txt
```

**Node.js:**
```bash
npm install
```

**System Requirements:**
- Python 3.8 or higher
- Node.js 18 or higher
- 100MB+ disk space
- Internet connection (for AI APIs)

---

This is a modern, lightweight stack that's easy to deploy and scale!

