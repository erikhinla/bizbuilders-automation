# Content Generation Hub Dashboard

A modern web dashboard for managing AI-powered content generation, integrated into the TransformBy10X.ai hub.

## 🎯 Features

- **Multi-Brand Support**: Switch between TransformBy10X, BizBuilders, and BizBot Marketing
- **Dashboard Overview**: Statistics, recent content, and quick actions
- **Content Queue Management**: View, filter, approve, and publish content
- **Trend Management**: Add trends and generate content from them
- **Settings**: Configure API endpoints and generation settings

## 🚀 Getting Started

### 1. Install Dependencies

```bash
npm install
```

### 2. Start the Backend API

```bash
python content_hub_api.py
```

The API will run on `http://localhost:5000`

### 3. Start the Frontend

```bash
npm run dev
```

The dashboard will be available at `http://localhost:5173/hub/dashboard`

## 📍 Routes

- `/` - Landing page (TransformBy10X homepage)
- `/hub/dashboard` - Main dashboard
- `/hub/content` - Content queue management
- `/hub/trends` - Trend management
- `/hub/settings` - Settings and configuration

## 🎨 Dashboard Features

### Dashboard Page
- Real-time statistics
- Recent content preview
- Quick generation button
- Platform and content type distribution

### Content Queue
- Filter by status (draft, approved, published)
- Search content
- View full content details
- Approve and publish content
- Status management

### Trends Page
- View all trends
- Add new trends manually
- Generate content from trends
- Trend statistics and relevance scores

### Settings
- API configuration
- Generation settings
- API key management

## 🔧 Configuration

### Environment Variables

Create a `.env` file:

```env
VITE_API_URL=http://localhost:5000
VITE_OPENAI_API_KEY=sk-your-key (optional)
```

### API Connection

The dashboard connects to the Flask API at `http://localhost:5000` by default. You can change this in Settings or via the `VITE_API_URL` environment variable.

## 🏗️ Architecture

```
React Dashboard (Frontend)
    ↓
Flask API (content_hub_api.py)
    ↓
Content Generation Hub (content_generation_hub.py)
    ↓
SQLite Database (content_hub.db)
```

## 📱 Multi-Brand Support

The dashboard supports three brands:
- **TransformBy10X** - Purple theme
- **BizBuilders** - Blue theme  
- **BizBot Marketing** - Green theme

Switch between brands using the sidebar selector. Each brand can have its own content and trends.

## 🔐 Security

- API keys stored in localStorage (client-side)
- CORS enabled on Flask API for frontend access
- Environment variables for sensitive configuration

## 🚀 Deployment

### Frontend
Deploy to Vercel/Netlify with:
- Build command: `npm run build`
- Output directory: `dist`
- Environment variables: `VITE_API_URL`

### Backend
Deploy Flask API to any Python host:
- AWS EC2
- DigitalOcean
- Heroku
- Railway

## 📝 Usage

1. **Start Backend**: `python content_hub_api.py`
2. **Start Frontend**: `npm run dev`
3. **Access Dashboard**: Navigate to `/hub/dashboard`
4. **Add Trends**: Go to Trends page and add a trend
5. **Generate Content**: Click "Generate Content" on a trend
6. **Manage Content**: View and approve content in Content Queue
7. **Publish**: Approve and publish content when ready

## 🎯 Next Steps

- Add content editing capabilities
- Integrate with social media APIs for auto-posting
- Add content analytics and performance tracking
- Implement user authentication
- Add content scheduling calendar

