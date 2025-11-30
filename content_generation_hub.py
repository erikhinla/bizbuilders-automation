#!/usr/bin/env python3
"""
Content Generation Automation Hub
AI-powered content generation system that automatically creates content from trends
"""

import os
import json
import time
import datetime
import sqlite3
import schedule
import threading
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
import requests

# Try to import OpenAI, fallback to requests if not available
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("⚠️ OpenAI library not installed. Install with: pip install openai")

@dataclass
class ContentPiece:
    """Data class for content pieces"""
    id: str
    title: str
    content: str
    content_type: str  # blog, social_post, email, etc.
    platform: str  # twitter, linkedin, facebook, blog, etc.
    status: str  # draft, approved, scheduled, published
    created_at: str
    scheduled_for: Optional[str] = None
    published_at: Optional[str] = None
    engagement_metrics: Optional[Dict[str, int]] = None
    seo_keywords: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class TrendData:
    """Data class for trend information"""
    keyword: str
    volume: int
    growth_rate: float
    platform: str
    timestamp: str
    relevance_score: float
    source: str  # twitter, google_trends, reddit, etc.

class ContentGenerationHub:
    def __init__(self, db_path: str = "content_hub.db", config_path: str = "config.json"):
        """Initialize the content generation hub"""
        self.db_path = db_path
        self.config_path = config_path
        self.config = self.load_config()
        self.init_database()
        self.running = False
        
        # Initialize AI client if available
        self.ai_client = None
        if OPENAI_AVAILABLE and self.config.get('openai_api_key'):
            self.ai_client = OpenAI(api_key=self.config.get('openai_api_key'))
        elif self.config.get('openai_api_key'):
            print("⚠️ OpenAI API key configured but library not installed")
        
        # Content generation settings
        self.content_settings = {
            'transformby10x': {
                'tone': 'professional, authoritative, data-driven',
                'target_audience': 'business owners, entrepreneurs, executives',
                'content_themes': ['AI transformation', 'business automation', '10x growth', 'productivity'],
                'brand_voice': 'TransformBy10X helps businesses achieve exponential growth through AI-powered automation'
            },
            'bizbuilders': {
                'tone': 'inspirational, practical, community-focused',
                'target_audience': 'entrepreneurs, startup founders, business builders',
                'content_themes': ['entrepreneurship', 'business building', 'startup tools', 'business development'],
                'brand_voice': 'BizBuilders empowers entrepreneurs to build successful businesses'
            }
        }
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file or environment"""
        config = {
            'openai_api_key': os.getenv('OPENAI_API_KEY', ''),
            'anthropic_api_key': os.getenv('ANTHROPIC_API_KEY', ''),
            'content_generation_enabled': True,
            'auto_schedule_enabled': False,
            'default_platform': 'transformby10x',
            'generation_interval_hours': 2,
            'max_content_per_cycle': 5,
            'min_relevance_score': 0.7
        }
        
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    file_config = json.load(f)
                    config.update(file_config)
            except Exception as e:
                print(f"⚠️ Error loading config: {e}")
        
        return config
    
    def save_config(self):
        """Save configuration to file"""
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def init_database(self):
        """Initialize SQLite database for content management"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Content pieces table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS content_pieces (
                id TEXT PRIMARY KEY,
                title TEXT,
                content TEXT,
                content_type TEXT,
                platform TEXT,
                status TEXT,
                created_at DATETIME,
                scheduled_for DATETIME,
                published_at DATETIME,
                engagement_metrics TEXT,
                seo_keywords TEXT,
                metadata TEXT
            )
        ''')
        
        # Trends table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trends (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword TEXT,
                volume INTEGER,
                growth_rate REAL,
                platform TEXT,
                timestamp DATETIME,
                relevance_score REAL,
                source TEXT
            )
        ''')
        
        # Generation logs
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS generation_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                action TEXT,
                status TEXT,
                details TEXT,
                timestamp DATETIME
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def generate_content_with_ai(self, topic: str, content_type: str, platform: str, 
                                 brand_config: Dict[str, Any]) -> Dict[str, str]:
        """Generate content using AI (OpenAI or Anthropic)"""
        
        if not self.ai_client and not self.config.get('anthropic_api_key'):
            # Fallback to template-based generation
            return self._generate_template_content(topic, content_type, platform, brand_config)
        
        # Build prompt based on content type
        if content_type == 'blog_post':
            prompt = self._build_blog_prompt(topic, brand_config)
        elif content_type == 'social_post':
            prompt = self._build_social_prompt(topic, platform, brand_config)
        elif content_type == 'email':
            prompt = self._build_email_prompt(topic, brand_config)
        else:
            prompt = self._build_generic_prompt(topic, content_type, platform, brand_config)
        
        try:
            if self.ai_client:
                # Use OpenAI
                response = self.ai_client.chat.completions.create(
                    model=self.config.get('openai_model', 'gpt-4'),
                    messages=[
                        {"role": "system", "content": "You are an expert content writer specializing in business, AI, and entrepreneurship."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=2000
                )
                generated_text = response.choices[0].message.content
            elif self.config.get('anthropic_api_key'):
                # Use Anthropic Claude
                headers = {
                    "x-api-key": self.config['anthropic_api_key'],
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json"
                }
                data = {
                    "model": "claude-3-sonnet-20240229",
                    "max_tokens": 2000,
                    "messages": [
                        {"role": "user", "content": prompt}
                    ]
                }
                response = requests.post(
                    "https://api.anthropic.com/v1/messages",
                    headers=headers,
                    json=data
                )
                if response.status_code == 200:
                    generated_text = response.json()['content'][0]['text']
                else:
                    raise Exception(f"Anthropic API error: {response.status_code}")
            else:
                raise Exception("No AI service configured")
            
            # Parse generated content
            return self._parse_ai_response(generated_text, content_type)
            
        except Exception as e:
            print(f"❌ AI generation failed: {e}")
            # Fallback to template
            return self._generate_template_content(topic, content_type, platform, brand_config)
    
    def _build_blog_prompt(self, topic: str, brand_config: Dict[str, Any]) -> str:
        """Build prompt for blog post generation"""
        return f"""Write a comprehensive blog post about: {topic}

Brand Voice: {brand_config.get('brand_voice', '')}
Tone: {brand_config.get('tone', 'professional')}
Target Audience: {brand_config.get('target_audience', 'business professionals')}

Requirements:
- Compelling headline
- Introduction that hooks the reader
- 3-5 main sections with actionable insights
- Conclusion with clear call-to-action
- SEO-optimized with relevant keywords
- 800-1200 words

Format your response as JSON:
{{
    "title": "Blog post title",
    "content": "Full blog post content with sections",
    "excerpt": "Short excerpt for preview",
    "keywords": ["keyword1", "keyword2", "keyword3"]
}}"""
    
    def _build_social_prompt(self, topic: str, platform: str, brand_config: Dict[str, Any]) -> str:
        """Build prompt for social media post generation"""
        platform_limits = {
            'twitter': 280,
            'linkedin': 3000,
            'facebook': 5000,
            'instagram': 2200
        }
        char_limit = platform_limits.get(platform, 500)
        
        return f"""Write a {platform} post about: {topic}

Brand Voice: {brand_config.get('brand_voice', '')}
Tone: {brand_config.get('tone', 'professional')}
Character Limit: {char_limit} characters
Platform: {platform}

Requirements:
- Engaging hook in first line
- Value-driven content
- Clear call-to-action
- Relevant hashtags (3-5)
- Platform-appropriate formatting

Format your response as JSON:
{{
    "content": "Post content",
    "hashtags": ["#hashtag1", "#hashtag2"],
    "title": "Short title for reference"
}}"""
    
    def _build_email_prompt(self, topic: str, brand_config: Dict[str, Any]) -> str:
        """Build prompt for email generation"""
        return f"""Write a marketing email about: {topic}

Brand Voice: {brand_config.get('brand_voice', '')}
Tone: {brand_config.get('tone', 'professional')}

Requirements:
- Compelling subject line
- Personal greeting
- Clear value proposition
- 2-3 key points
- Strong call-to-action
- Professional closing

Format your response as JSON:
{{
    "subject": "Email subject line",
    "content": "Email body content",
    "preview_text": "Preview text"
}}"""
    
    def _build_generic_prompt(self, topic: str, content_type: str, platform: str, 
                             brand_config: Dict[str, Any]) -> str:
        """Build generic prompt for other content types"""
        return f"""Write {content_type} content about: {topic}

Brand Voice: {brand_config.get('brand_voice', '')}
Tone: {brand_config.get('tone', 'professional')}
Platform: {platform}

Create engaging, valuable content that resonates with the target audience.

Format your response as JSON with appropriate fields."""
    
    def _parse_ai_response(self, response_text: str, content_type: str) -> Dict[str, str]:
        """Parse AI response into structured content"""
        try:
            # Try to extract JSON from response
            if '{' in response_text and '}' in response_text:
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                json_str = response_text[json_start:json_end]
                parsed = json.loads(json_str)
                return parsed
        except:
            pass
        
        # Fallback: return as-is
        return {
            'content': response_text,
            'title': response_text.split('\n')[0][:100] if '\n' in response_text else response_text[:100]
        }
    
    def _generate_template_content(self, topic: str, content_type: str, platform: str,
                                  brand_config: Dict[str, Any]) -> Dict[str, str]:
        """Generate template-based content as fallback"""
        if content_type == 'social_post':
            content = f"🚀 {topic}\n\nDiscover how this trend is transforming businesses. Key insights and actionable strategies for growth.\n\n#BusinessGrowth #AI #Automation"
            return {
                'content': content,
                'hashtags': ['#BusinessGrowth', '#AI', '#Automation'],
                'title': f"Post about {topic}"
            }
        elif content_type == 'blog_post':
            return {
                'title': f"How {topic} is Transforming Business",
                'content': f"# {topic}\n\n## Introduction\n\n{topic} represents a significant opportunity for business transformation...",
                'excerpt': f"Discover how {topic} is revolutionizing business operations.",
                'keywords': [topic.lower().replace(' ', '-')]
            }
        else:
            return {
                'content': f"Content about {topic}",
                'title': f"{content_type} about {topic}"
            }
    
    def generate_content_from_trend(self, trend: TrendData, content_types: List[str] = None) -> List[ContentPiece]:
        """Generate content pieces from a trend"""
        if content_types is None:
            content_types = ['social_post', 'blog_post']
        
        brand_config = self.content_settings.get(trend.platform, self.content_settings['transformby10x'])
        content_pieces = []
        
        for content_type in content_types:
            # Determine platform for social posts
            if content_type == 'social_post':
                platforms = ['twitter', 'linkedin']
            else:
                platforms = [trend.platform]
            
            for platform in platforms:
                # Generate content with AI
                generated = self.generate_content_with_ai(
                    topic=trend.keyword,
                    content_type=content_type,
                    platform=platform,
                    brand_config=brand_config
                )
                
                # Create content piece
                content_id = f"{content_type}_{platform}_{int(time.time())}_{hash(trend.keyword) % 10000}"
                
                content_piece = ContentPiece(
                    id=content_id,
                    title=generated.get('title', f"{content_type} about {trend.keyword}"),
                    content=generated.get('content', ''),
                    content_type=content_type,
                    platform=platform,
                    status='draft',
                    created_at=datetime.datetime.now().isoformat(),
                    seo_keywords=generated.get('keywords', [trend.keyword]),
                    metadata={
                        'trend_keyword': trend.keyword,
                        'trend_score': trend.relevance_score,
                        'hashtags': generated.get('hashtags', []),
                        'excerpt': generated.get('excerpt', '')
                    }
                )
                
                content_pieces.append(content_piece)
        
        return content_pieces
    
    def save_content_piece(self, content: ContentPiece):
        """Save content piece to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO content_pieces 
            (id, title, content, content_type, platform, status, created_at, 
             scheduled_for, published_at, engagement_metrics, seo_keywords, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            content.id, content.title, content.content, content.content_type,
            content.platform, content.status, content.created_at,
            content.scheduled_for, content.published_at,
            json.dumps(content.engagement_metrics) if content.engagement_metrics else None,
            json.dumps(content.seo_keywords) if content.seo_keywords else None,
            json.dumps(content.metadata) if content.metadata else None
        ))
        
        conn.commit()
        conn.close()
    
    def get_trends_from_database(self, limit: int = 10) -> List[TrendData]:
        """Get recent trends from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT keyword, volume, growth_rate, platform, timestamp, relevance_score, source
            FROM trends
            WHERE relevance_score >= ?
            ORDER BY relevance_score DESC, timestamp DESC
            LIMIT ?
        ''', (self.config.get('min_relevance_score', 0.7), limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        trends = []
        for row in rows:
            trends.append(TrendData(
                keyword=row[0],
                volume=row[1],
                growth_rate=row[2],
                platform=row[3],
                timestamp=row[4],
                relevance_score=row[5],
                source=row[6]
            ))
        
        return trends
    
    def add_trend(self, trend: TrendData):
        """Add a trend to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO trends 
            (keyword, volume, growth_rate, platform, timestamp, relevance_score, source)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            trend.keyword, trend.volume, trend.growth_rate,
            trend.platform, trend.timestamp, trend.relevance_score, trend.source
        ))
        
        conn.commit()
        conn.close()
    
    def run_content_generation_cycle(self):
        """Run a complete content generation cycle"""
        print("\n🚀 Starting content generation cycle...")
        print("=" * 60)
        
        try:
            # Get trends
            trends = self.get_trends_from_database(limit=self.config.get('max_content_per_cycle', 5))
            print(f"📊 Found {len(trends)} relevant trends")
            
            if not trends:
                print("⚠️ No trends found. Add trends to the database first.")
                self.log_action("generation_cycle", "warning", "No trends available")
                return
            
            total_generated = 0
            
            for trend in trends:
                print(f"\n📝 Generating content for: {trend.keyword} (score: {trend.relevance_score:.2f})")
                
                # Generate content
                content_pieces = self.generate_content_from_trend(trend)
                
                # Save content pieces
                for piece in content_pieces:
                    self.save_content_piece(piece)
                    total_generated += 1
                    print(f"  ✅ Generated {piece.content_type} for {piece.platform}: {piece.title[:50]}...")
                
                # Rate limiting
                time.sleep(1)
            
            print(f"\n🎉 Generation cycle complete! Generated {total_generated} content pieces")
            self.log_action("generation_cycle", "success", f"Generated {total_generated} pieces from {len(trends)} trends")
            
        except Exception as e:
            print(f"❌ Generation cycle failed: {e}")
            self.log_action("generation_cycle", "error", str(e))
    
    def log_action(self, action: str, status: str, details: str = ""):
        """Log an action to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO generation_logs (action, status, details, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (action, status, details, datetime.datetime.now()))
        
        conn.commit()
        conn.close()
    
    def get_content_queue(self, status: str = None, limit: int = 50) -> List[ContentPiece]:
        """Get content from queue"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if status:
            cursor.execute('''
                SELECT id, title, content, content_type, platform, status, created_at,
                       scheduled_for, published_at, engagement_metrics, seo_keywords, metadata
                FROM content_pieces
                WHERE status = ?
                ORDER BY created_at DESC
                LIMIT ?
            ''', (status, limit))
        else:
            cursor.execute('''
                SELECT id, title, content, content_type, platform, status, created_at,
                       scheduled_for, published_at, engagement_metrics, seo_keywords, metadata
                FROM content_pieces
                ORDER BY created_at DESC
                LIMIT ?
            ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        content_pieces = []
        for row in rows:
            content_pieces.append(ContentPiece(
                id=row[0],
                title=row[1],
                content=row[2],
                content_type=row[3],
                platform=row[4],
                status=row[5],
                created_at=row[6],
                scheduled_for=row[7],
                published_at=row[8],
                engagement_metrics=json.loads(row[9]) if row[9] else None,
                seo_keywords=json.loads(row[10]) if row[10] else None,
                metadata=json.loads(row[11]) if row[11] else None
            ))
        
        return content_pieces
    
    def start_scheduled_generation(self):
        """Start scheduled content generation"""
        interval = self.config.get('generation_interval_hours', 2)
        schedule.every(interval).hours.do(self.run_content_generation_cycle)
        
        self.running = True
        print(f"⏰ Scheduled content generation every {interval} hours")
        
        while self.running:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    def stop_scheduled_generation(self):
        """Stop scheduled generation"""
        self.running = False
        print("🛑 Scheduled generation stopped")

def main():
    """Main function"""
    print("🤖 Content Generation Automation Hub")
    print("=" * 60)
    
    hub = ContentGenerationHub()
    
    # Check configuration
    if not hub.config.get('openai_api_key') and not hub.config.get('anthropic_api_key'):
        print("\n⚠️ No AI API key configured!")
        print("Set OPENAI_API_KEY or ANTHROPIC_API_KEY environment variable")
        print("Or add 'openai_api_key' or 'anthropic_api_key' to config.json")
        print("\nYou can still use template-based generation, but AI generation requires an API key.")
    
    # Add sample trend for testing
    sample_trend = TrendData(
        keyword="AI-powered business automation",
        volume=5000,
        growth_rate=0.25,
        platform="transformby10x",
        timestamp=datetime.datetime.now().isoformat(),
        relevance_score=0.85,
        source="manual"
    )
    hub.add_trend(sample_trend)
    print(f"\n✅ Added sample trend: {sample_trend.keyword}")
    
    # Run generation cycle
    print("\n🚀 Running content generation cycle...")
    hub.run_content_generation_cycle()
    
    # Show generated content
    print("\n📋 Generated Content Queue:")
    content_queue = hub.get_content_queue(limit=10)
    for content in content_queue:
        print(f"  - [{content.status}] {content.content_type} for {content.platform}: {content.title}")

if __name__ == "__main__":
    main()

