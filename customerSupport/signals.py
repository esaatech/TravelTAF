from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .services.email_service import EmailManager
import logging

logger = logging.getLogger(__name__)

User = get_user_model()

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    """
    Signal to send welcome email when a new user is created
    """
    if created:  # Only for new users
        try:
            email_manager = EmailManager()
            success, message = email_manager.send_welcome_email({
                'email': instance.email,
                'full_name': f"{instance.get_full_name() or instance.email.split('@')[0]}"
            })
            
            if success:
                logger.info(f"Welcome email sent successfully to {instance.email}")
            else:
                logger.error(f"Failed to send welcome email to {instance.email}: {message}")
                
        except Exception as e:
            logger.error(f"Error in welcome email signal for {instance.email}: {str(e)}") 