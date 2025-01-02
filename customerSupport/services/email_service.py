from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class EmailService:
    @staticmethod
    def send_form_submission_email(form_data, form_type):
        """
        Send email notification for form submissions
        form_type can be 'study_abroad' or 'moving_abroad'
        """
        # Validate required fields
        required_fields = ['full_name', 'email']
        if not all(field in form_data for field in required_fields):
            return False, "Missing required fields"

        try:
            # Email to admin
            admin_subject = f'New {form_type.replace("_", " ").title()} Form Submission'
            admin_message = render_to_string('emails/admin_notification.html', {
                'form_type': form_type,
                'form_data': form_data
            })
            
            send_mail(
                subject=admin_subject,
                message='',
                html_message=admin_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=False
            )

            # Email to user
            user_subject = f'Thank you for your {form_type.replace("_", " ")} inquiry'
            user_message = render_to_string('emails/user_confirmation.html', {
                'name': form_data.get('full_name', 'there'),
                'form_type': form_type
            })
            
            send_mail(
                subject=user_subject,
                message='',
                html_message=user_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[form_data['email']],
                fail_silently=False
            )
            
            return True, "Emails sent successfully"
            
        except Exception as e:
            logger.error(f"Error sending emails: {str(e)}")
            return False, str(e)
