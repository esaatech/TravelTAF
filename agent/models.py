from django.db import models
from django.contrib.auth.models import User

class Interaction(models.Model):
    """
    The Interaction model tracks all user interactions with the system, including chat messages
    and call requests. It serves as a central repository for monitoring and analyzing user
    engagement, support quality, and system performance.

    Key Features:
    - Tracks both chat and call interactions
    - Maintains message history with responses
    - Monitors interaction status
    - Associates interactions with users (optional)
    - Records timestamps for analytics

    Use Cases:
    1. Customer Support
       - Review conversation history
       - Track response times
       - Monitor support quality

    2. Analytics
       - User engagement metrics
       - Popular interaction types
       - Peak usage times
       - Response time analysis

    3. System Improvement
       - Identify common queries
       - Analyze successful interactions
       - Monitor completion rates
       - Track user satisfaction
    """

    # Defines the types of interactions possible in the system
    INTERACTION_TYPES = [
        ('chat', 'Chat Message'),  # Text-based chat interactions
        ('call', 'Call Request'),  # Voice call requests
    ]

    # Tracks the current state of each interaction
    STATUS_CHOICES = [
        ('pending', 'Pending'),     # Newly created, awaiting response
        ('processed', 'Processed'), # System has generated a response
        ('completed', 'Completed'), # Interaction successfully concluded
        ('cancelled', 'Cancelled')  # Interaction terminated before completion
    ]

    # Links to Django's built-in User model (optional)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="The user who initiated the interaction. Can be null for anonymous users."
    )

    # The type of interaction (chat or call)
    type = models.CharField(
        max_length=10,
        choices=INTERACTION_TYPES,
        help_text="The type of interaction (chat message or call request)"
    )

    # The user's input message or call details
    message = models.TextField(
        null=True,
        blank=True,
        help_text="The user's message or call details"
    )

    # The system's response to the user
    response = models.TextField(
        null=True,
        blank=True,
        help_text="The system's response to the user's message"
    )

    # Current status of the interaction
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        help_text="The current status of the interaction"
    )

    # Automatically set when the interaction is created
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the interaction was created"
    )

    # Automatically updated whenever the interaction is modified
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the interaction was last modified"
    )

    class Meta:
        ordering = ['-created_at']  # Most recent interactions first
        indexes = [
            models.Index(fields=['type']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
            models.Index(fields=['user']),
        ]
        verbose_name = "User Interaction"
        verbose_name_plural = "User Interactions"

    def __str__(self):
        """
        String representation of the interaction.
        Format: "{type} - {timestamp}"
        """
        return f"{self.type} - {self.created_at}"

    def get_duration(self):
        """
        Calculate the duration of the interaction.
        Returns: Timedelta between creation and last update
        """
        return self.updated_at - self.created_at

    def is_resolved(self):
        """
        Check if the interaction has been resolved.
        Returns: Boolean indicating if status is 'completed' or 'cancelled'
        """
        return self.status in ['completed', 'cancelled']

    def get_response_time(self):
        """
        Calculate the initial response time.
        Returns: Timedelta between creation and first response
        """
        if self.response:
            return self.updated_at - self.created_at
        return None

    @property
    def is_anonymous(self):
        """
        Check if the interaction is from an anonymous user.
        Returns: Boolean indicating if no user is associated
        """
        return self.user is None

    @classmethod
    def get_pending_interactions(cls):
        """
        Get all pending interactions.
        Returns: QuerySet of pending interactions
        """
        return cls.objects.filter(status='pending')

    @classmethod
    def get_user_history(cls, user):
        """
        Get interaction history for a specific user.
        Args:
            user: User object
        Returns: QuerySet of user's interactions
        """
        return cls.objects.filter(user=user)
