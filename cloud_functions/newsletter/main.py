import base64
import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from datetime import datetime

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
        if 'data' not in event:
            raise ValueError("No data found in Pub/Sub message")
            
        pubsub_data = base64.b64decode(event['data']).decode('utf-8')
        news_data = json.loads(pubsub_data)
        logger.info(f"Received news data: {news_data}")

        # Validate required fields
        required_fields = ['title', 'summary', 'url', 'author', 'subscribers']
        missing_fields = [field for field in required_fields if not news_data.get(field)]
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

        # Get Gmail credentials from environment variables
        gmail_user = os.environ.get('GMAIL_USER')
        gmail_app_password = os.environ.get('GMAIL_APP_PASSWORD')
        
        if not gmail_user or not gmail_app_password:
            raise ValueError("Gmail credentials not properly configured")
            
        logger.info(f"Attempting to send email using account: {gmail_user}")

        subscribers = news_data.get('subscribers', [])
        if not subscribers:
            logger.warning("No active subscribers found")
            return {
                'status': 'success',
                'message': 'No active subscribers to send to'
            }

        # Create email content
        email_content = create_email_content(news_data)
        
        # Create message
        message = MIMEMultipart('alternative')
        message['Subject'] = f"TravelTAF News: {news_data['title']}"
        message['From'] = f"TravelTAF News <{gmail_user}>"
        message['To'] = gmail_user  # Set To as the sender
        message['Bcc'] = ', '.join(subscribers)  # Add all subscribers in BCC
        
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
            
            # Send to all recipients in one go
            server.send_message(message)
            logger.info(f"Bulk email sent successfully to {len(subscribers)} subscribers")
            
        return {
            'status': 'success',
            'message': f"Newsletter sent successfully to {len(subscribers)} subscribers"
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
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
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
                background-color: #1980e6;
                padding: 20px;
                text-align: center;
                border-radius: 5px;
                color: white;
            }}
            .content {{
                padding: 20px 0;
                background-color: white;
            }}
            .article-meta {{
                color: #666;
                font-size: 0.9em;
                margin: 10px 0;
            }}
            .summary {{
                background-color: #f8f9fa;
                padding: 15px;
                border-radius: 5px;
                margin: 20px 0;
            }}
            .footer {{
                text-align: center;
                padding: 20px;
                font-size: 0.8em;
                color: #666;
                border-top: 1px solid #eee;
                margin-top: 20px;
            }}
            .button {{
                display: inline-block;
                padding: 12px 24px;
                background-color: #1980e6;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                margin-top: 20px;
                font-weight: bold;
            }}
            .button:hover {{
                background-color: #1666b8;
            }}
            @media only screen and (max-width: 600px) {{
                body {{
                    padding: 10px;
                }}
                .header {{
                    padding: 15px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>{news_data['title']}</h1>
        </div>
        
        <div class="content">
            <div class="article-meta">
                <p>By {news_data['author']} | Category: {news_data['category']}</p>
            </div>
            
            <div class="summary">
                <p><strong>Summary:</strong></p>
                <p>{news_data['summary']}</p>
            </div>
            
            <p>We've published a new article that might interest you. Click below to read the full story on our website:</p>
            
            <div style="text-align: center;">
                <a href="{news_data['url']}" class="button">Read Full Article</a>
            </div>
        </div>
        
        <div class="footer">
            <p>You received this email because you subscribed to TravelTAF news updates.</p>
            <p>© {news_data.get('source_name', 'TravelTAF')} {datetime.now().year}</p>
            <p><small>If you no longer wish to receive these emails, please visit our website to manage your subscription.</small></p>
        </div>
    </body>
    </html>
    """ 