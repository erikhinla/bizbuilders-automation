#!/usr/bin/env python3
"""
Daily Briefing System
Automated daily trend briefings for content creation team
"""

import sys
import json
import datetime
import sqlite3
from typing import Dict, Any, List, Optional
from collections import Counter, defaultdict
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from dataclasses import dataclass

# Add the Manus API client path
sys.path.append('/opt/.manus/.sandbox-runtime')
from data_api import ApiClient

@dataclass
class DailyInsight:
    """Data class for daily insights"""
    date: datetime.date
    top_trends: List[Dict[str, Any]]
    viral_content: List[Dict[str, Any]]
    content_patterns: List[Dict[str, Any]]
    competitor_insights: List[Dict[str, Any]]
    recommendations: List[str]
    opportunities: List[str]

class DailyBriefingSystem:
    def __init__(self, db_path: str = "/home/ubuntu/trend_intelligence.db"):
        """Initialize the daily briefing system"""
        self.client = ApiClient()
        self.db_path = db_path
        
    def get_top_trends(self, date: datetime.date, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top trending topics for a specific date"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT keyword, AVG(trend_score) as avg_score, 
                   SUM(tweet_count) as total_tweets,
                   AVG(engagement_score) as avg_engagement,
                   COUNT(*) as mentions
            FROM trending_topics 
            WHERE DATE(timestamp) = ?
            GROUP BY keyword
            ORDER BY avg_score DESC, total_tweets DESC
            LIMIT ?
        ''', (date, limit))
        
        trends = cursor.fetchall()
        conn.close()
        
        return [
            {
                'keyword': trend[0],
                'trend_score': round(trend[1], 2) if trend[1] else 0,
                'tweet_count': trend[2] if trend[2] else 0,
                'avg_engagement': round(trend[3], 2) if trend[3] else 0,
                'mentions': trend[4],
                'growth_indicator': self.calculate_growth_indicator(trend[0], date)
            }
            for trend in trends
        ]
    
    def get_viral_content(self, date: datetime.date, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top viral content for a specific date"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT username, content, engagement_rate, content_type, 
                   retweet_count, like_count, reply_count, keywords
            FROM viral_content 
            WHERE DATE(timestamp) = ?
            ORDER BY engagement_rate DESC
            LIMIT ?
        ''', (date, limit))
        
        content = cursor.fetchall()
        conn.close()
        
        return [
            {
                'username': item[0],
                'content': item[1][:150] + '...' if len(item[1]) > 150 else item[1],
                'engagement_rate': round(item[2], 4),
                'content_type': item[3],
                'retweets': item[4],
                'likes': item[5],
                'replies': item[6],
                'keywords': item[7],
                'total_engagement': item[4] + item[5] + item[6]
            }
            for item in content
        ]
    
    def get_content_patterns(self, date: datetime.date) -> List[Dict[str, Any]]:
        """Analyze content patterns for a specific date"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get content type performance
        cursor.execute('''
            SELECT content_type, AVG(engagement_rate) as avg_engagement,
                   COUNT(*) as count
            FROM viral_content 
            WHERE DATE(timestamp) = ?
            GROUP BY content_type
            ORDER BY avg_engagement DESC
        ''', (date,))
        
        patterns = cursor.fetchall()
        
        # Get posting time analysis
        cursor.execute('''
            SELECT strftime('%H', timestamp) as hour, 
                   AVG(engagement_rate) as avg_engagement,
                   COUNT(*) as count
            FROM viral_content 
            WHERE DATE(timestamp) = ?
            GROUP BY hour
            ORDER BY avg_engagement DESC
            LIMIT 5
        ''', (date,))
        
        time_patterns = cursor.fetchall()
        
        conn.close()
        
        content_patterns = [
            {
                'type': 'content_type',
                'pattern': pattern[0],
                'avg_engagement': round(pattern[1], 4),
                'count': pattern[2],
                'recommendation': self.get_content_type_recommendation(pattern[0], pattern[1])
            }
            for pattern in patterns
        ]
        
        time_patterns_formatted = [
            {
                'type': 'posting_time',
                'pattern': f"{time[0]}:00",
                'avg_engagement': round(time[1], 4),
                'count': time[2],
                'recommendation': f"Consider posting at {time[0]}:00 for higher engagement"
            }
            for time in time_patterns
        ]
        
        return content_patterns + time_patterns_formatted
    
    def get_competitor_insights(self, date: datetime.date) -> List[Dict[str, Any]]:
        """Get competitor insights for a specific date"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Top performing competitors
        cursor.execute('''
            SELECT username, AVG(engagement_rate) as avg_engagement,
                   COUNT(*) as post_count,
                   SUM(retweet_count + like_count + reply_count) as total_engagement
            FROM viral_content 
            WHERE DATE(timestamp) = ?
            GROUP BY username
            ORDER BY avg_engagement DESC
            LIMIT 10
        ''', (date,))
        
        competitors = cursor.fetchall()
        
        # Most used keywords by competitors
        cursor.execute('''
            SELECT keywords, COUNT(*) as usage_count,
                   AVG(engagement_rate) as avg_engagement
            FROM viral_content 
            WHERE DATE(timestamp) = ? AND keywords IS NOT NULL
            GROUP BY keywords
            ORDER BY usage_count DESC, avg_engagement DESC
            LIMIT 5
        ''', (date,))
        
        keyword_usage = cursor.fetchall()
        
        conn.close()
        
        insights = []
        
        # Competitor performance insights
        for comp in competitors:
            insights.append({
                'type': 'competitor_performance',
                'username': comp[0],
                'avg_engagement': round(comp[1], 4),
                'post_count': comp[2],
                'total_engagement': comp[3],
                'insight': f"@{comp[0]} achieved {comp[1]:.2%} avg engagement with {comp[2]} posts"
            })
        
        # Keyword usage insights
        for keyword in keyword_usage:
            insights.append({
                'type': 'keyword_usage',
                'keyword': keyword[0],
                'usage_count': keyword[1],
                'avg_engagement': round(keyword[2], 4),
                'insight': f"'{keyword[0]}' used {keyword[1]} times with {keyword[2]:.2%} avg engagement"
            })
        
        return insights
    
    def calculate_growth_indicator(self, keyword: str, date: datetime.date) -> str:
        """Calculate growth indicator for a keyword"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get current day data
        cursor.execute('''
            SELECT AVG(trend_score) FROM trending_topics 
            WHERE keyword = ? AND DATE(timestamp) = ?
        ''', (keyword, date))
        current_score = cursor.fetchone()[0] or 0
        
        # Get previous day data
        prev_date = date - datetime.timedelta(days=1)
        cursor.execute('''
            SELECT AVG(trend_score) FROM trending_topics 
            WHERE keyword = ? AND DATE(timestamp) = ?
        ''', (keyword, prev_date))
        prev_score = cursor.fetchone()[0] or 0
        
        conn.close()
        
        if prev_score == 0:
            return "🆕 NEW"
        elif current_score > prev_score * 1.2:
            return "📈 RISING"
        elif current_score < prev_score * 0.8:
            return "📉 DECLINING"
        else:
            return "➡️ STABLE"
    
    def get_content_type_recommendation(self, content_type: str, engagement: float) -> str:
        """Get recommendation based on content type performance"""
        recommendations = {
            'media_post': "Visual content performs well - increase image/video posts",
            'question': "Questions drive engagement - use more interactive content",
            'educational': "Educational content resonates - share more tips and guides",
            'announcement': "Announcements get attention - time them strategically",
            'link_share': "Link sharing works - curate valuable external content",
            'long_form': "Long-form content engages - consider thread posts",
            'general': "General posts are versatile - maintain variety"
        }
        
        base_rec = recommendations.get(content_type, "Monitor this content type")
        
        if engagement > 0.01:  # 1% engagement rate
            return f"🔥 HIGH PERFORMING: {base_rec}"
        elif engagement > 0.005:  # 0.5% engagement rate
            return f"✅ GOOD: {base_rec}"
        else:
            return f"⚠️ LOW: Consider optimizing {content_type} strategy"
    
    def generate_recommendations(self, insights: DailyInsight) -> List[str]:
        """Generate actionable recommendations based on insights"""
        recommendations = []
        
        # Trend-based recommendations
        if insights.top_trends:
            top_trend = insights.top_trends[0]
            recommendations.append(
                f"🎯 Focus on '{top_trend['keyword']}' - trending with {top_trend['trend_score']} score"
            )
            
            if top_trend['growth_indicator'] == "📈 RISING":
                recommendations.append(
                    f"⚡ Act fast on '{top_trend['keyword']}' - showing rapid growth"
                )
        
        # Content pattern recommendations
        if insights.content_patterns:
            best_type = max(insights.content_patterns, 
                          key=lambda x: x.get('avg_engagement', 0))
            recommendations.append(
                f"📊 Prioritize {best_type['pattern']} content - highest engagement type"
            )
        
        # Viral content insights
        if insights.viral_content:
            top_viral = insights.viral_content[0]
            recommendations.append(
                f"💡 Study @{top_viral['username']}'s approach - {top_viral['engagement_rate']:.2%} engagement"
            )
        
        # Competitor insights
        competitor_keywords = [c for c in insights.competitor_insights 
                             if c['type'] == 'keyword_usage']
        if competitor_keywords:
            top_keyword = competitor_keywords[0]
            recommendations.append(
                f"🔍 Consider content around '{top_keyword['keyword']}' - competitor focus area"
            )
        
        # General recommendations
        recommendations.extend([
            "📅 Plan content calendar based on top trends",
            "🤝 Engage with trending conversations",
            "📈 Monitor competitor strategies for inspiration",
            "🎨 Test different content formats based on patterns"
        ])
        
        return recommendations[:8]  # Return top 8 recommendations
    
    def generate_opportunities(self, insights: DailyInsight) -> List[str]:
        """Generate content opportunities based on insights"""
        opportunities = []
        
        # Trend opportunities
        for trend in insights.top_trends[:3]:
            if trend['growth_indicator'] in ["📈 RISING", "🆕 NEW"]:
                opportunities.append(
                    f"Create timely content about '{trend['keyword']}' while it's trending"
                )
        
        # Content gap opportunities
        if insights.content_patterns:
            low_performing = [p for p in insights.content_patterns 
                            if p.get('avg_engagement', 0) < 0.005]
            for pattern in low_performing[:2]:
                opportunities.append(
                    f"Improve {pattern['pattern']} content strategy - underperforming"
                )
        
        # Viral content opportunities
        for viral in insights.viral_content[:2]:
            if viral['content_type'] in ['educational', 'question']:
                opportunities.append(
                    f"Create similar {viral['content_type']} content - proven engagement"
                )
        
        # Time-based opportunities
        time_patterns = [p for p in insights.content_patterns 
                        if p['type'] == 'posting_time']
        if time_patterns:
            best_time = time_patterns[0]
            opportunities.append(
                f"Schedule important posts around {best_time['pattern']} for better reach"
            )
        
        return opportunities[:6]  # Return top 6 opportunities
    
    def create_visualization(self, insights: DailyInsight, save_path: str):
        """Create visualization for the daily briefing"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle(f'Daily Trend Intelligence Briefing - {insights.date}', fontsize=16, fontweight='bold')
        
        # Top trends chart
        if insights.top_trends:
            trends = insights.top_trends[:5]
            keywords = [t['keyword'][:15] + '...' if len(t['keyword']) > 15 else t['keyword'] for t in trends]
            scores = [t['trend_score'] for t in trends]
            
            ax1.barh(keywords, scores, color='skyblue')
            ax1.set_xlabel('Trend Score')
            ax1.set_title('Top Trending Keywords')
            ax1.grid(axis='x', alpha=0.3)
        
        # Content type performance
        if insights.content_patterns:
            content_types = [p for p in insights.content_patterns if p['type'] == 'content_type']
            if content_types:
                types = [c['pattern'] for c in content_types]
                engagements = [c['avg_engagement'] * 100 for c in content_types]  # Convert to percentage
                
                ax2.bar(types, engagements, color='lightcoral')
                ax2.set_ylabel('Avg Engagement (%)')
                ax2.set_title('Content Type Performance')
                ax2.tick_params(axis='x', rotation=45)
                ax2.grid(axis='y', alpha=0.3)
        
        # Viral content engagement
        if insights.viral_content:
            viral = insights.viral_content[:5]
            usernames = [v['username'] for v in viral]
            engagements = [v['engagement_rate'] * 100 for v in viral]
            
            ax3.scatter(range(len(usernames)), engagements, s=100, color='gold', alpha=0.7)
            ax3.set_xticks(range(len(usernames)))
            ax3.set_xticklabels(usernames, rotation=45)
            ax3.set_ylabel('Engagement Rate (%)')
            ax3.set_title('Top Viral Content')
            ax3.grid(alpha=0.3)
        
        # Posting time analysis
        time_patterns = [p for p in insights.content_patterns if p['type'] == 'posting_time']
        if time_patterns:
            times = [int(t['pattern'].split(':')[0]) for t in time_patterns]
            engagements = [t['avg_engagement'] * 100 for t in time_patterns]
            
            ax4.plot(times, engagements, marker='o', linewidth=2, markersize=8, color='green')
            ax4.set_xlabel('Hour of Day')
            ax4.set_ylabel('Avg Engagement (%)')
            ax4.set_title('Optimal Posting Times')
            ax4.grid(alpha=0.3)
            ax4.set_xticks(range(0, 24, 2))
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    
    def generate_daily_briefing(self, date: datetime.date = None) -> DailyInsight:
        """Generate comprehensive daily briefing"""
        if date is None:
            date = datetime.date.today()
        
        print(f"📋 Generating daily briefing for {date}")
        
        # Gather all insights
        top_trends = self.get_top_trends(date)
        viral_content = self.get_viral_content(date)
        content_patterns = self.get_content_patterns(date)
        competitor_insights = self.get_competitor_insights(date)
        
        # Create insights object
        insights = DailyInsight(
            date=date,
            top_trends=top_trends,
            viral_content=viral_content,
            content_patterns=content_patterns,
            competitor_insights=competitor_insights,
            recommendations=[],
            opportunities=[]
        )
        
        # Generate recommendations and opportunities
        insights.recommendations = self.generate_recommendations(insights)
        insights.opportunities = self.generate_opportunities(insights)
        
        return insights
    
    def format_briefing_report(self, insights: DailyInsight) -> str:
        """Format briefing as a readable report"""
        report = f"""
# 📊 Daily Trend Intelligence Briefing
## {insights.date.strftime('%A, %B %d, %Y')}

---

## 🔥 TOP TRENDING TOPICS

"""
        
        for i, trend in enumerate(insights.top_trends[:5], 1):
            report += f"""
### {i}. {trend['keyword']} {trend['growth_indicator']}
- **Trend Score:** {trend['trend_score']}
- **Tweet Volume:** {trend['tweet_count']} tweets
- **Avg Engagement:** {trend['avg_engagement']}
- **Mentions:** {trend['mentions']}
"""
        
        report += "\n---\n\n## 🚀 VIRAL CONTENT HIGHLIGHTS\n"
        
        for i, content in enumerate(insights.viral_content[:3], 1):
            report += f"""
### {i}. @{content['username']} ({content['content_type']})
- **Content:** {content['content']}
- **Engagement Rate:** {content['engagement_rate']:.2%}
- **Total Engagement:** {content['total_engagement']:,}
"""
        
        report += "\n---\n\n## 📈 CONTENT PATTERNS\n"
        
        for pattern in insights.content_patterns[:5]:
            report += f"- **{pattern['pattern']}:** {pattern['avg_engagement']:.2%} avg engagement ({pattern['count']} posts)\n"
        
        report += "\n---\n\n## 🎯 RECOMMENDATIONS\n"
        
        for rec in insights.recommendations:
            report += f"- {rec}\n"
        
        report += "\n---\n\n## 💡 CONTENT OPPORTUNITIES\n"
        
        for opp in insights.opportunities:
            report += f"- {opp}\n"
        
        report += "\n---\n\n## 🔍 COMPETITOR INSIGHTS\n"
        
        for insight in insights.competitor_insights[:5]:
            report += f"- {insight['insight']}\n"
        
        report += f"""

---

## 📊 SUMMARY METRICS
- **Total Trends Analyzed:** {len(insights.top_trends)}
- **Viral Content Reviewed:** {len(insights.viral_content)}
- **Content Patterns Identified:** {len(insights.content_patterns)}
- **Competitor Accounts Monitored:** {len(set(c['username'] for c in insights.competitor_insights if 'username' in c))}

---

*Generated by Real-Time Trend Intelligence Hub*
*Report Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
        """
        
        return report.strip()
    
    def save_briefing(self, insights: DailyInsight, base_path: str = "/home/ubuntu"):
        """Save daily briefing in multiple formats"""
        date_str = insights.date.strftime('%Y-%m-%d')
        
        # Save as JSON
        briefing_data = {
            'date': insights.date.isoformat(),
            'top_trends': insights.top_trends,
            'viral_content': insights.viral_content,
            'content_patterns': insights.content_patterns,
            'competitor_insights': insights.competitor_insights,
            'recommendations': insights.recommendations,
            'opportunities': insights.opportunities
        }
        
        json_path = f"{base_path}/daily_briefing_{date_str}.json"
        with open(json_path, 'w') as f:
            json.dump(briefing_data, f, indent=2, default=str)
        
        # Save as markdown report
        report = self.format_briefing_report(insights)
        md_path = f"{base_path}/daily_briefing_{date_str}.md"
        with open(md_path, 'w') as f:
            f.write(report)
        
        # Create visualization
        viz_path = f"{base_path}/daily_briefing_{date_str}_chart.png"
        self.create_visualization(insights, viz_path)
        
        return {
            'json_path': json_path,
            'markdown_path': md_path,
            'visualization_path': viz_path
        }

def main():
    """Main function to generate daily briefing"""
    print("📋 Daily Briefing System")
    print("=" * 30)
    
    # Initialize the briefing system
    briefing_system = DailyBriefingSystem()
    
    # Generate today's briefing
    today = datetime.date.today()
    insights = briefing_system.generate_daily_briefing(today)
    
    # Save briefing
    file_paths = briefing_system.save_briefing(insights)
    
    print(f"\n✅ Daily briefing generated for {today}")
    print(f"📊 Top trends: {len(insights.top_trends)}")
    print(f"🚀 Viral content: {len(insights.viral_content)}")
    print(f"📈 Content patterns: {len(insights.content_patterns)}")
    print(f"🎯 Recommendations: {len(insights.recommendations)}")
    print(f"💡 Opportunities: {len(insights.opportunities)}")
    print(f"\n📁 Files saved:")
    for file_type, path in file_paths.items():
        print(f"  - {file_type}: {path}")

if __name__ == "__main__":
    main()

