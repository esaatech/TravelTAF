import base64
import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def send_newsletter(event, context):
    """Cloud Function triggered by Pub/Sub event.
    
    Args:
        event (dict): The dictionary with data specific to this type of event.
        context (google.cloud.functions.Context): The Cloud Functions event
            metadata.
    """
    try:
        # Extract data from the Pub/Sub message
        if 'data' in event:
            pubsub_data = base64.b64decode(event['data']).decode('utf-8')
            news_data = json.loads(pubsub_data)
            logger.info(f"Received news data: {news_data}")
        else:
            raise ValueError("No data found in Pub/Sub message")

        # Get Gmail credentials from environment variables
        gmail_user = os.environ.get('GMAIL_USER')
        gmail_app_password = os.environ.get('GMAIL_APP_PASSWORD')
        
        if not gmail_user or not gmail_app_password:
            raise ValueError("Gmail credentials not properly configured")
            
        logger.info(f"Attempting to send email using account: {gmail_user}")

        # Create email content
        email_content = create_email_content(news_data)
        
        # Get test recipient email
        recipient_email = os.environ.get('TEST_EMAIL', 'test@example.com')
        
        # Create message
        message = MIMEMultipart('alternative')
        message['Subject'] = f"Newsletter: {news_data['title']}"
        message['From'] = gmail_user
        message['To'] = recipient_email
        
        # Attach HTML content
        html_part = MIMEText(email_content, 'html')
        message.attach(html_part)
        
        # Send email using Gmail SMTP with TLS
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            logger.info("Attempting Gmail login...")
            server.login(gmail_user, gmail_app_password)
            logger.info("Gmail login successful")
            server.send_message(message)
            logger.info(f"Email sent successfully to {recipient_email}")
            
        return {
            'status': 'success',
            'message': f"Newsletter sent successfully for article: {news_data['title']}"
        }
        
    except Exception as e:
        error_message = f"Error processing newsletter: {str(e)}"
        logger.error(error_message)
        raise Exception(error_message)

def create_email_content(news_data):
    """Creates HTML content for the newsletter email.
    
    Args:
        news_data (dict): The news article data from Pub/Sub message
        
    Returns:
        str: HTML content for the email
    """
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                background-color: #f8f9fa;
                padding: 20px;
                text-align: center;
                border-radius: 5px;
            }}
            .content {{
                padding: 20px 0;
            }}
            .footer {{
                text-align: center;
                padding: 20px;
                font-size: 0.8em;
                color: #666;
            }}
            .button {{
                display: inline-block;
                padding: 10px 20px;
                background-color: #007bff;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>{news_data['title']}</h1>
            <p>By {news_data['author']}</p>
        </div>
        
        <div class="content">
            <p><strong>Summary:</strong></p>
            <p>{news_data['summary']}</p>
            
            <p><strong>Category:</strong> {news_data['category']}</p>
            
            <a href="{news_data['url']}" class="button">Read More</a>
        </div>
        
        <div class="footer">
            <p>You received this email because you subscribed to our newsletter.</p>
            <p>To unsubscribe, please click <a href="#">here</a>.</p>
        </div>
    </body>
    </html>
    """ 