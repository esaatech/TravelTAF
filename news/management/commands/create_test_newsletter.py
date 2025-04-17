from django.core.management.base import BaseCommand
from news.models import News, NewsCategory
from django.utils import timezone
import time

class Command(BaseCommand):
    help = 'Creates a test news article with newsletter flag enabled'

    def handle(self, *args, **kwargs):
        try:
            # Get or create a test category
            category, created = NewsCategory.objects.get_or_create(
                name='Test Category',
                defaults={
                    'slug': 'test-category',
                    'description': 'A test category for newsletter testing'
                }
            )

            # Create a unique slug using timestamp
            timestamp = int(time.time())
            
            # Create a test news article
            news = News.objects.create(
                title=f'Test Newsletter Article {timestamp}',
                slug=f'test-newsletter-article-{timestamp}',
                category=category,
                author='Test Author',
                summary='This is a test article for newsletter functionality.',
                content='<p>This is a detailed content for testing the newsletter functionality. '
                       'This article should trigger the Cloud Function to send an email.</p>',
                is_published=True,
                status='APPROVED',
                send_as_newsletter=True  # This will trigger the newsletter
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created test article "{news.title}" '
                    f'with newsletter flag enabled. '
                    f'Check your test email for the newsletter.'
                )
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating test article: {str(e)}')
            ) 