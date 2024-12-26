from django import template
from django.utils import timezone
from ..models import Promotion

register = template.Library()

@register.inclusion_tag('promotions/carousel.html')
def show_promotions_carousel():
    active_promotions = Promotion.objects.filter(
        is_active=True,
        start_date__lte=timezone.now()
    ).exclude(
        end_date__lt=timezone.now()
    ).order_by('order')
    
    return {'promotions': active_promotions}
