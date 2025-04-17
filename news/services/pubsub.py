from google.cloud import pubsub_v1
from django.conf import settings
import json
import logging
from typing import Dict, Any
from datetime import datetime
from subscribers.models import Subscriber
from asgiref.sync import sync_to_async
import asyncio

logger = logging.getLogger(__name__)

class NewsletterPublisher:
    """Handles publishing news articles to Google Cloud Pub/Sub for newsletter processing."""
    
    def __init__(self):
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(
            settings.GCP_PROJECT_ID,
            settings.NEWSLETTER_TOPIC_ID
        )
    
    def _serialize_datetime(self, dt: datetime) -> str:
        """Serialize datetime objects to ISO format."""
        return dt.isoformat() if dt else None

    def create_message_data(self, news_article) -> Dict[str, Any]:
        """
        Create the message payload from a news article.
        
        Args:
            news_article: News model instance
            
        Returns:
            Dict containing the message data
        """
        # Get active subscribers who want news updates
        subscribers = Subscriber.objects.filter(
            subscription_type='news',
            is_active=True
        ).values_list('email', flat=True)

        # Get the full URL including domain
        site_url = settings.SITE_URL.rstrip('/')  # Remove trailing slash if present
        article_url = news_article.get_absolute_url().lstrip('/')  # Remove leading slash if present
        full_url = f"{site_url}/{article_url}"

        return {
            "news_id": news_article.id,
            "title": news_article.title,
            "summary": news_article.summary or "",  # Ensure we don't send None
            "content": news_article.content or "",
            "author": news_article.author or "TravelTAF Team",
            "published_date": self._serialize_datetime(news_article.published_date),
            "category": news_article.category.name if news_article.category else "Uncategorized",
            "url": full_url,
            "source_name": news_article.source_name or "TravelTAF",
            "source_url": news_article.source_url or "",
            "subscribers": list(subscribers)  # Convert QuerySet to list for serialization
        }

    def publish_newsletter_sync(self, news_article) -> str:
        """
        Synchronously publish a news article to the newsletter topic.
        
        Args:
            news_article: News model instance
            
        Returns:
            The published message ID
            
        Raises:
            Exception: If publishing fails
        """
        try:
            message_data = self.create_message_data(news_article)
            data = json.dumps(message_data).encode("utf-8")
            
            # Publish the message
            future = self.publisher.publish(
                self.topic_path,
                data,
                news_id=str(news_article.id),  # Add custom attributes
                content_type="application/json"
            )
            
            # Get the message ID
            message_id = future.result()
            
            logger.info(
                f"Published newsletter message for news ID {news_article.id} "
                f"with message ID {message_id}"
            )
            
            return message_id
            
        except Exception as e:
            logger.error(
                f"Failed to publish newsletter for news ID {news_article.id}: {str(e)}"
            )
            raise

    async def publish_newsletter(self, news_article) -> str:
        """
        Asynchronously publish a news article to the newsletter topic.
        This method can be called from both sync and async contexts.
        
        Args:
            news_article: News model instance
            
        Returns:
            The published message ID
            
        Raises:
            Exception: If publishing fails
        """
        try:
            # Run the sync version in a thread to avoid blocking
            loop = asyncio.get_event_loop()
            message_id = await loop.run_in_executor(None, self.publish_newsletter_sync, news_article)
            return message_id
        except Exception as e:
            logger.error(
                f"Failed to publish newsletter for news ID {news_article.id}: {str(e)}"
            )
            raise 