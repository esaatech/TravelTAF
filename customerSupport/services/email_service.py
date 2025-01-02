import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from jinja2 import Template
import logging

logger = logging.getLogger(__name__)

class EmailManager:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.port = 587
        self.sender = os.getenv('EMAIL_HOST_USER')
        self.password = os.getenv('EMAIL_HOST_PASSWORD')
        
        # Template paths
        self.template_dir = Path(__file__).parent.parent / 'templates' / 'emails'
        
        # Available templates
        self.templates = {
            'study_abroad': 'study_abroad_submission.html',
            'moving_abroad': 'moving_abroad_submission.html',
            'consultation': 'consultation_confirmation.html',
            'welcome': 'welcome.html'
        }
    
    def send_email(self, to_email, subject, template_name, context=None):
        """
        Send an email using a template
        
        Args:
            to_email (str): Recipient email
            subject (str): Email subject
            template_name (str): Name of template to use
            context (dict): Data to pass to template
        """
        try:
            # Create message
            message = MIMEMultipart()
            message["From"] = self.sender
            message["To"] = to_email
            message["Subject"] = subject

            # Get and render template
            template_path = self.template_dir / self.templates.get(template_name, 'default.html')
            with open(template_path, 'r') as f:
                template = Template(f.read())
                html_content = template.render(**(context or {}))

            # Attach HTML content
            message.attach(MIMEText(html_content, "html"))

            # Create SMTP session and send
            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.starttls()
                server.login(self.sender, self.password)
                server.send_message(message)

            logger.info(f"Email sent successfully to {to_email}")
            return True, "Email sent successfully"

        except Exception as e:
            error_msg = f"Failed to send email: {str(e)}"
            logger.error(error_msg)
            return False, error_msg

    def send_study_abroad_confirmation(self, user_data):
        """Helper method for study abroad submissions"""
        return self.send_email(
            to_email=user_data['email'],
            subject="Your Study Abroad Application",
            template_name="study_abroad",
            context={
                "name": user_data.get('full_name', 'there'),
                "countries": user_data.get('target_countries', []),
                "program": user_data.get('preferred_program', ''),
            }
        )

    def send_moving_abroad_confirmation(self, user_data):
        """Helper method for moving abroad submissions"""
        return self.send_email(
            to_email=user_data['email'],
            subject="Your Moving Abroad Application",
            template_name="moving_abroad",
            context={
                "name": user_data.get('full_name', 'there'),
                "countries": user_data.get('target_countries', []),
                "timeline": user_data.get('timeline', ''),
            }
        )

    def send_welcome_email(self, user_data):
        """Helper method for welcome emails"""
        return self.send_email(
            to_email=user_data['email'],
            subject="Welcome to TravelTAF!",
            template_name="welcome",
            context={
                "name": user_data.get('full_name', 'there'),
            }
        )
