"""
Katzu Waitlist API - Flask Backend for Railway
Handles waitlist form submissions and adds them to Notion database
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from notion_client import Client
from datetime import datetime
import os
import logging

# Initialize Flask app
app = Flask(__name__)

# Configure CORS - Allow requests from katzu.org
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://katzu.org", "https://www.katzu.org", "http://katzu.org", "http://www.katzu.org"],
        "methods": ["POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Notion client
notion = Client(auth=os.environ.get("NOTION_TOKEN"))
DATABASE_ID = os.environ.get("NOTION_DATABASE_ID")

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Railway"""
    return jsonify({"status": "healthy", "service": "katzu-waitlist-api"}), 200

@app.route('/api/waitlist', methods=['POST', 'OPTIONS'])
def add_to_waitlist():
    """
    Add a new waitlist entry to Notion database
    
    Expected JSON payload:
    {
        "name": "John Doe",
        "email": "john@example.com",
        "tracker": "Apple Watch" (optional),
        "frequency": "3-4x per week" (optional)
    }
    """
    
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        # Get form data
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Validate required fields
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        
        if not name or not email:
            return jsonify({"error": "Name and email are required"}), 400
        
        # Validate email format (basic check)
        if '@' not in email or '.' not in email:
            return jsonify({"error": "Invalid email format"}), 400
        
        # Optional fields
        tracker = data.get('tracker', '').strip() or 'Not specified'
        frequency = data.get('frequency', '').strip() or 'Not specified'
        
        # Current date/time
        signup_date = datetime.now().isoformat()
        
        # Log the submission
        logger.info(f"New waitlist submission: {name} ({email})")
        
        # Create Notion page (database entry)
        notion.pages.create(
            parent={"database_id": DATABASE_ID},
            properties={
                "Name": {
                    "title": [
                        {
                            "text": {
                                "content": name
                            }
                        }
                    ]
                },
                "Email": {
                    "email": email
                },
                "Fitness Tracker": {
                    "rich_text": [
                        {
                            "text": {
                                "content": tracker
                            }
                        }
                    ]
                },
                "Running Frequency": {
                    "rich_text": [
                        {
                            "text": {
                                "content": frequency
                            }
                        }
                    ]
                },
                "Signup Date": {
                    "date": {
                        "start": signup_date
                    }
                },
                "Status": {
                    "rich_text": [
                        {
                            "text": {
                                "content": "New"
                            }
                        }
                    ]
                }
            }
        )
        
        logger.info(f"Successfully added {email} to Notion database")
        
        return jsonify({
            "success": True,
            "message": "Successfully joined waitlist"
        }), 201
        
    except Exception as e:
        logger.error(f"Error adding to waitlist: {str(e)}")
        return jsonify({
            "error": "Failed to add to waitlist",
            "details": str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    # Check for required environment variables
    if not os.environ.get("NOTION_TOKEN"):
        logger.error("NOTION_TOKEN environment variable not set")
        exit(1)
    
    if not os.environ.get("NOTION_DATABASE_ID"):
        logger.error("NOTION_DATABASE_ID environment variable not set")
        exit(1)
    
    # Get port from environment (Railway provides this)
    port = int(os.environ.get("PORT", 5000))
    
    logger.info(f"Starting Katzu Waitlist API on port {port}")
    app.run(host='0.0.0.0', port=port)
