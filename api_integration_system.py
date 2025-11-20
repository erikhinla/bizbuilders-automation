#!/usr/bin/env python3
"""
API Integration System
Connects with existing social media automation tools and platforms
"""

import os
import json
import time
import datetime
import requests
import sqlite3
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
import hashlib
import hmac
import base64

@dataclass
class SocialMediaPost:
    """Data class for social media posts"""
    id: str
    platform: str
    content: str
    media_urls: List[str]
    hashtags: List[str]
    scheduled_time: str
    status: str
    engagement_metrics: Optional[Dict[str, int]] = None

@dataclass
class WebhookPayload:
    """Data class for webhook payloads"""
    event_type: str
    platform: str
    data: Dict[str, Any]
    timestamp: str
    signature: str

class APIIntegrationSystem:
    def __init__(self, db_path: str = "/home/ubuntu/api_integration.db"):
        """Initialize the API integration system"""
        self.db_path = db_path
        self.init_database()
        
        # API configurations (would be loaded from environment in production)
        self.api_configs = {
            'n8n': {
                'webhook_url': 'http://localhost:5678/webhook/social-automation',
                'api_key': 'your-n8n-api-key',
                'enabled': True
            },
            'activepieces': {
                'webhook_url': 'http://localhost:3000/api/v1/webhooks/social-content',
                'api_key': 'your-activepieces-api-key',
                'enabled': True
            },
            'zapier': {
                'webhook_url': 'https://hooks.zapier.com/hooks/catch/your-webhook-id',
                'api_key': 'your-zapier-api-key',
                'enabled': False
            },
            'make': {
                'webhook_url': 'https://hook.integromat.com/your-webhook-id',
                'api_key': 'your-make-api-key',
                'enabled': False
            }
        }
        
        # Social media platform configurations
        self.social_platforms = {
            'twitter': {
                'api_endpoint': 'https://api.twitter.com/2/tweets',
                'character_limit': 280,
                'hashtag_limit': 10,
                'media_limit': 4
            },
            'linkedin': {
                'api_endpoint': 'https://api.linkedin.com/v2/ugcPosts',
                'character_limit': 3000,
                'hashtag_limit': 5,
                'media_limit': 9
            },
            'facebook': {
                'api_endpoint': 'https://graph.facebook.com/v18.0/me/feed',
                'character_limit': 63206,
                'hashtag_limit': 30,
                'media_limit': 10
            },
            'instagram': {
                'api_endpoint': 'https://graph.facebook.com/v18.0/me/media',
                'character_limit': 2200,
                'hashtag_limit': 30,
                'media_limit': 10
            }
        }
    
    def init_database(self):
        """Initialize SQLite database for API integration"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Social media posts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS social_posts (
                id TEXT PRIMARY KEY,
                platform TEXT,
                content TEXT,
                media_urls TEXT,
                hashtags TEXT,
                scheduled_time DATETIME,
                status TEXT,
                engagement_metrics TEXT,
                created_at DATETIME,
                updated_at DATETIME
            )
        ''')
        
        # API calls log table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS api_calls_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                service TEXT,
                endpoint TEXT,
                method TEXT,
                status_code INTEGER,
                response_time REAL,
                timestamp DATETIME,
                error_message TEXT
            )
        ''')
        
        # Webhook events table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS webhook_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT,
                platform TEXT,
                payload TEXT,
                processed BOOLEAN,
                timestamp DATETIME
            )
        ''')
        
        # Integration metrics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS integration_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                service TEXT,
                metric_name TEXT,
                metric_value REAL,
                timestamp DATETIME
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def log_api_call(self, service: str, endpoint: str, method: str, 
                     status_code: int, response_time: float, error_message: str = ""):
        """Log API call details"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO api_calls_log 
            (service, endpoint, method, status_code, response_time, timestamp, error_message)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (service, endpoint, method, status_code, response_time, 
              datetime.datetime.now(), error_message))
        
        conn.commit()
        conn.close()
    
    def create_webhook_payload(self, event_type: str, platform: str, data: Dict[str, Any]) -> WebhookPayload:
        """Create webhook payload with signature"""
        timestamp = datetime.datetime.now().isoformat()
        
        # Create signature for webhook security
        payload_string = f"{event_type}{platform}{json.dumps(data, sort_keys=True)}{timestamp}"
        signature = hashlib.sha256(payload_string.encode()).hexdigest()
        
        return WebhookPayload(
            event_type=event_type,
            platform=platform,
            data=data,
            timestamp=timestamp,
            signature=signature
        )
    
    def send_to_n8n(self, payload: WebhookPayload) -> bool:
        """Send data to n8n automation workflow"""
        config = self.api_configs['n8n']
        if not config['enabled']:
            return False
        
        try:
            start_time = time.time()
            
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f"Bearer {config['api_key']}",
                'X-Webhook-Signature': payload.signature
            }
            
            response = requests.post(
                config['webhook_url'],
                json=asdict(payload),
                headers=headers,
                timeout=30
            )
            
            response_time = time.time() - start_time
            
            self.log_api_call('n8n', config['webhook_url'], 'POST', 
                            response.status_code, response_time)
            
            return response.status_code == 200
            
        except Exception as e:
            self.log_api_call('n8n', config['webhook_url'], 'POST', 
                            0, 0, str(e))
            return False
    
    def send_to_activepieces(self, payload: WebhookPayload) -> bool:
        """Send data to Activepieces automation workflow"""
        config = self.api_configs['activepieces']
        if not config['enabled']:
            return False
        
        try:
            start_time = time.time()
            
            headers = {
                'Content-Type': 'application/json',
                'X-API-Key': config['api_key'],
                'X-Webhook-Signature': payload.signature
            }
            
            response = requests.post(
                config['webhook_url'],
                json=asdict(payload),
                headers=headers,
                timeout=30
            )
            
            response_time = time.time() - start_time
            
            self.log_api_call('activepieces', config['webhook_url'], 'POST', 
                            response.status_code, response_time)
            
            return response.status_code == 200
            
        except Exception as e:
            self.log_api_call('activepieces', config['webhook_url'], 'POST', 
                            0, 0, str(e))
            return False
    
    def optimize_content_for_platform(self, content: str, platform: str) -> Dict[str, Any]:
        """Optimize content for specific social media platform"""
        platform_config = self.social_platforms.get(platform, {})
        character_limit = platform_config.get('character_limit', 280)
        hashtag_limit = platform_config.get('hashtag_limit', 10)
        
        # Extract hashtags from content
        import re
        hashtags = re.findall(r'#\w+', content)
        hashtags = hashtags[:hashtag_limit]
        
        # Remove hashtags from content for length calculation
        content_without_hashtags = re.sub(r'#\w+', '', content).strip()
        
        # Truncate content if necessary
        hashtag_length = sum(len(tag) + 1 for tag in hashtags)  # +1 for space
        available_length = character_limit - hashtag_length - 10  # -10 for buffer
        
        if len(content_without_hashtags) > available_length:
            content_without_hashtags = content_without_hashtags[:available_length-3] + "..."
        
        # Combine content and hashtags
        optimized_content = content_without_hashtags
        if hashtags:
            optimized_content += "\n\n" + " ".join(hashtags)
        
        return {
            'content': optimized_content,
            'hashtags': hashtags,
            'character_count': len(optimized_content),
            'within_limit': len(optimized_content) <= character_limit
        }
    
    def create_social_media_posts(self, content_data: Dict[str, Any]) -> List[SocialMediaPost]:
        """Create optimized social media posts for multiple platforms"""
        posts = []
        
        base_content = content_data.get('content', '')
        title = content_data.get('title', '')
        platform_focus = content_data.get('platform', 'transformby10x')
        
        # Define platform-specific content variations
        platform_variations = {
            'twitter': {
                'prefix': '🚀',
                'cta': 'Learn more:',
                'hashtags': ['#AI', '#BusinessGrowth', '#Automation']
            },
            'linkedin': {
                'prefix': '💼',
                'cta': 'What are your thoughts on this?',
                'hashtags': ['#BusinessTransformation', '#AI', '#Leadership']
            },
            'facebook': {
                'prefix': '👥',
                'cta': 'Share your experience in the comments!',
                'hashtags': ['#Business', '#Innovation', '#Growth']
            },
            'instagram': {
                'prefix': '📸',
                'cta': 'Double tap if you agree!',
                'hashtags': ['#Entrepreneur', '#Success', '#Motivation']
            }
        }
        
        for platform, variation in platform_variations.items():
            # Create platform-specific content
            platform_content = f"{variation['prefix']} {title}\n\n{base_content}\n\n{variation['cta']}"
            
            # Add platform-specific hashtags
            if platform_focus == 'transformby10x':
                variation['hashtags'].extend(['#TransformBy10X', '#BusinessAutomation'])
            else:
                variation['hashtags'].extend(['#BizBuilders', '#Entrepreneurship'])
            
            # Optimize for platform
            optimized = self.optimize_content_for_platform(
                platform_content + " " + " ".join(variation['hashtags']), 
                platform
            )
            
            # Create post object
            post_id = f"{platform}_{int(time.time())}_{hash(platform_content) % 1000}"
            
            post = SocialMediaPost(
                id=post_id,
                platform=platform,
                content=optimized['content'],
                media_urls=[],  # Would be populated with actual media URLs
                hashtags=optimized['hashtags'],
                scheduled_time=(datetime.datetime.now() + datetime.timedelta(hours=1)).isoformat(),
                status='draft'
            )
            
            posts.append(post)
        
        return posts
    
    def save_social_posts(self, posts: List[SocialMediaPost]):
        """Save social media posts to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for post in posts:
            cursor.execute('''
                INSERT OR REPLACE INTO social_posts 
                (id, platform, content, media_urls, hashtags, scheduled_time, status, 
                 engagement_metrics, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (post.id, post.platform, post.content, 
                  json.dumps(post.media_urls), json.dumps(post.hashtags),
                  post.scheduled_time, post.status, 
                  json.dumps(post.engagement_metrics) if post.engagement_metrics else None,
                  datetime.datetime.now(), datetime.datetime.now()))
        
        conn.commit()
        conn.close()
    
    def send_posts_to_automation_platforms(self, posts: List[SocialMediaPost]) -> Dict[str, bool]:
        """Send posts to all enabled automation platforms"""
        results = {}
        
        for post in posts:
            # Create webhook payload
            payload = self.create_webhook_payload(
                event_type='social_post_created',
                platform=post.platform,
                data=asdict(post)
            )
            
            # Send to n8n
            if self.api_configs['n8n']['enabled']:
                results[f"n8n_{post.platform}"] = self.send_to_n8n(payload)
            
            # Send to Activepieces
            if self.api_configs['activepieces']['enabled']:
                results[f"activepieces_{post.platform}"] = self.send_to_activepieces(payload)
        
        return results
    
    def process_content_batch(self, content_batch: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Process a batch of content for social media automation"""
        print(f"📦 Processing batch of {len(content_batch)} content pieces...")
        
        all_posts = []
        processing_results = {
            'total_content_pieces': len(content_batch),
            'total_posts_created': 0,
            'platform_distribution': {},
            'automation_results': {},
            'errors': []
        }
        
        for content_data in content_batch:
            try:
                # Create social media posts
                posts = self.create_social_media_posts(content_data)
                all_posts.extend(posts)
                
                # Update platform distribution
                for post in posts:
                    platform = post.platform
                    processing_results['platform_distribution'][platform] = \
                        processing_results['platform_distribution'].get(platform, 0) + 1
                
            except Exception as e:
                processing_results['errors'].append(f"Error processing content: {str(e)}")
        
        # Save all posts
        if all_posts:
            self.save_social_posts(all_posts)
            processing_results['total_posts_created'] = len(all_posts)
            
            # Send to automation platforms
            automation_results = self.send_posts_to_automation_platforms(all_posts)
            processing_results['automation_results'] = automation_results
        
        return processing_results
    
    def create_integration_dashboard_data(self) -> Dict[str, Any]:
        """Create data for integration dashboard"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get recent API call statistics
        cursor.execute('''
            SELECT service, COUNT(*) as call_count, AVG(response_time) as avg_response_time,
                   SUM(CASE WHEN status_code = 200 THEN 1 ELSE 0 END) as success_count
            FROM api_calls_log 
            WHERE timestamp > datetime('now', '-24 hours')
            GROUP BY service
        ''')
        api_stats = cursor.fetchall()
        
        # Get social posts statistics
        cursor.execute('''
            SELECT platform, status, COUNT(*) as count
            FROM social_posts
            WHERE created_at > datetime('now', '-24 hours')
            GROUP BY platform, status
        ''')
        post_stats = cursor.fetchall()
        
        # Get webhook events statistics
        cursor.execute('''
            SELECT event_type, COUNT(*) as count
            FROM webhook_events
            WHERE timestamp > datetime('now', '-24 hours')
            GROUP BY event_type
        ''')
        webhook_stats = cursor.fetchall()
        
        conn.close()
        
        dashboard_data = {
            'timestamp': datetime.datetime.now().isoformat(),
            'api_statistics': [dict(zip(['service', 'call_count', 'avg_response_time', 'success_count'], stat)) for stat in api_stats],
            'post_statistics': [dict(zip(['platform', 'status', 'count'], stat)) for stat in post_stats],
            'webhook_statistics': [dict(zip(['event_type', 'count'], stat)) for stat in webhook_stats],
            'integration_health': self.check_integration_health()
        }
        
        return dashboard_data
    
    def check_integration_health(self) -> Dict[str, str]:
        """Check health of all integrations"""
        health_status = {}
        
        for service, config in self.api_configs.items():
            if config['enabled']:
                try:
                    # Simple health check (ping endpoint)
                    response = requests.get(config['webhook_url'], timeout=5)
                    health_status[service] = 'healthy' if response.status_code < 500 else 'degraded'
                except:
                    health_status[service] = 'unhealthy'
            else:
                health_status[service] = 'disabled'
        
        return health_status

def main():
    """Main function to run API integration system"""
    print("🔌 API Integration System")
    print("=" * 40)
    
    # Initialize the API integration system
    api_system = APIIntegrationSystem()
    
    # Load sample content from integration hub
    sample_content = [
        {
            'title': 'Transform Your Business with AI Automation',
            'content': 'Discover how AI automation can revolutionize your business operations and drive 10x growth.',
            'platform': 'transformby10x',
            'keywords': ['AI automation', 'business transformation', '10x growth']
        },
        {
            'title': 'Building Your Startup Empire',
            'content': 'Learn the essential tools and strategies successful entrepreneurs use to build thriving businesses.',
            'platform': 'bizbuilders',
            'keywords': ['startup', 'entrepreneurship', 'business building']
        }
    ]
    
    # Process content batch
    print("🚀 Processing sample content batch...")
    results = api_system.process_content_batch(sample_content)
    
    print(f"✅ Created {results['total_posts_created']} social media posts")
    print(f"📊 Platform distribution: {results['platform_distribution']}")
    print(f"🔗 Automation results: {results['automation_results']}")
    
    # Create dashboard data
    dashboard_data = api_system.create_integration_dashboard_data()
    
    # Save dashboard data
    dashboard_path = "/home/ubuntu/api_integration_dashboard.json"
    with open(dashboard_path, 'w') as f:
        json.dump(dashboard_data, f, indent=2, default=str)
    
    print(f"📋 Dashboard data saved to {dashboard_path}")
    
    # Save API integration results
    results_path = "/home/ubuntu/api_integration_results.json"
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"📊 Integration results saved to {results_path}")
    print("✅ API integration system setup complete!")

if __name__ == "__main__":
    main()

