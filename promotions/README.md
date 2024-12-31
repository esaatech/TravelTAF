# Promotions App

A flexible Django app for managing and displaying promotional content across your website.

## Features

- Multiple promotion types (configurable through admin)
- Different display styles (basic, card, featured)
- Customizable call-to-action buttons
- Time-based activation (start/end dates)
- Support for both internal and external links
- Image support
- Ordering system

## Quick Start

1. Add "promotions" to your INSTALLED_APPS setting:

```python
INSTALLED_APPS = [
...
'promotions',
]
```

2. Run migrations:

```bash
python manage.py migrate
```


3. Create promotion types in admin interface:

- Custom types as needed

## Usage

### Template Tags

Include promotions in your templates:


{# Basic style #}
{% show_promotions promotion_type='general' style='basic' %}
{# Card style with images #}
{% show_promotions promotion_type='school' style='card' %}
{# Featured style for important promotions #}
{% show_promotions promotion_type='service' style='featured' %}

### Available Styles

1. **Basic** (`basic`)
   - Simple text and link
   - Minimal styling
   - Best for sidebar promotions

2. **Card** (`card`)
   - Image support
   - Title and description
   - CTA button
   - Best for grid layouts

3. **Featured** (`featured`)
   - Large format
   - Full content display
   - Prominent CTA
   - Best for hero sections

## Models

### PromotionType
- name
- slug
- description
- is_active
- created_at

### Promotion
- title
- description
- image
- link_type (internal/external)
- external_url
- internal_name
- promotion_type
- cta_text
- is_active
- order
- start_date
- end_date

## Admin Interface

The app provides a customized admin interface for managing:
- Promotion types
- Individual promotions
- Scheduling and ordering
- Link configuration

## Dependencies

- Django 5.0+
- Python 3.8+
- Pillow (for image handling)

## License

This project is licensed under the MIT License.