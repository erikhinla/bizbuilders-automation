#!/usr/bin/env python3
"""
Test script for content generation hub
"""

from content_generation_hub import ContentGenerationHub, TrendData
import datetime

def main():
    print("🧪 Testing Content Generation Hub")
    print("=" * 60)
    
    # Initialize hub
    hub = ContentGenerationHub()
    
    # Check if AI is configured
    has_ai = bool(hub.config.get('openai_api_key') or hub.config.get('anthropic_api_key'))
    if has_ai:
        print("✅ AI API configured - will use AI generation")
    else:
        print("⚠️ No AI API key - will use template generation")
        print("   Set OPENAI_API_KEY or ANTHROPIC_API_KEY to use AI")
    
    # Add test trends
    test_trends = [
        TrendData(
            keyword="AI-powered business automation",
            volume=5000,
            growth_rate=0.25,
            platform="transformby10x",
            timestamp=datetime.datetime.now().isoformat(),
            relevance_score=0.85,
            source="test"
        ),
        TrendData(
            keyword="Entrepreneurship tools for startups",
            volume=3000,
            growth_rate=0.15,
            platform="bizbuilders",
            timestamp=datetime.datetime.now().isoformat(),
            relevance_score=0.75,
            source="test"
        )
    ]
    
    print("\n📊 Adding test trends...")
    for trend in test_trends:
        hub.add_trend(trend)
        print(f"  ✅ Added: {trend.keyword}")
    
    # Generate content
    print("\n🚀 Generating content...")
    for trend in test_trends:
        print(f"\n📝 Generating for: {trend.keyword}")
        content_pieces = hub.generate_content_from_trend(
            trend, 
            content_types=['social_post']
        )
        
        for piece in content_pieces:
            hub.save_content_piece(piece)
            print(f"  ✅ Generated {piece.content_type} for {piece.platform}")
            print(f"     Title: {piece.title}")
            print(f"     Content preview: {piece.content[:100]}...")
    
    # Show queue
    print("\n📋 Content Queue:")
    content_queue = hub.get_content_queue(limit=10)
    print(f"Total content pieces: {len(content_queue)}")
    for content in content_queue:
        print(f"  - [{content.status}] {content.content_type}/{content.platform}: {content.title}")
    
    print("\n✅ Test complete!")

if __name__ == "__main__":
    main()

