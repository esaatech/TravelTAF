from decimal import Decimal
from django.db import models
from django.conf import settings
from payments.models import BasePayment
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

class CreditPayment(BasePayment):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def get_failure_url(self):
        return f'/credits/payment/failed/{self.pk}'

    def get_success_url(self):
        return f'/credits/payment/success/{self.pk}'

    def get_purchased_items(self):
        return [{
            'name': f'Credit Purchase - {self.description}',
            'sku': 'CREDITS',
            'quantity': 1,
            'price': Decimal(self.total),
            'currency': self.currency,
        }]

    def handle_payment_status_change(self, old_status, new_status):
        from .add_user_credit import add_credits_to_user
        if new_status == 'confirmed' and not self.extra_data.get('credits_added'):
            add_credits_to_user(self.user, self.total)
            self.extra_data = {'credits_added': True}
            self.save()

class UserCredit(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.balance} credits"

class CreditTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('PURCHASE', 'Purchase'),
        ('USAGE', 'Usage'),
        ('REFUND', 'Refund'),
        ('BONUS', 'Bonus'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    payment = models.ForeignKey(CreditPayment, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255)
    payment_intent_id = models.CharField(max_length=255, null=True, blank=True)
    currency = models.CharField(max_length=3, default='USD')
    stripe_invoice_id = models.CharField(max_length=255, null=True, blank=True)
    invoice_url = models.URLField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} - {self.transaction_type} - {self.amount}"

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_credit_with_bonus(sender, instance, created, **kwargs):
    """
    Signal to create UserCredit with 100 bonus credits when a new user is created
    """
    if created:  # Only when a new user is created
        # Create UserCredit with initial balance
        user_credit, _ = UserCredit.objects.get_or_create(
            user=instance,
            defaults={'balance': Decimal('100.00')}
        )

        # Create transaction record for the welcome bonus
        CreditTransaction.objects.create(
            user=instance,
            amount=Decimal('100.00'),
            transaction_type='BONUS',
            description='Welcome bonus credits'
        )



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.user.email