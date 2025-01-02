from django.test import TestCase, override_settings
from django.core import mail
from django.conf import settings
from customerSupport.services.email_service import EmailService

@override_settings(
    EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend',
    DEFAULT_FROM_EMAIL='test@example.com',
    ADMIN_EMAIL='admin@example.com'
)
class EmailServiceTest(TestCase):
    def setUp(self):
        self.sample_study_abroad_data = {
            'full_name': 'John Doe',
            'email': 'esaathings@gmail.com',
            'phone': '+6132408100',
            'age': '22',
            'education_level': 'bachelors',
            'field_of_study': 'Computer Science',
            'target_countries': ['canada', 'australia'],
            'preferred_program': 'Masters'
        }
        
        self.sample_moving_abroad_data = {
            'full_name': 'Jane Smith',
            'email': 'esaathings@gmail.com',
            'phone': '+1987654321',
            'age': '28',
            'marital_status': 'single',
            'primary_language': 'english',
            'target_countries': ['uk', 'germany'],
            'timeline': '6months'
        }

    def test_study_abroad_email_sending(self):
        success, message = EmailService.send_form_submission_email(
            self.sample_study_abroad_data, 
            'study_abroad'
        )
        
        # Print the outbox for debugging
        print("\n=== Email Outbox Contents ===")
        for email in mail.outbox:
            print(f"\nSubject: {email.subject}")
            print(f"To: {email.to}")
            print(f"From: {email.from_email}")
            print("Body preview:", email.body[:100] if email.body else "No plain text body")
            print("HTML preview:", email.alternatives[0][0][:100] if email.alternatives else "No HTML body")
        print("===========================\n")
        
        # Check if emails were sent
        self.assertTrue(success)
        self.assertEqual(len(mail.outbox), 2)  # Two emails: admin and user
        
        # Check admin email
        admin_email = mail.outbox[0]
        self.assertEqual(admin_email.subject, 'New Study Abroad Form Submission')
        self.assertEqual(admin_email.to, [settings.ADMIN_EMAIL])
        
        # Check user email
        user_email = mail.outbox[1]
        self.assertEqual(user_email.subject, 'Thank you for your study abroad inquiry')
        self.assertEqual(user_email.to, ['esaathings@gmail.com'])

    def test_moving_abroad_email_sending(self):
        success, message = EmailService.send_form_submission_email(
            self.sample_moving_abroad_data, 
            'moving_abroad'
        )
        
        # Check if emails were sent
        self.assertTrue(success)
        self.assertEqual(len(mail.outbox), 2)
        
        # Check admin email
        admin_email = mail.outbox[0]
        self.assertEqual(admin_email.subject, 'New Moving Abroad Form Submission')
        self.assertEqual(admin_email.to, [settings.ADMIN_EMAIL])
        
        # Check user email
        user_email = mail.outbox[1]
        self.assertEqual(user_email.subject, 'Thank you for your moving abroad inquiry')
        self.assertEqual(user_email.to, ['esaathings@gmail.com'])

    def test_email_sending_failure(self):
        # Test with invalid email
        invalid_data = self.sample_study_abroad_data.copy()
        invalid_data['email'] = 'invalid-email'
        
        success, message = EmailService.send_form_submission_email(
            invalid_data, 
            'study_abroad'
        )
        
        self.assertFalse(success)
        self.assertTrue(isinstance(message, str)) 