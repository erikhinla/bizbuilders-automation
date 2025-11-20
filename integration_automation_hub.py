#!/usr/bin/env python3
"""
Integration and Automation Hub
Comprehensive system to integrate trend monitoring, websites, and social media automation
"""

import os
import json
import time
import datetime
import requests
import sqlite3
import schedule
import threading
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
import subprocess

@dataclass
class ContentPiece:
    """Data class for content pieces"""
    id: str
    title: str
    content: str
    platform: str
    status: str
    created_at: str
    scheduled_for: Optional[str] = None
    engagement_metrics: Optional[Dict[str, int]] = None
    seo_keywords: Optional[List[str]] = None

@dataclass
class TrendData:
    """Data class for trend information"""
    keyword: str
    volume: int
    growth_rate: float
    platform: str
    timestamp: str
    relevance_score: float

@dataclass
class WebsiteMetrics:
    """Data class for website performance metrics"""
    url: str
    page_views: int
    conversion_rate: float
    bounce_rate: float
    avg_session_duration: float
    timestamp: str

class IntegrationHub:
    def __init__(self, db_path: str = "/home/ubuntu/integration_hub.db"):
        """Initialize the integration hub"""
        self.db_path = db_path
        self.init_database()
        self.running = False
        
        # Configuration for different platforms
        self.platforms = {
            'transformby10x': {
                'website_url': 'https://transformby10x.ai',
                'local_url': 'http://localhost:5173',
                'keywords': ['AI transformation', 'business automation', '10x growth'],
                'content_themes': ['productivity', 'automation', 'AI tools', 'business growth']
            },
            'bizbuilders': {
                'website_url': 'https://bizbuilders.ai',
                'local_url': 'http://localhost:5174',
                'keywords': ['business building', 'entrepreneur tools', 'startup automation'],
                'content_themes': ['entrepreneurship', 'business creation', 'startup tools', 'business development']
            }
        }
        
    def init_database(self):
        """Initialize SQLite database for integration data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Content management table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS content_queue (
                id TEXT PRIMARY KEY,
                title TEXT,
                content TEXT,
                platform TEXT,
                status TEXT,
                created_at DATETIME,
                scheduled_for DATETIME,
                engagement_metrics TEXT,
                seo_keywords TEXT
            )
        ''')
        
        # Trend tracking table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trend_tracking (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword TEXT,
                volume INTEGER,
                growth_rate REAL,
                platform TEXT,
                timestamp DATETIME,
                relevance_score REAL
            )
        ''')
        
        # Website metrics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS website_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT,
                page_views INTEGER,
                conversion_rate REAL,
                bounce_rate REAL,
                avg_session_duration REAL,
                timestamp DATETIME
            )
        ''')
        
        # Automation logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS automation_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                action TEXT,
                platform TEXT,
                status TEXT,
                details TEXT,
                timestamp DATETIME
            )
        ''')
        
        # Integration status table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS integration_status (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                service_name TEXT,
                status TEXT,
                last_check DATETIME,
                error_message TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def log_automation_action(self, action: str, platform: str, status: str, details: str = ""):
        """Log automation actions to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO automation_logs (action, platform, status, details, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (action, platform, status, details, datetime.datetime.now()))
        
        conn.commit()
        conn.close()
    
    def update_integration_status(self, service_name: str, status: str, error_message: str = ""):
        """Update integration status for a service"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO integration_status 
            (service_name, status, last_check, error_message)
            VALUES (?, ?, ?, ?)
        ''', (service_name, status, datetime.datetime.now(), error_message))
        
        conn.commit()
        conn.close()
    
    def collect_trend_data(self) -> List[TrendData]:
        """Collect trend data from the trend monitoring system"""
        print("📊 Collecting trend data...")
        
        trend_data = []
        
        try:
            # Read trend analysis results
            trend_file = "/home/ubuntu/trend_analysis_results.json"
            if os.path.exists(trend_file):
                with open(trend_file, 'r') as f:
                    data = json.load(f)
                    
                for platform, platform_data in self.platforms.items():
                    for keyword in platform_data['keywords']:
                        # Simulate trend data (in real implementation, this would come from APIs)
                        trend = TrendData(
                            keyword=keyword,
                            volume=1000 + hash(keyword) % 5000,
                            growth_rate=0.1 + (hash(keyword) % 100) / 1000,
                            platform=platform,
                            timestamp=datetime.datetime.now().isoformat(),
                            relevance_score=0.7 + (hash(keyword) % 30) / 100
                        )
                        trend_data.append(trend)
            
            self.update_integration_status("trend_monitoring", "active")
            self.log_automation_action("collect_trends", "all", "success", f"Collected {len(trend_data)} trends")
            
        except Exception as e:
            self.update_integration_status("trend_monitoring", "error", str(e))
            self.log_automation_action("collect_trends", "all", "error", str(e))
        
        return trend_data
    
    def save_trend_data(self, trends: List[TrendData]):
        """Save trend data to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for trend in trends:
            cursor.execute('''
                INSERT INTO trend_tracking 
                (keyword, volume, growth_rate, platform, timestamp, relevance_score)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (trend.keyword, trend.volume, trend.growth_rate, 
                  trend.platform, trend.timestamp, trend.relevance_score))
        
        conn.commit()
        conn.close()
    
    def generate_content_from_trends(self, trends: List[TrendData]) -> List[ContentPiece]:
        """Generate content pieces based on trending topics"""
        print("✍️ Generating content from trends...")
        
        content_pieces = []
        
        for trend in trends[:5]:  # Top 5 trends
            if trend.relevance_score > 0.8:
                content_id = f"content_{int(time.time())}_{hash(trend.keyword) % 1000}"
                
                # Generate content based on trend and platform
                platform_config = self.platforms.get(trend.platform, {})
                themes = platform_config.get('content_themes', [])
                
                if trend.platform == 'transformby10x':
                    title = f"How {trend.keyword} Can Transform Your Business Operations"
                    content = f"""Discover how {trend.keyword} is revolutionizing business operations. 
                    With a {trend.growth_rate:.1%} growth rate and {trend.volume:,} searches, 
                    this trend represents a massive opportunity for business transformation.
                    
                    Key benefits:
                    • Increased efficiency through automation
                    • Scalable business processes
                    • Competitive advantage in the market
                    
                    Ready to transform your business? Learn more about our AI-powered solutions."""
                    
                elif trend.platform == 'bizbuilders':
                    title = f"Building Your Business with {trend.keyword}"
                    content = f"""Entrepreneurs are leveraging {trend.keyword} to build successful businesses. 
                    With {trend.volume:,} people searching for this topic and {trend.growth_rate:.1%} growth, 
                    now is the perfect time to capitalize on this opportunity.
                    
                    How to get started:
                    • Identify market opportunities
                    • Build automated systems
                    • Scale your operations
                    
                    Join thousands of successful entrepreneurs using our platform."""
                
                content_piece = ContentPiece(
                    id=content_id,
                    title=title,
                    content=content,
                    platform=trend.platform,
                    status="draft",
                    created_at=datetime.datetime.now().isoformat(),
                    seo_keywords=[trend.keyword] + platform_config.get('keywords', [])
                )
                
                content_pieces.append(content_piece)
        
        return content_pieces
    
    def save_content_pieces(self, content_pieces: List[ContentPiece]):
        """Save content pieces to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for content in content_pieces:
            cursor.execute('''
                INSERT OR REPLACE INTO content_queue 
                (id, title, content, platform, status, created_at, scheduled_for, 
                 engagement_metrics, seo_keywords)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (content.id, content.title, content.content, content.platform,
                  content.status, content.created_at, content.scheduled_for,
                  json.dumps(content.engagement_metrics) if content.engagement_metrics else None,
                  json.dumps(content.seo_keywords) if content.seo_keywords else None))
        
        conn.commit()
        conn.close()
    
    def check_website_health(self) -> Dict[str, WebsiteMetrics]:
        """Check health and metrics of both websites"""
        print("🌐 Checking website health...")
        
        website_metrics = {}
        
        for platform, config in self.platforms.items():
            try:
                # Check local development server
                local_url = config['local_url']
                response = requests.get(local_url, timeout=10)
                
                if response.status_code == 200:
                    # Simulate metrics (in real implementation, use analytics APIs)
                    metrics = WebsiteMetrics(
                        url=local_url,
                        page_views=1000 + hash(platform) % 5000,
                        conversion_rate=0.02 + (hash(platform) % 50) / 1000,
                        bounce_rate=0.3 + (hash(platform) % 40) / 100,
                        avg_session_duration=120 + hash(platform) % 300,
                        timestamp=datetime.datetime.now().isoformat()
                    )
                    
                    website_metrics[platform] = metrics
                    self.update_integration_status(f"website_{platform}", "active")
                    self.log_automation_action("health_check", platform, "success", 
                                             f"Response time: {response.elapsed.total_seconds():.2f}s")
                else:
                    self.update_integration_status(f"website_{platform}", "error", 
                                                 f"HTTP {response.status_code}")
                    self.log_automation_action("health_check", platform, "error", 
                                             f"HTTP {response.status_code}")
                    
            except Exception as e:
                self.update_integration_status(f"website_{platform}", "error", str(e))
                self.log_automation_action("health_check", platform, "error", str(e))
        
        return website_metrics
    
    def save_website_metrics(self, metrics: Dict[str, WebsiteMetrics]):
        """Save website metrics to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for platform, metric in metrics.items():
            cursor.execute('''
                INSERT INTO website_metrics 
                (url, page_views, conversion_rate, bounce_rate, avg_session_duration, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (metric.url, metric.page_views, metric.conversion_rate,
                  metric.bounce_rate, metric.avg_session_duration, metric.timestamp))
        
        conn.commit()
        conn.close()
    
    def create_social_media_posts(self, content_pieces: List[ContentPiece]) -> List[Dict[str, Any]]:
        """Create social media posts from content pieces"""
        print("📱 Creating social media posts...")
        
        social_posts = []
        
        for content in content_pieces:
            # Create Twitter/X post
            twitter_post = {
                'platform': 'twitter',
                'content': f"{content.title}\n\n{content.content[:200]}...\n\n#{content.platform} #AI #BusinessGrowth",
                'scheduled_time': datetime.datetime.now() + datetime.timedelta(hours=2),
                'content_id': content.id
            }
            
            # Create LinkedIn post
            linkedin_post = {
                'platform': 'linkedin',
                'content': f"{content.title}\n\n{content.content}\n\n#BusinessTransformation #AI #Entrepreneurship",
                'scheduled_time': datetime.datetime.now() + datetime.timedelta(hours=4),
                'content_id': content.id
            }
            
            social_posts.extend([twitter_post, linkedin_post])
        
        return social_posts
    
    def integrate_with_existing_automation(self, social_posts: List[Dict[str, Any]]):
        """Integrate with existing n8n/Activepieces automation"""
        print("🔗 Integrating with existing automation systems...")
        
        # Create integration file for existing automation systems
        integration_data = {
            'timestamp': datetime.datetime.now().isoformat(),
            'social_posts': social_posts,
            'platforms': list(self.platforms.keys()),
            'status': 'ready_for_automation'
        }
        
        # Save to file that can be picked up by existing automation
        integration_file = "/home/ubuntu/social_automation_integration.json"
        with open(integration_file, 'w') as f:
            json.dump(integration_data, f, indent=2, default=str)
        
        self.log_automation_action("social_integration", "all", "success", 
                                 f"Created {len(social_posts)} social posts")
    
    def run_automation_cycle(self):
        """Run a complete automation cycle"""
        print("\n🚀 Running automation cycle...")
        print("=" * 50)
        
        try:
            # 1. Collect trend data
            trends = self.collect_trend_data()
            self.save_trend_data(trends)
            print(f"✅ Collected {len(trends)} trends")
            
            # 2. Generate content from trends
            content_pieces = self.generate_content_from_trends(trends)
            self.save_content_pieces(content_pieces)
            print(f"✅ Generated {len(content_pieces)} content pieces")
            
            # 3. Check website health
            website_metrics = self.check_website_health()
            self.save_website_metrics(website_metrics)
            print(f"✅ Checked {len(website_metrics)} websites")
            
            # 4. Create social media posts
            social_posts = self.create_social_media_posts(content_pieces)
            print(f"✅ Created {len(social_posts)} social media posts")
            
            # 5. Integrate with existing automation
            self.integrate_with_existing_automation(social_posts)
            print("✅ Integrated with existing automation systems")
            
            # 6. Update overall status
            self.update_integration_status("automation_hub", "active")
            
            print(f"\n🎉 Automation cycle completed successfully!")
            
        except Exception as e:
            print(f"❌ Automation cycle failed: {str(e)}")
            self.update_integration_status("automation_hub", "error", str(e))
            self.log_automation_action("automation_cycle", "all", "error", str(e))
    
    def generate_integration_report(self) -> Dict[str, Any]:
        """Generate comprehensive integration report"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get recent automation logs
        cursor.execute('''
            SELECT action, platform, status, COUNT(*) as count
            FROM automation_logs 
            WHERE timestamp > datetime('now', '-24 hours')
            GROUP BY action, platform, status
        ''')
        recent_logs = cursor.fetchall()
        
        # Get integration status
        cursor.execute('''
            SELECT service_name, status, last_check, error_message
            FROM integration_status
            ORDER BY last_check DESC
        ''')
        integration_status = cursor.fetchall()
        
        # Get content queue status
        cursor.execute('''
            SELECT platform, status, COUNT(*) as count
            FROM content_queue
            GROUP BY platform, status
        ''')
        content_status = cursor.fetchall()
        
        # Get trend summary
        cursor.execute('''
            SELECT platform, AVG(relevance_score) as avg_relevance, COUNT(*) as trend_count
            FROM trend_tracking
            WHERE timestamp > datetime('now', '-24 hours')
            GROUP BY platform
        ''')
        trend_summary = cursor.fetchall()
        
        conn.close()
        
        report = {
            'timestamp': datetime.datetime.now().isoformat(),
            'automation_logs': [dict(zip(['action', 'platform', 'status', 'count'], log)) for log in recent_logs],
            'integration_status': [dict(zip(['service', 'status', 'last_check', 'error'], status)) for status in integration_status],
            'content_status': [dict(zip(['platform', 'status', 'count'], content)) for content in content_status],
            'trend_summary': [dict(zip(['platform', 'avg_relevance', 'trend_count'], trend)) for trend in trend_summary],
            'overall_health': 'healthy' if all(status[1] == 'active' for status in integration_status) else 'needs_attention'
        }
        
        return report
    
    def start_scheduled_automation(self):
        """Start scheduled automation tasks"""
        print("⏰ Starting scheduled automation...")
        
        # Schedule automation cycles
        schedule.every(2).hours.do(self.run_automation_cycle)
        schedule.every().day.at("09:00").do(self.run_automation_cycle)
        schedule.every().day.at("15:00").do(self.run_automation_cycle)
        
        self.running = True
        
        while self.running:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    def stop_automation(self):
        """Stop the automation system"""
        self.running = False
        print("🛑 Automation system stopped")

def main():
    """Main function to run the integration hub"""
    print("🔗 Integration and Automation Hub")
    print("=" * 40)
    
    # Initialize the integration hub
    hub = IntegrationHub()
    
    # Run initial automation cycle
    hub.run_automation_cycle()
    
    # Generate and save integration report
    report = hub.generate_integration_report()
    report_path = "/home/ubuntu/integration_report.json"
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    print(f"\n📋 Integration report saved to {report_path}")
    print(f"🎯 Overall system health: {report['overall_health']}")
    
    # Create automation startup script
    startup_script = """#!/bin/bash
# Integration Hub Startup Script
cd /home/ubuntu
python3 integration_automation_hub.py
"""
    
    with open("/home/ubuntu/start_automation.sh", 'w') as f:
        f.write(startup_script)
    
    os.chmod("/home/ubuntu/start_automation.sh", 0o755)
    
    print("✅ Integration and automation setup complete!")
    print("🚀 Use './start_automation.sh' to start the automation system")

if __name__ == "__main__":
    main()

