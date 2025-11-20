#!/usr/bin/env python3
"""
Trend Alert System
Real-time notification system for trending topics and content opportunities
"""

import sys
import json
import time
import datetime
import sqlite3
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Add the Manus API client path
sys.path.append('/opt/.manus/.sandbox-runtime')
from data_api import ApiClient

@dataclass
class TrendAlert:
    """Data class for trend alerts"""
    keyword: str
    trend_score: float
    tweet_count: int
    engagement_score: float
    alert_type: str
    timestamp: datetime.datetime
    content_opportunities: List[str]
    recommended_actions: List[str]

class TrendAlertSystem:
    def __init__(self, db_path: str = "/home/ubuntu/trend_intelligence.db"):
        """Initialize the trend alert system"""
        self.client = ApiClient()
        self.db_path = db_path
        
        # Alert thresholds
        self.thresholds = {
            'high_trend_score': 50.0,
            'viral_engagement': 1000,
            'rapid_growth': 0.5,  # 50% increase in mentions
            'new_keyword_emergence': 10  # minimum mentions for new keywords
        }
        
        # Alert types
        self.alert_types = {
            'VIRAL_TREND': 'Viral trend detected',
            'EMERGING_TOPIC': 'New topic emerging',
            'ENGAGEMENT_SPIKE': 'Engagement spike detected',
            'COMPETITOR_ACTIVITY': 'Competitor activity alert',
            'CONTENT_OPPORTUNITY': 'Content opportunity identified'
        }
        
    def check_viral_trends(self) -> List[TrendAlert]:
        """Check for viral trends based on engagement and growth"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        alerts = []
        
        # Get trends from last 24 hours with high engagement
        cursor.execute('''
            SELECT keyword, AVG(trend_score) as avg_score, 
                   SUM(tweet_count) as total_tweets,
                   AVG(engagement_score) as avg_engagement
            FROM trending_topics 
            WHERE timestamp >= datetime('now', '-24 hours')
            GROUP BY keyword
            HAVING avg_score > ? OR avg_engagement > ?
            ORDER BY avg_score DESC
        ''', (self.thresholds['high_trend_score'], self.thresholds['viral_engagement']))
        
        viral_trends = cursor.fetchall()
        
        for trend in viral_trends:
            keyword, score, tweets, engagement = trend
            
            # Generate content opportunities
            opportunities = self.generate_content_opportunities(keyword, score, engagement)
            actions = self.generate_recommended_actions(keyword, score, engagement)
            
            alert = TrendAlert(
                keyword=keyword,
                trend_score=score,
                tweet_count=tweets,
                engagement_score=engagement,
                alert_type='VIRAL_TREND',
                timestamp=datetime.datetime.now(),
                content_opportunities=opportunities,
                recommended_actions=actions
            )
            alerts.append(alert)
        
        conn.close()
        return alerts
    
    def check_emerging_topics(self) -> List[TrendAlert]:
        """Check for emerging topics that are gaining traction"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        alerts = []
        
        # Find keywords that appeared recently but are growing
        cursor.execute('''
            SELECT keyword, COUNT(*) as mention_count,
                   AVG(trend_score) as avg_score,
                   AVG(engagement_score) as avg_engagement,
                   MIN(timestamp) as first_seen
            FROM trending_topics 
            WHERE timestamp >= datetime('now', '-48 hours')
            GROUP BY keyword
            HAVING mention_count >= ? AND first_seen >= datetime('now', '-24 hours')
            ORDER BY avg_score DESC
        ''', (self.thresholds['new_keyword_emergence'],))
        
        emerging_topics = cursor.fetchall()
        
        for topic in emerging_topics:
            keyword, mentions, score, engagement, first_seen = topic
            
            opportunities = self.generate_content_opportunities(keyword, score, engagement)
            actions = self.generate_recommended_actions(keyword, score, engagement)
            
            alert = TrendAlert(
                keyword=keyword,
                trend_score=score,
                tweet_count=mentions,
                engagement_score=engagement,
                alert_type='EMERGING_TOPIC',
                timestamp=datetime.datetime.now(),
                content_opportunities=opportunities,
                recommended_actions=actions
            )
            alerts.append(alert)
        
        conn.close()
        return alerts
    
    def check_engagement_spikes(self) -> List[TrendAlert]:
        """Check for sudden engagement spikes on tracked keywords"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        alerts = []
        
        # Compare recent engagement with historical averages
        cursor.execute('''
            WITH recent_engagement AS (
                SELECT keyword, AVG(engagement_score) as recent_avg
                FROM trending_topics 
                WHERE timestamp >= datetime('now', '-6 hours')
                GROUP BY keyword
            ),
            historical_engagement AS (
                SELECT keyword, AVG(engagement_score) as historical_avg
                FROM trending_topics 
                WHERE timestamp BETWEEN datetime('now', '-7 days') AND datetime('now', '-24 hours')
                GROUP BY keyword
            )
            SELECT r.keyword, r.recent_avg, h.historical_avg,
                   (r.recent_avg - h.historical_avg) / h.historical_avg as growth_rate
            FROM recent_engagement r
            JOIN historical_engagement h ON r.keyword = h.keyword
            WHERE growth_rate > ?
            ORDER BY growth_rate DESC
        ''', (self.thresholds['rapid_growth'],))
        
        spikes = cursor.fetchall()
        
        for spike in spikes:
            keyword, recent_avg, historical_avg, growth_rate = spike
            
            opportunities = self.generate_content_opportunities(keyword, recent_avg, recent_avg)
            actions = [
                f"Capitalize on {growth_rate*100:.1f}% engagement increase",
                "Create timely content around this trending topic",
                "Monitor for continued growth"
            ]
            
            alert = TrendAlert(
                keyword=keyword,
                trend_score=recent_avg,
                tweet_count=0,
                engagement_score=recent_avg,
                alert_type='ENGAGEMENT_SPIKE',
                timestamp=datetime.datetime.now(),
                content_opportunities=opportunities,
                recommended_actions=actions
            )
            alerts.append(alert)
        
        conn.close()
        return alerts
    
    def check_competitor_activity(self) -> List[TrendAlert]:
        """Check for significant competitor activity"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        alerts = []
        
        # Find high-engagement content from competitors
        cursor.execute('''
            SELECT username, content, engagement_rate, content_type, keywords
            FROM viral_content 
            WHERE timestamp >= datetime('now', '-24 hours')
              AND engagement_rate > 0.1
            ORDER BY engagement_rate DESC
            LIMIT 10
        ''')
        
        competitor_content = cursor.fetchall()
        
        if competitor_content:
            # Group by keywords to identify trending topics
            keyword_activity = {}
            for content in competitor_content:
                username, text, engagement, content_type, keywords = content
                if keywords:
                    if keywords not in keyword_activity:
                        keyword_activity[keywords] = []
                    keyword_activity[keywords].append({
                        'username': username,
                        'engagement': engagement,
                        'type': content_type
                    })
            
            for keyword, activities in keyword_activity.items():
                avg_engagement = sum(a['engagement'] for a in activities) / len(activities)
                
                opportunities = [
                    f"Respond to competitor content on {keyword}",
                    f"Create alternative perspective on {keyword}",
                    f"Engage with trending {keyword} discussions"
                ]
                
                actions = [
                    "Monitor competitor strategies",
                    "Create differentiated content",
                    "Engage in trending conversations"
                ]
                
                alert = TrendAlert(
                    keyword=keyword,
                    trend_score=avg_engagement * 100,
                    tweet_count=len(activities),
                    engagement_score=avg_engagement,
                    alert_type='COMPETITOR_ACTIVITY',
                    timestamp=datetime.datetime.now(),
                    content_opportunities=opportunities,
                    recommended_actions=actions
                )
                alerts.append(alert)
        
        conn.close()
        return alerts
    
    def generate_content_opportunities(self, keyword: str, score: float, engagement: float) -> List[str]:
        """Generate content opportunities based on trending keyword"""
        opportunities = []
        
        # Base opportunities
        opportunities.extend([
            f"Create educational content about {keyword}",
            f"Share case study related to {keyword}",
            f"Start discussion thread on {keyword}",
            f"Create infographic about {keyword} trends"
        ])
        
        # Score-based opportunities
        if score > 75:
            opportunities.extend([
                f"Host live discussion on {keyword}",
                f"Create video content about {keyword}",
                f"Launch poll about {keyword} preferences"
            ])
        
        # Engagement-based opportunities
        if engagement > 500:
            opportunities.extend([
                f"Create viral-style content about {keyword}",
                f"Collaborate with influencers on {keyword}",
                f"Run contest related to {keyword}"
            ])
        
        return opportunities[:5]  # Return top 5 opportunities
    
    def generate_recommended_actions(self, keyword: str, score: float, engagement: float) -> List[str]:
        """Generate recommended actions based on trend data"""
        actions = []
        
        # Immediate actions
        actions.extend([
            f"Monitor {keyword} mentions for next 24 hours",
            f"Prepare content calendar around {keyword}",
            f"Research {keyword} audience demographics"
        ])
        
        # Priority-based actions
        if score > 50:
            actions.extend([
                "Create content within next 2 hours",
                "Engage with existing conversations",
                "Share relevant expertise"
            ])
        
        if engagement > 1000:
            actions.extend([
                "Allocate additional resources to this topic",
                "Consider paid promotion",
                "Prepare follow-up content series"
            ])
        
        return actions[:5]  # Return top 5 actions
    
    def format_alert_message(self, alert: TrendAlert) -> str:
        """Format alert message for notification"""
        message = f"""
🚨 TREND ALERT: {self.alert_types[alert.alert_type]}

📊 Keyword: {alert.keyword}
📈 Trend Score: {alert.trend_score:.1f}
💬 Tweet Count: {alert.tweet_count}
🔥 Engagement Score: {alert.engagement_score:.1f}
⏰ Detected: {alert.timestamp.strftime('%Y-%m-%d %H:%M:%S')}

💡 CONTENT OPPORTUNITIES:
{chr(10).join(f"• {opp}" for opp in alert.content_opportunities)}

🎯 RECOMMENDED ACTIONS:
{chr(10).join(f"• {action}" for action in alert.recommended_actions)}

---
Generated by Real-Time Trend Intelligence Hub
        """.strip()
        
        return message
    
    def save_alert(self, alert: TrendAlert):
        """Save alert to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create alerts table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trend_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword TEXT,
                alert_type TEXT,
                trend_score REAL,
                tweet_count INTEGER,
                engagement_score REAL,
                timestamp DATETIME,
                opportunities TEXT,
                actions TEXT,
                status TEXT DEFAULT 'active'
            )
        ''')
        
        cursor.execute('''
            INSERT INTO trend_alerts 
            (keyword, alert_type, trend_score, tweet_count, engagement_score, 
             timestamp, opportunities, actions)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            alert.keyword,
            alert.alert_type,
            alert.trend_score,
            alert.tweet_count,
            alert.engagement_score,
            alert.timestamp,
            json.dumps(alert.content_opportunities),
            json.dumps(alert.recommended_actions)
        ))
        
        conn.commit()
        conn.close()
    
    def run_alert_check(self) -> List[TrendAlert]:
        """Run comprehensive alert check"""
        print("🔍 Running trend alert check...")
        
        all_alerts = []
        
        # Check different types of alerts
        viral_alerts = self.check_viral_trends()
        emerging_alerts = self.check_emerging_topics()
        spike_alerts = self.check_engagement_spikes()
        competitor_alerts = self.check_competitor_activity()
        
        all_alerts.extend(viral_alerts)
        all_alerts.extend(emerging_alerts)
        all_alerts.extend(spike_alerts)
        all_alerts.extend(competitor_alerts)
        
        # Save alerts and format messages
        alert_messages = []
        for alert in all_alerts:
            self.save_alert(alert)
            message = self.format_alert_message(alert)
            alert_messages.append(message)
            print(f"🚨 Alert: {alert.alert_type} for '{alert.keyword}'")
        
        return all_alerts, alert_messages

def main():
    """Main function to run the trend alert system"""
    print("🚨 Trend Alert System")
    print("=" * 30)
    
    # Initialize the alert system
    alert_system = TrendAlertSystem()
    
    # Run alert check
    alerts, messages = alert_system.run_alert_check()
    
    # Save alert summary
    alert_summary = {
        'timestamp': datetime.datetime.now().isoformat(),
        'total_alerts': len(alerts),
        'alert_types': {alert_type: len([a for a in alerts if a.alert_type == alert_type]) 
                       for alert_type in alert_system.alert_types.keys()},
        'alerts': [
            {
                'keyword': alert.keyword,
                'type': alert.alert_type,
                'score': alert.trend_score,
                'engagement': alert.engagement_score,
                'opportunities': alert.content_opportunities,
                'actions': alert.recommended_actions
            }
            for alert in alerts
        ],
        'messages': messages
    }
    
    with open('/home/ubuntu/trend_alerts.json', 'w') as f:
        json.dump(alert_summary, f, indent=2, default=str)
    
    print(f"\n✅ Alert check complete!")
    print(f"🚨 Generated {len(alerts)} alerts")
    print(f"📊 Alert breakdown: {alert_summary['alert_types']}")
    print(f"💾 Results saved to trend_alerts.json")

if __name__ == "__main__":
    main()

