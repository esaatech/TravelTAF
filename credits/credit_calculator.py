from decimal import Decimal
from typing import Optional
from dataclasses import dataclass
from django.db import transaction
from django.contrib.auth import get_user_model

User = get_user_model()

@dataclass
class CreditCalculationResult:
    base_credits: int
    bonus_credits: int
    total_credits: int
    currency: str
    exchange_rate: float

class CreditCalculator:
    # Default bonus tiers (can be moved to settings or database later)
    BONUS_TIERS = {
        200: 0.20,  # 20% bonus for $200+
        100: 0.10,  # 10% bonus for $100+
        0: 0.00     # No bonus for less than $100
    }
    
    # Example exchange rates (should be fetched from an API in production)
    EXCHANGE_RATES = {
        'USD': 1.0,
        'EUR': 1.08,
        'GBP': 1.27,
        # Add more currencies as needed
    }

    @classmethod
    def calculate_credits(
        cls,
        amount: float,
        currency: str = 'USD',
        custom_bonus: Optional[float] = None
    ) -> CreditCalculationResult:
        """
        Calculate credits based on amount, currency, and applicable bonuses
        
        Args:
            amount: The payment amount
            currency: The currency code (default: USD)
            custom_bonus: Optional custom bonus percentage (0.0 to 1.0)
            
        Returns:
            CreditCalculationResult object containing credit calculation details
        """
        # Convert to USD if necessary
        exchange_rate = cls.EXCHANGE_RATES.get(currency, 1.0)
        usd_amount = amount * exchange_rate

        # Calculate base credits (1:1 ratio with USD)
        base_credits = int(usd_amount)

        # Determine bonus percentage
        if custom_bonus is not None:
            bonus_percentage = custom_bonus
        else:
            bonus_percentage = 0
            for tier_amount, tier_bonus in sorted(cls.BONUS_TIERS.items(), reverse=True):
                if usd_amount >= tier_amount:
                    bonus_percentage = tier_bonus
                    break

        # Calculate bonus credits
        bonus_credits = int(base_credits * bonus_percentage)
        total_credits = base_credits + bonus_credits

        return CreditCalculationResult(
            base_credits=base_credits,
            bonus_credits=bonus_credits,
            total_credits=total_credits,
            currency=currency,
            exchange_rate=exchange_rate
        )

    @classmethod
    def get_available_currencies(cls) -> list[str]:
        """Get list of supported currencies"""
        return list(cls.EXCHANGE_RATES.keys())

    @classmethod
    def get_bonus_tiers(cls) -> dict:
        """Get current bonus tiers"""
        return cls.BONUS_TIERS

