#!/usr/bin/env python3
"""
Content Generation Hub API
REST API for managing content generation and queue
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from content_generation_hub import ContentGenerationHub, TrendData
import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# Initialize hub
hub = ContentGenerationHub()

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'ai_configured': bool(hub.config.get('openai_api_key') or hub.config.get('anthropic_api_key'))
    })

@app.route('/api/trends', methods=['GET'])
def get_trends():
    """Get trends from database"""
    limit = request.args.get('limit', 10, type=int)
    trends = hub.get_trends_from_database(limit=limit)
    return jsonify([{
        'keyword': t.keyword,
        'volume': t.volume,
        'growth_rate': t.growth_rate,
        'platform': t.platform,
        'timestamp': t.timestamp,
        'relevance_score': t.relevance_score,
        'source': t.source
    } for t in trends])

@app.route('/api/trends', methods=['POST'])
def add_trend():
    """Add a new trend"""
    data = request.json
    trend = TrendData(
        keyword=data['keyword'],
        volume=data.get('volume', 0),
        growth_rate=data.get('growth_rate', 0.0),
        platform=data.get('platform', 'transformby10x'),
        timestamp=datetime.datetime.now().isoformat(),
        relevance_score=data.get('relevance_score', 0.7),
        source=data.get('source', 'manual')
    )
    hub.add_trend(trend)
    return jsonify({'status': 'success', 'message': 'Trend added'})

@app.route('/api/content', methods=['GET'])
def get_content():
    """Get content from queue"""
    status = request.args.get('status')
    limit = request.args.get('limit', 50, type=int)
    content = hub.get_content_queue(status=status, limit=limit)
    return jsonify([{
        'id': c.id,
        'title': c.title,
        'content': c.content,
        'content_type': c.content_type,
        'platform': c.platform,
        'status': c.status,
        'created_at': c.created_at,
        'scheduled_for': c.scheduled_for,
        'published_at': c.published_at,
        'seo_keywords': c.seo_keywords,
        'metadata': c.metadata
    } for c in content])

@app.route('/api/content/generate', methods=['POST'])
def generate_content():
    """Generate content from a trend"""
    data = request.json
    keyword = data.get('keyword')
    content_types = data.get('content_types', ['social_post'])
    
    if not keyword:
        return jsonify({'error': 'keyword is required'}), 400
    
    # Create trend
    trend = TrendData(
        keyword=keyword,
        volume=data.get('volume', 1000),
        growth_rate=data.get('growth_rate', 0.1),
        platform=data.get('platform', 'transformby10x'),
        timestamp=datetime.datetime.now().isoformat(),
        relevance_score=data.get('relevance_score', 0.8),
        source=data.get('source', 'api')
    )
    
    # Generate content
    content_pieces = hub.generate_content_from_trend(trend, content_types=content_types)
    
    # Save content
    for piece in content_pieces:
        hub.save_content_piece(piece)
    
    return jsonify({
        'status': 'success',
        'generated': len(content_pieces),
        'content': [{
            'id': c.id,
            'title': c.title,
            'content': c.content[:200] + '...' if len(c.content) > 200 else c.content,
            'content_type': c.content_type,
            'platform': c.platform
        } for c in content_pieces]
    })

@app.route('/api/content/<content_id>', methods=['GET'])
def get_content_item(content_id):
    """Get a specific content piece"""
    content_queue = hub.get_content_queue(limit=1000)
    content = next((c for c in content_queue if c.id == content_id), None)
    
    if not content:
        return jsonify({'error': 'Content not found'}), 404
    
    return jsonify({
        'id': content.id,
        'title': content.title,
        'content': content.content,
        'content_type': content.content_type,
        'platform': content.platform,
        'status': content.status,
        'created_at': content.created_at,
        'scheduled_for': content.scheduled_for,
        'published_at': content.published_at,
        'seo_keywords': content.seo_keywords,
        'metadata': content.metadata
    })

@app.route('/api/content/<content_id>/status', methods=['PUT'])
def update_content_status(content_id):
    """Update content status"""
    data = request.json
    new_status = data.get('status')
    
    if not new_status:
        return jsonify({'error': 'status is required'}), 400
    
    # Update in database
    conn = hub.db_path
    import sqlite3
    conn_db = sqlite3.connect(conn)
    cursor = conn_db.cursor()
    
    cursor.execute('''
        UPDATE content_pieces
        SET status = ?
        WHERE id = ?
    ''', (new_status, content_id))
    
    conn_db.commit()
    conn_db.close()
    
    return jsonify({'status': 'success', 'message': f'Content {content_id} updated to {new_status}'})

@app.route('/api/generate/cycle', methods=['POST'])
def run_generation_cycle():
    """Manually trigger a content generation cycle"""
    try:
        hub.run_content_generation_cycle()
        return jsonify({'status': 'success', 'message': 'Generation cycle completed'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/generate-content', methods=['POST'])
def generate_simple_content():
    """Generate content from topic, channel, and count"""
    data = request.json
    topic = data.get('topic')
    channel = data.get('channel', 'linkedin')
    count = data.get('count', 3)
    
    if not topic:
        return jsonify({'error': 'topic is required'}), 400
    
    try:
        import uuid
        posts = []
        
        # Determine which AI to use
        use_anthropic = hub.config.get('anthropic_api_key')
        use_openai = hub.config.get('openai_api_key') and hub.ai_client
        
        if not use_anthropic and not use_openai:
            return jsonify({'error': 'No AI API key configured. Please set OPENAI_API_KEY or ANTHROPIC_API_KEY'}), 400
        
        # Generate posts
        for i in range(int(count)):
            if use_anthropic:
                # Use Anthropic Claude
                try:
                    import anthropic
                    client = anthropic.Anthropic(api_key=hub.config.get('anthropic_api_key'))
                except ImportError:
                    # Fallback to requests if library not installed
                    import requests
                    headers = {
                        "x-api-key": hub.config.get('anthropic_api_key'),
                        "anthropic-version": "2023-06-01",
                        "content-type": "application/json"
                    }
                
                    prompt = f"""Create a social media post about "{topic}" for {channel}.

Requirements:
- Platform: {channel}
- Topic: {topic}
- Make it engaging and valuable
- Include a clear call-to-action
- Keep it appropriate for the platform's character limits

Generate the post content only, no explanations."""
                    
                    data = {
                        "model": "claude-3-5-sonnet-20241022",
                        "max_tokens": 1000,
                        "messages": [{
                            "role": "user",
                            "content": prompt
                        }]
                    }
                    
                    response = requests.post(
                        "https://api.anthropic.com/v1/messages",
                        headers=headers,
                        json=data
                    )
                    
                    if response.status_code == 200:
                        text = response.json()['content'][0]['text']
                    else:
                        raise Exception(f"Anthropic API error: {response.status_code}")
                except Exception as e:
                    # If Anthropic fails, try OpenAI as fallback
                    if use_openai:
                        prompt = f"""Create a social media post about "{topic}" for {channel}.

Requirements:
- Platform: {channel}
- Topic: {topic}
- Make it engaging and valuable
- Include a clear call-to-action
- Keep it appropriate for the platform's character limits

Generate the post content only, no explanations."""
                        
                        response = hub.ai_client.chat.completions.create(
                            model="gpt-4",
                            messages=[
                                {"role": "system", "content": "You are a social media content creator."},
                                {"role": "user", "content": prompt}
                            ],
                            max_tokens=1000,
                            temperature=0.7
                        )
                        
                        text = response.choices[0].message.content if response.choices else ""
                    else:
                        raise e
            else:
                # Use OpenAI
                prompt = f"""Create a social media post about "{topic}" for {channel}.

Requirements:
- Platform: {channel}
- Topic: {topic}
- Make it engaging and valuable
- Include a clear call-to-action
- Keep it appropriate for the platform's character limits

Generate the post content only, no explanations."""
                
                response = hub.ai_client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a social media content creator."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=1000,
                    temperature=0.7
                )
                
                text = response.choices[0].message.content if response.choices else ""
            
            posts.append({
                'id': str(uuid.uuid4()),
                'channel': channel,
                'text': text.strip()
            })
        
        return jsonify({
            'status': 'success',
            'posts': posts
        })
    except Exception as e:
        print(f"Error generating content: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/content', methods=['POST'])
def add_content():
    """Add content to the queue"""
    data = request.json
    
    try:
        import uuid
        content_id = str(uuid.uuid4())
        title = data.get('title', 'Untitled Content')
        content = data.get('content', '')
        content_type = data.get('content_type', 'social_post')
        platform = data.get('platform', 'linkedin')
        status = data.get('status', 'draft')
        seo_keywords = data.get('seo_keywords', [])
        metadata = data.get('metadata', {})
        
        # Create content piece
        from content_generation_hub import ContentPiece
        content_piece = ContentPiece(
            id=content_id,
            title=title,
            content=content,
            content_type=content_type,
            platform=platform,
            status=status,
            created_at=datetime.datetime.now().isoformat(),
            seo_keywords=seo_keywords if isinstance(seo_keywords, list) else [],
            metadata=metadata if isinstance(metadata, dict) else {}
        )
        
        # Save to database
        hub.save_content_piece(content_piece)
        
        return jsonify({
            'status': 'success',
            'id': content_id,
            'message': 'Content added to queue'
        })
    except Exception as e:
        print(f"Error adding content: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get statistics about content generation"""
    import sqlite3
    conn = sqlite3.connect(hub.db_path)
    cursor = conn.cursor()
    
    # Total content
    cursor.execute('SELECT COUNT(*) FROM content_pieces')
    total_content = cursor.fetchone()[0]
    
    # By status
    cursor.execute('SELECT status, COUNT(*) FROM content_pieces GROUP BY status')
    by_status = dict(cursor.fetchall())
    
    # By platform
    cursor.execute('SELECT platform, COUNT(*) FROM content_pieces GROUP BY platform')
    by_platform = dict(cursor.fetchall())
    
    # By content type
    cursor.execute('SELECT content_type, COUNT(*) FROM content_pieces GROUP BY content_type')
    by_type = dict(cursor.fetchall())
    
    conn.close()
    
    return jsonify({
        'total_content': total_content,
        'by_status': by_status,
        'by_platform': by_platform,
        'by_type': by_type
    })

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    print("🚀 Starting Content Generation Hub API...")
    print(f"📡 API available at http://0.0.0.0:{port}")
    print("📚 API Documentation:")
    print("  GET  /api/health - Health check")
    print("  GET  /api/trends - Get trends")
    print("  POST /api/trends - Add trend")
    print("  GET  /api/content - Get content queue")
    print("  POST /api/content/generate - Generate content")
    print("  GET  /api/content/<id> - Get specific content")
    print("  PUT  /api/content/<id>/status - Update content status")
    print("  POST /api/generate/cycle - Run generation cycle")
    print("  GET  /api/stats - Get statistics")
    
    app.run(host='0.0.0.0', port=port, debug=debug)

