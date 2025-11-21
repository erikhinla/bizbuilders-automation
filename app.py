#!/usr/bin/env python3
"""
BizBuilders AI - Content Generation API
Powered by Anthropic Claude for intelligent social media content creation
"""

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import logging
from anthropic import Anthropic

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Anthropic client
anthropic_key = os.getenv('ANTHROPIC_API_KEY')
if anthropic_key:
    anthropic_client = Anthropic(api_key=anthropic_key)
    logger.info("Anthropic client initialized successfully")
else:
    anthropic_client = None
    logger.warning("ANTHROPIC_API_KEY not found - content generation will be limited")

# Health check
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'bizbuilders-automation',
        'version': '2.0.0',
        'anthropic_available': anthropic_client is not None
    }), 200

# Root endpoint
@app.route('/', methods=['GET'])
def root():
    return jsonify({
        'message': 'BizBuilders AI Content Generation API',
        'powered_by': 'Anthropic Claude',
        'endpoints': {
            '/health': 'Health check (GET)',
            '/api/generate/post': 'Generate social media post (POST)',
            '/api/generate/thread': 'Generate thread/carousel (POST)',
            '/api/generate/variants': 'Generate content variants (POST)',
            '/api/optimize': 'Optimize existing content (POST)'
        }
    }), 200

# Generate social media post
@app.route('/api/generate/post', methods=['POST'])
def generate_post():
    try:
        if not anthropic_client:
            return jsonify({'error': 'Anthropic API not configured'}), 503
        
        data = request.get_json()
        topic = data.get('topic', '')
        platform = data.get('platform', 'linkedin')
        tone = data.get('tone', 'professional')
        
        if not topic:
            return jsonify({'error': 'Topic is required'}), 400
        
        prompt = f"""Generate a compelling {platform} post about: {topic}

Tone: {tone}
Requirements:
- Engaging hook
- Value-driven content
- Clear call-to-action
- Appropriate length for {platform}
- Include relevant hashtags

Generate only the post content, no explanations."""
        
        message = anthropic_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        
        content = message.content[0].text
        
        return jsonify({
            'success': True,
            'content': content,
            'platform': platform,
            'topic': topic,
            'model': 'claude-3-5-sonnet'
        }), 200
        
    except Exception as e:
        logger.error(f"Error generating post: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Generate content thread
@app.route('/api/generate/thread', methods=['POST'])
def generate_thread():
    try:
        if not anthropic_client:
            return jsonify({'error': 'Anthropic API not configured'}), 503
        
        data = request.get_json()
        topic = data.get('topic', '')
        num_posts = data.get('num_posts', 5)
        platform = data.get('platform', 'twitter')
        
        if not topic:
            return jsonify({'error': 'Topic is required'}), 400
        
        prompt = f"""Create a {num_posts}-part thread for {platform} about: {topic}

Requirements:
- Each post should be cohesive yet standalone
- Build narrative progression
- Include engaging hooks
- End with strong CTA

Format as JSON array of posts."""
        
        message = anthropic_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}]
        )
        
        content = message.content[0].text
        
        return jsonify({
            'success': True,
            'thread': content,
            'num_posts': num_posts,
            'topic': topic
        }), 200
        
    except Exception as e:
        logger.error(f"Error generating thread: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Generate content variants
@app.route('/api/generate/variants', methods=['POST'])
def generate_variants():
    try:
        if not anthropic_client:
            return jsonify({'error': 'Anthropic API not configured'}), 503
        
        data = request.get_json()
        original = data.get('content', '')
        num_variants = data.get('num_variants', 3)
        
        if not original:
            return jsonify({'error': 'Content is required'}), 400
        
        prompt = f"""Generate {num_variants} unique variants of this content:

{original}

Requirements:
- Maintain core message
- Vary tone and structure
- Keep platform best practices
- Different hooks/angles

Return as numbered list."""
        
        message = anthropic_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}]
        )
        
        variants = message.content[0].text
        
        return jsonify({
            'success': True,
            'original': original,
            'variants': variants,
            'count': num_variants
        }), 200
        
    except Exception as e:
        logger.error(f"Error generating variants: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Optimize content
@app.route('/api/optimize', methods=['POST'])
def optimize_content():
    try:
        if not anthropic_client:
            return jsonify({'error': 'Anthropic API not configured'}), 503
        
        data = request.get_json()
        content = data.get('content', '')
        goal = data.get('goal', 'engagement')
        
        if not content:
            return jsonify({'error': 'Content is required'}), 400
        
        prompt = f"""Optimize this content for {goal}:

{content}

Provide:
1. Optimized version
2. Key improvements made
3. Engagement score (1-10)

Focus on hooks, clarity, and call-to-action."""
        
        message = anthropic_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1536,
            messages=[{"role": "user", "content": prompt}]
        )
        
        optimization = message.content[0].text
        
        return jsonify({
            'success': True,
            'original': content,
            'optimization': optimization,
            'goal': goal
        }), 200
        
    except Exception as e:
        logger.error(f"Error optimizing content: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(
        host='0.0.0.0',
        port=port,
        debug=os.getenv('FLASK_DEBUG', 'False') == 'True'
    )
