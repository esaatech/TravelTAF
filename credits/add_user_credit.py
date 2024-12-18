from decimal import Decimal
from django.db import transaction

def add_credits_to_user(user, credits_amount: Decimal) -> None:
    """
    Safely add credits to a user's balance using database transaction
    
    Args:
        user: User instance
        credits_amount: Decimal amount of credits to add
    """
    from .models import UserCredit, CreditTransaction  # Import here to avoid circular import

    with transaction.atomic():
        # Get or create user credit balance
        user_credit, created = UserCredit.objects.select_for_update().get_or_create(
            user=user,
            defaults={'balance': Decimal('0.00')}
        )
        
        # Add credits to current balance
        user_credit.balance += Decimal(str(credits_amount))
        user_credit.save()

        # Create transaction record
        CreditTransaction.objects.create(
            user=user,
            amount=credits_amount,
            transaction_type='BONUS',
            description=f'Added {credits_amount} credits'
        )
