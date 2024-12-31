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

@register.inclusion_tag('promotions/school_promotions.html')
def show_school_promotions():
    school_promotions = Promotion.objects.filter(
        promotion_type='school',
        is_active=True,
        start_date__lte=timezone.now()
    ).exclude(
        end_date__lt=timezone.now()
    ).order_by('order')
    
    return {'promotions': school_promotions}

@register.inclusion_tag('promotions/promotion_wrapper.html')
def show_promotions(promotion_type='general', style='basic'):
    """
    Display promotions with specified type and style
    
    Args:
        promotion_type: Slug of the promotion type (general, school, service)
        style: Template style to use (basic, card, featured)
    """
    promotions = Promotion.objects.filter(
        promotion_type__slug=promotion_type,
        is_active=True,
        start_date__lte=timezone.now()
    ).exclude(
        end_date__lt=timezone.now()
    ).order_by('order')
    
    return {
        'promotions': promotions,
        'style': style
    }
