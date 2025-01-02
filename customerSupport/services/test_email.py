from django.core.mail import send_mail
import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load environment variables
load_dotenv()

def send_test_email():
    try:
        # Get email settings from environment variables
        smtp_server = "smtp.gmail.com"
        port = 587
        sender = os.getenv('EMAIL_HOST_USER')
        password = os.getenv('EMAIL_HOST_PASSWORD')
        recipient = 'esaathings@gmail.com'

        # Create message
        message = MIMEMultipart()
        message["From"] = sender
        message["To"] = recipient
        message["Subject"] = "Test Email from Python"

        # Add body
        body = "This is a test email sent from Python using SMTP."
        message.attach(MIMEText(body, "plain"))

        # Create SMTP session
        print("Connecting to SMTP server...")
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()  # Enable TLS
        
        print("Logging in...")
        server.login(sender, password)
        
        print("Sending email...")
        server.send_message(message)
        
        print("✅ Test email sent successfully!")
        
        # Close the connection
        server.quit()
            
    except Exception as e:
        print(f"❌ Error sending email: {str(e)}")

if __name__ == "__main__":
    print("Starting email test...")
    send_test_email() 