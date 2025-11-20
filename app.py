#!/usr/bin/env python3
"""
BizBuilders AI - Social Automation API
Flask REST API for content generation and social media automation
"""

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'bizbuilders-automation',
        'version': '1.0.0'
    }), 200

# Root endpoint
@app.route('/', methods=['GET'])
def root():
    return jsonify({
        'message': 'BizBuilders AI Social Automation API',
        'endpoints': {
            '/health': 'Health check',
            '/api/generate': 'Generate content (POST)',
            '/api/schedule': 'Schedule post (POST)',
            '/api/status': 'Get status (GET)'
        }
    }), 200

# Content generation endpoint
@app.route('/api/generate', methods=['POST'])
def generate_content():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Placeholder for content generation logic
        # You'll integrate your modules here
        result = {
            'success': True,
            'message': 'Content generation endpoint',
            'data': data
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error in generate_content: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Schedule post endpoint
@app.route('/api/schedule', methods=['POST'])
def schedule_post():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Placeholder for scheduling logic
        result = {
            'success': True,
            'message': 'Post scheduled successfully',
            'scheduled_time': data.get('scheduled_time', 'now')
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error in schedule_post: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Status endpoint
@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify({
        'status': 'running',
        'active_jobs': 0,
        'completed_jobs': 0
    }), 200

if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.getenv('PORT', 5000))
    
    # Run the app
    app.run(
        host='0.0.0.0',
        port=port,
        debug=os.getenv('FLASK_DEBUG', 'False') == 'True'
    )
