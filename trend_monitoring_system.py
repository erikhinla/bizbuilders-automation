#!/usr/bin/env python3
"""
Real-Time Trend Intelligence Hub
Monitors trends in business automation, AI transformation, and entrepreneurship
Analyzes viral X/Twitter content patterns for business accounts
"""

import sys
import json
import time
import datetime
import re
from typing import Dict, Any, List, Optional
from collections import defaultdict, Counter
import sqlite3
import os

# Add the Manus API client path
sys.path.append('/opt/.manus/.sandbox-runtime')
from data_api import ApiClient

class TrendMonitoringSystem:
    def __init__(self, db_path: str = "/home/ubuntu/trend_intelligence.db"):
        """Initialize the trend monitoring system"""
        self.client = ApiClient()
        self.db_path = db_path
        self.init_database()
        
        # Key monitoring keywords for business automation and AI transformation
        self.business_keywords = [
            "business automation", "AI transformation", "digital transformation",
            "workflow automation", "process automation", "AI tools", "automation tools",
            "entrepreneurship", "startup automation", "business AI", "AI business",
            "automation strategy", "digital business", "AI entrepreneurship",
            "business efficiency", "automated workflows", "AI productivity",
            "business innovation", "tech entrepreneurship", "AI startup",
            "automation ROI", "business optimization", "AI integration"
        ]
        
        # High-performing business accounts to monitor
        self.business_accounts = [
            "elonmusk", "sundarpichai", "satyanadella", "tim_cook", "jeffweiner",
            "reidhoffman", "naval", "paulg", "sama", "dharmesh", "jason",
            "garyvee", "neilpatel", "randfish", "buffer", "hootsuite",
            "hubspot", "salesforce", "zapier", "airtable", "notion"
        ]
        
    def init_database(self):
        """Initialize SQLite database for storing trend data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables for different data types
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trending_topics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword TEXT,
                tweet_count INTEGER,
                engagement_score REAL,
                timestamp DATETIME,
                trend_score REAL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS viral_content (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tweet_id TEXT UNIQUE,
                username TEXT,
                content TEXT,
                retweet_count INTEGER,
                like_count INTEGER,
                reply_count INTEGER,
                engagement_rate REAL,
                timestamp DATETIME,
                content_type TEXT,
                keywords TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS content_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_type TEXT,
                pattern_description TEXT,
                success_rate REAL,
                avg_engagement REAL,
                examples TEXT,
                timestamp DATETIME
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_insights (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE,
                top_trends TEXT,
                content_opportunities TEXT,
                competitor_insights TEXT,
                recommendations TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def search_trending_content(self, keyword: str, count: int = 50) -> List[Dict]:
        """Search for trending content related to specific keywords"""
        try:
            query_params = {
                'query': f"{keyword} -is:retweet lang:en",
                'count': str(count)
            }
            
            response = self.client.call_api('Twitter/search_twitter', query=query_params)
            
            tweets = []
            if 'result' in response and 'timeline' in response['result']:
                timeline = response['result']['timeline']
                instructions = timeline.get('instructions', [])
                
                for instruction in instructions:
                    if instruction.get('type') == 'TimelineAddEntries':
                        entries = instruction.get('entries', [])
                        for entry in entries:
                            if entry.get('entryId', '').startswith('tweet-'):
                                content = entry.get('content', {})
                                if 'itemContent' in content:
                                    tweet_results = content['itemContent'].get('tweet_results', {})
                                    if 'result' in tweet_results:
                                        tweets.append(tweet_results['result'])
            
            return tweets
            
        except Exception as e:
            print(f"Error searching for keyword '{keyword}': {str(e)}")
            return []
    
    def get_user_profile(self, username: str) -> Dict[str, Any]:
        """Get Twitter user profile information"""
        try:
            query_params = {'username': username}
            response = self.client.call_api('Twitter/get_user_profile_by_username', query=query_params)
            
            if response and 'result' in response:
                user_data = response['result'].get('data', {}).get('user', {}).get('result', {})
                return user_data
            return {}
            
        except Exception as e:
            print(f"Error getting profile for @{username}: {str(e)}")
            return {}
    
    def get_user_tweets(self, user_id: str, count: int = 20) -> List[Dict]:
        """Get recent tweets from a specific user"""
        try:
            query_params = {
                'user': str(user_id),
                'count': str(count)
            }
            
            response = self.client.call_api('Twitter/get_user_tweets', query=query_params)
            
            tweets = []
            if 'result' in response and 'timeline' in response['result']:
                timeline = response['result']['timeline']
                instructions = timeline.get('instructions', [])
                
                for instruction in instructions:
                    if instruction.get('type') == 'TimelineAddEntries':
                        entries = instruction.get('entries', [])
                        for entry in entries:
                            if entry.get('entryId', '').startswith('tweet-'):
                                content = entry.get('content', {})
                                if 'itemContent' in content:
                                    tweet_results = content['itemContent'].get('tweet_results', {})
                                    if 'result' in tweet_results:
                                        tweets.append(tweet_results['result'])
            
            return tweets
            
        except Exception as e:
            print(f"Error getting tweets for user {user_id}: {str(e)}")
            return []
    
    def analyze_tweet_engagement(self, tweet_data: Dict) -> Dict[str, Any]:
        """Analyze engagement metrics for a tweet"""
        legacy = tweet_data.get('legacy', {})
        
        retweet_count = legacy.get('retweet_count', 0)
        favorite_count = legacy.get('favorite_count', 0)
        reply_count = legacy.get('reply_count', 0)
        quote_count = legacy.get('quote_count', 0)
        
        # Calculate engagement rate (simplified)
        total_engagement = retweet_count + favorite_count + reply_count + quote_count
        
        # Get follower count for engagement rate calculation
        core = tweet_data.get('core', {})
        user_results = core.get('user_results', {})
        user_result = user_results.get('result', {})
        user_legacy = user_result.get('legacy', {})
        followers_count = user_legacy.get('followers_count', 1)
        
        engagement_rate = (total_engagement / max(followers_count, 1)) * 100
        
        return {
            'retweet_count': retweet_count,
            'favorite_count': favorite_count,
            'reply_count': reply_count,
            'quote_count': quote_count,
            'total_engagement': total_engagement,
            'engagement_rate': engagement_rate,
            'followers_count': followers_count
        }
    
    def extract_content_patterns(self, tweets: List[Dict]) -> Dict[str, Any]:
        """Extract patterns from high-performing content"""
        patterns = {
            'hashtag_usage': Counter(),
            'content_length': [],
            'posting_times': [],
            'content_types': Counter(),
            'engagement_by_type': defaultdict(list)
        }
        
        for tweet in tweets:
            legacy = tweet.get('legacy', {})
            text = legacy.get('full_text', '')
            created_at = legacy.get('created_at', '')
            
            # Extract hashtags
            hashtags = re.findall(r'#\w+', text)
            patterns['hashtag_usage'].update(hashtags)
            
            # Content length
            patterns['content_length'].append(len(text))
            
            # Posting time analysis
            if created_at:
                try:
                    # Parse Twitter timestamp format
                    dt = datetime.datetime.strptime(created_at, '%a %b %d %H:%M:%S %z %Y')
                    patterns['posting_times'].append(dt.hour)
                except:
                    pass
            
            # Content type classification
            content_type = self.classify_content_type(text, legacy)
            patterns['content_types'][content_type] += 1
            
            # Engagement by content type
            engagement = self.analyze_tweet_engagement(tweet)
            patterns['engagement_by_type'][content_type].append(engagement['engagement_rate'])
        
        return patterns
    
    def classify_content_type(self, text: str, legacy: Dict) -> str:
        """Classify the type of content"""
        text_lower = text.lower()
        
        # Check for media
        entities = legacy.get('entities', {})
        has_media = bool(entities.get('media', []))
        has_urls = bool(entities.get('urls', []))
        
        # Classification logic
        if '?' in text:
            return 'question'
        elif has_media:
            return 'media_post'
        elif has_urls:
            return 'link_share'
        elif any(word in text_lower for word in ['tip', 'how to', 'guide', 'tutorial']):
            return 'educational'
        elif any(word in text_lower for word in ['announcement', 'launching', 'excited to']):
            return 'announcement'
        elif len(text) > 200:
            return 'long_form'
        else:
            return 'general'
    
    def calculate_trend_score(self, keyword: str, tweets: List[Dict]) -> float:
        """Calculate a trend score for a keyword based on engagement and volume"""
        if not tweets:
            return 0.0
        
        total_engagement = 0
        total_tweets = len(tweets)
        
        for tweet in tweets:
            engagement = self.analyze_tweet_engagement(tweet)
            total_engagement += engagement['total_engagement']
        
        # Normalize by tweet count and apply time decay
        avg_engagement = total_engagement / max(total_tweets, 1)
        volume_score = min(total_tweets / 100, 1.0)  # Cap at 100 tweets
        
        trend_score = (avg_engagement * 0.7) + (volume_score * 0.3)
        return trend_score
    
    def store_trending_data(self, keyword: str, tweets: List[Dict], trend_score: float):
        """Store trending data in the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        timestamp = datetime.datetime.now()
        tweet_count = len(tweets)
        
        # Calculate average engagement
        total_engagement = sum(
            self.analyze_tweet_engagement(tweet)['total_engagement'] 
            for tweet in tweets
        )
        avg_engagement = total_engagement / max(tweet_count, 1)
        
        cursor.execute('''
            INSERT INTO trending_topics 
            (keyword, tweet_count, engagement_score, timestamp, trend_score)
            VALUES (?, ?, ?, ?, ?)
        ''', (keyword, tweet_count, avg_engagement, timestamp, trend_score))
        
        # Store viral content (top performing tweets)
        for tweet in tweets[:10]:  # Store top 10 tweets
            legacy = tweet.get('legacy', {})
            core = tweet.get('core', {})
            user_results = core.get('user_results', {})
            user_result = user_results.get('result', {})
            user_legacy = user_result.get('legacy', {})
            
            tweet_id = legacy.get('id_str', tweet.get('rest_id', ''))
            username = user_legacy.get('screen_name', '')
            content = legacy.get('full_text', '')
            
            engagement = self.analyze_tweet_engagement(tweet)
            content_type = self.classify_content_type(content, legacy)
            
            try:
                cursor.execute('''
                    INSERT OR REPLACE INTO viral_content 
                    (tweet_id, username, content, retweet_count, like_count, 
                     reply_count, engagement_rate, timestamp, content_type, keywords)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    tweet_id, username, content[:500], 
                    engagement['retweet_count'], engagement['favorite_count'],
                    engagement['reply_count'], engagement['engagement_rate'],
                    timestamp, content_type, keyword
                ))
            except sqlite3.IntegrityError:
                pass  # Tweet already exists
        
        conn.commit()
        conn.close()
    
    def monitor_business_accounts(self):
        """Monitor high-performing business accounts for content patterns"""
        print("Monitoring business accounts for content patterns...")
        
        account_insights = {}
        
        for username in self.business_accounts[:5]:  # Monitor first 5 accounts
            print(f"Analyzing @{username}...")
            
            # Get user profile
            profile = self.get_user_profile(username)
            if not profile:
                continue
            
            # Get user ID
            user_id = profile.get('rest_id')
            if not user_id:
                continue
            
            # Get recent tweets
            tweets = self.get_user_tweets(user_id, count=20)
            if not tweets:
                continue
            
            # Analyze content patterns
            patterns = self.extract_content_patterns(tweets)
            
            # Calculate average engagement
            engagements = [
                self.analyze_tweet_engagement(tweet)['engagement_rate'] 
                for tweet in tweets
            ]
            avg_engagement = sum(engagements) / len(engagements) if engagements else 0
            
            account_insights[username] = {
                'avg_engagement': avg_engagement,
                'patterns': patterns,
                'follower_count': profile.get('legacy', {}).get('followers_count', 0),
                'tweet_count': len(tweets)
            }
            
            time.sleep(1)  # Rate limiting
        
        return account_insights
    
    def run_trend_analysis(self):
        """Run comprehensive trend analysis"""
        print("Starting comprehensive trend analysis...")
        
        trend_results = {}
        
        # Monitor each keyword
        for keyword in self.business_keywords[:10]:  # Monitor first 10 keywords
            print(f"Analyzing trend: {keyword}")
            
            tweets = self.search_trending_content(keyword, count=30)
            if tweets:
                trend_score = self.calculate_trend_score(keyword, tweets)
                self.store_trending_data(keyword, tweets, trend_score)
                
                trend_results[keyword] = {
                    'tweet_count': len(tweets),
                    'trend_score': trend_score,
                    'patterns': self.extract_content_patterns(tweets)
                }
            
            time.sleep(2)  # Rate limiting
        
        return trend_results
    
    def generate_daily_briefing(self) -> Dict[str, Any]:
        """Generate daily trend briefing"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get today's top trends
        today = datetime.date.today()
        cursor.execute('''
            SELECT keyword, AVG(trend_score) as avg_score, COUNT(*) as mentions
            FROM trending_topics 
            WHERE DATE(timestamp) = ?
            GROUP BY keyword
            ORDER BY avg_score DESC
            LIMIT 10
        ''', (today,))
        
        top_trends = cursor.fetchall()
        
        # Get top viral content
        cursor.execute('''
            SELECT username, content, engagement_rate, content_type
            FROM viral_content 
            WHERE DATE(timestamp) = ?
            ORDER BY engagement_rate DESC
            LIMIT 5
        ''', (today,))
        
        viral_content = cursor.fetchall()
        
        # Get content patterns
        cursor.execute('''
            SELECT content_type, AVG(engagement_rate) as avg_engagement
            FROM viral_content 
            WHERE DATE(timestamp) = ?
            GROUP BY content_type
            ORDER BY avg_engagement DESC
        ''', (today,))
        
        content_patterns = cursor.fetchall()
        
        conn.close()
        
        briefing = {
            'date': today.isoformat(),
            'top_trends': [
                {'keyword': trend[0], 'score': trend[1], 'mentions': trend[2]}
                for trend in top_trends
            ],
            'viral_content': [
                {
                    'username': content[0],
                    'content': content[1][:100] + '...',
                    'engagement_rate': content[2],
                    'type': content[3]
                }
                for content in viral_content
            ],
            'content_patterns': [
                {'type': pattern[0], 'avg_engagement': pattern[1]}
                for pattern in content_patterns
            ]
        }
        
        return briefing

def main():
    """Main function to run the trend monitoring system"""
    print("🚀 Real-Time Trend Intelligence Hub")
    print("=" * 50)
    
    # Initialize the system
    monitor = TrendMonitoringSystem()
    
    # Run trend analysis
    print("\n📊 Running trend analysis...")
    trend_results = monitor.run_trend_analysis()
    
    # Monitor business accounts
    print("\n👥 Monitoring business accounts...")
    account_insights = monitor.monitor_business_accounts()
    
    # Generate daily briefing
    print("\n📋 Generating daily briefing...")
    briefing = monitor.generate_daily_briefing()
    
    # Save results
    results = {
        'timestamp': datetime.datetime.now().isoformat(),
        'trend_results': trend_results,
        'account_insights': account_insights,
        'daily_briefing': briefing
    }
    
    with open('/home/ubuntu/trend_analysis_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print("\n✅ Analysis complete! Results saved to trend_analysis_results.json")
    print(f"📈 Analyzed {len(trend_results)} trending topics")
    print(f"👤 Monitored {len(account_insights)} business accounts")
    print(f"📊 Generated briefing with {len(briefing['top_trends'])} top trends")

if __name__ == "__main__":
    main()

