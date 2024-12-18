from decimal import Decimal
from django.db import models
from django.conf import settings
from payments.models import BasePayment

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

    def __str__(self):
        return f"{self.user.email} - {self.transaction_type} - {self.amount}"
