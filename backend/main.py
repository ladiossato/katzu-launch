"""
Katzu Waitlist & Contact API - Flask Backend for Railway
Handles waitlist form submissions and contact form, adds them to Notion database
Sends contact form emails to hello@katzu.app
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from notion_client import Client
from datetime import datetime
import os
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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

@app.route('/api/contact', methods=['POST', 'OPTIONS'])
def contact():
    """
    Handle contact form submission
    
    Expected JSON payload:
    {
        "name": "John Doe",
        "email": "john@example.com",
        "message": "Message content"
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
        message = data.get('message', '').strip()
        
        if not name or not email or not message:
            return jsonify({"error": "Name, email, and message are required"}), 400
        
        # Validate email format
        if '@' not in email or '.' not in email:
            return jsonify({"error": "Invalid email format"}), 400
        
        logger.info(f"New contact form submission from: {name} ({email})")
        
        # Send email
        try:
            send_contact_email(name, email, message)
            logger.info(f"Contact email sent successfully to hello@katzu.app")
        except Exception as e:
            logger.error(f"Failed to send contact email: {str(e)}")
            # Continue even if email fails - we still want to log it
        
        return jsonify({
            "success": True,
            "message": "Message sent successfully"
        }), 200
        
    except Exception as e:
        logger.error(f"Error processing contact form: {str(e)}")
        return jsonify({
            "error": "Failed to send message",
            "details": str(e)
        }), 500

def send_contact_email(name, from_email, message):
    """
    Send contact form submission via email to hello@katzu.app
    Uses SMTP configuration from environment variables
    """
    # Email configuration from environment variables
    smtp_server = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    smtp_username = os.environ.get("SMTP_USERNAME")
    smtp_password = os.environ.get("SMTP_PASSWORD")
    to_email = "hello@katzu.app"
    
    if not smtp_username or not smtp_password:
        raise Exception("SMTP credentials not configured")
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = to_email
    msg['Subject'] = f"Katzu Contact Form - {name}"
    msg['Reply-To'] = from_email
    
    # Email body
    body = f"""
New contact form submission from Katzu website:

Name: {name}
Email: {from_email}

Message:
{message}

---
This email was sent from the Katzu contact form.
Reply directly to this email to respond to {name}.
    """
    
    msg.attach(MIMEText(body, 'plain'))
    
    # Send email
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)
    server.send_message(msg)
    server.quit()

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
