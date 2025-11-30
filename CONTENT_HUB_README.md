# Content Generation Automation Hub

AI-powered content generation system that automatically creates content from trends and topics.

## 🎯 Features

- **AI-Powered Content Generation**: Uses OpenAI GPT-4 or Anthropic Claude to generate high-quality content
- **Multi-Platform Support**: Generates content for Twitter, LinkedIn, Facebook, blogs, and emails
- **Trend-Based Generation**: Automatically generates content from trending topics
- **Content Queue Management**: Organize and manage generated content
- **REST API**: Full API for integration with other systems
- **Scheduled Generation**: Automatically generate content on a schedule

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Keys

Create a `config.json` file (or copy from `config.json.example`):

```json
{
  "openai_api_key": "sk-your-openai-key",
  "anthropic_api_key": "sk-ant-your-anthropic-key",
  "openai_model": "gpt-4",
  "generation_interval_hours": 2,
  "max_content_per_cycle": 5
}
```

Or set environment variables:
```bash
export OPENAI_API_KEY="sk-your-key"
export ANTHROPIC_API_KEY="sk-ant-your-key"
```

### 3. Run Content Generation

**Command Line:**
```bash
python content_generation_hub.py
```

**API Server:**
```bash
python content_hub_api.py
```

The API will be available at `http://localhost:5000`

## 📖 Usage

### Generate Content from Trends

```python
from content_generation_hub import ContentGenerationHub, TrendData
import datetime

hub = ContentGenerationHub()

# Add a trend
trend = TrendData(
    keyword="AI-powered business automation",
    volume=5000,
    growth_rate=0.25,
    platform="transformby10x",
    timestamp=datetime.datetime.now().isoformat(),
    relevance_score=0.85,
    source="manual"
)
hub.add_trend(trend)

# Generate content
content_pieces = hub.generate_content_from_trend(trend, content_types=['social_post', 'blog_post'])

# Save content
for piece in content_pieces:
    hub.save_content_piece(piece)
```

### Using the API

**Add a trend:**
```bash
curl -X POST http://localhost:5000/api/trends \
  -H "Content-Type: application/json" \
  -d '{
    "keyword": "AI automation trends",
    "volume": 5000,
    "growth_rate": 0.25,
    "platform": "transformby10x",
    "relevance_score": 0.85
  }'
```

**Generate content:**
```bash
curl -X POST http://localhost:5000/api/content/generate \
  -H "Content-Type: application/json" \
  -d '{
    "keyword": "AI automation trends",
    "content_types": ["social_post", "blog_post"],
    "platform": "transformby10x"
  }'
```

**Get content queue:**
```bash
curl http://localhost:5000/api/content?status=draft
```

**Run generation cycle:**
```bash
curl -X POST http://localhost:5000/api/generate/cycle
```

## 🔧 Configuration

### Content Settings

The hub supports different brand configurations:

- **transformby10x**: Professional, authoritative, data-driven
- **bizbuilders**: Inspirational, practical, community-focused

### Content Types

- `social_post`: Social media posts (Twitter, LinkedIn, Facebook)
- `blog_post`: Full blog articles
- `email`: Marketing emails

### Platforms

- `twitter`: 280 character limit
- `linkedin`: 3000 character limit
- `facebook`: 5000 character limit
- `instagram`: 2200 character limit

## 📊 Database

Content is stored in SQLite database (`content_hub.db`):

- **content_pieces**: Generated content
- **trends**: Trend data
- **generation_logs**: Generation history

## 🔄 Scheduled Generation

Start scheduled generation:

```python
hub = ContentGenerationHub()
hub.start_scheduled_generation()  # Runs every 2 hours by default
```

## 📡 API Endpoints

- `GET /api/health` - Health check
- `GET /api/trends` - Get trends
- `POST /api/trends` - Add trend
- `GET /api/content` - Get content queue
- `POST /api/content/generate` - Generate content
- `GET /api/content/<id>` - Get specific content
- `PUT /api/content/<id>/status` - Update content status
- `POST /api/generate/cycle` - Run generation cycle
- `GET /api/stats` - Get statistics

## 🎨 Content Generation

The hub uses AI to generate:

1. **Blog Posts**: 800-1200 word articles with SEO optimization
2. **Social Posts**: Platform-optimized posts with hashtags
3. **Emails**: Marketing emails with subject lines

All content is:
- Brand-voice aligned
- SEO optimized
- Platform-specific
- Action-oriented

## 🔐 Security

- Store API keys in environment variables or `config.json` (not in git)
- Use `.gitignore` to exclude `config.json` and `*.db` files
- API supports CORS for frontend integration

## 📝 Example Workflow

1. **Add trends** (manually or from trend monitoring)
2. **Run generation cycle** (automatically or manually)
3. **Review generated content** in queue
4. **Approve/publish** content
5. **Track engagement** metrics

## 🚀 Next Steps

- Integrate with social media APIs for auto-posting
- Add image generation for visual content
- Connect to Notion/Activepieces for workflow automation
- Add content analytics and performance tracking

