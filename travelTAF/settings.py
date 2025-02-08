"""
Django settings for travelTAF project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
# Add logging to debug storage
import logging
from dotenv import load_dotenv

 


# Add this near the top of settings.py after imports
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        '': {  # Root logger
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-+hl-say_pic)ycn+(n_1ouysg%+li1do49k_kev6%c3u5%3bpt'



# Set DEBUG based on environment - default to True for development then for production we set debug to false in cloudrun
DEBUG = os.getenv('DEBUG', 'True') == 'True'  # Default to True for development

# Security settings for production
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_TRUSTED_ORIGINS = [
    'https://traveltaf.com',
    'https://*.traveltaf.com',
    'https://*.run.app',  # For default Cloud Run domain
]



# ... existing settings ...







LOGIN_URL = 'authentication:login'
LOGIN_REDIRECT_URL = 'dashboard:dashboard'

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '192.168.0.65',  # Your local IP
    'traveltaf-578103433472.us-central1.run.app',  # Your Cloud Run URL
    '.run.app',  # All Cloud Run URLs
    '*', #fixed the inconsistencies
]

# For CSRF protection in Cloud Run
CSRF_TRUSTED_ORIGINS = [
    'https://traveltaf-578103433472.us-central1.run.app',
    'https://*.run.app',
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
   #   # Updated: use this instead
    'rest_framework',
    'agent.apps.AgentConfig',
   # "django_browser_reload",
    'news.apps.NewsConfig',
    'subscribers',
    'tools',
    'authentication.apps.AuthenticationConfig',
    'social_django',
    'django_ckeditor_5',
    'storages',
    'payments',
    'credits',
    'resume_builder',
    'promotions',
    'subscriptions',
    'dashboard',
    'flights',
    'customerSupport',
    'faqs',
    'testimonials',
    'service_offerings',
    'shared_data_services.countries',
    'immigrationprograms',
     


]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # For now, allow any access
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
   # "django_browser_reload.middleware.BrowserReloadMiddleware",

]

ROOT_URLCONF = 'travelTAF.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),  # Add this line
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'travelTAF.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases



DATABASES = {
    'default': {
        'ENGINE': 'mysql.connector.django',
        'NAME': 'traveltaf',
        'USER': 'traveltaf-user',
        'PASSWORD': 'Nawoitomo@1985',
        'HOST': os.getenv('DB_HOST', '35.197.66.221'),
        'PORT': '3306',
    }
}

# If running on Cloud Run
if os.getenv('CLOUD_RUN', False):
    DATABASES['default']['HOST'] = '/cloudsql/esaasolution:us-west1:traveltaf-db'
    DATABASES['default']['OPTIONS'] = {
        'unix_socket': '/cloudsql/esaasolution:us-west1:traveltaf-db'
    }


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Email settings from environment variables
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL')





# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# For development only - to serve static files with Gunicorn
if DEBUG:
    STATICFILES_DIRS = [
        BASE_DIR / 'static',
    ]




# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Static files settings
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Whitenoise settings
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# For security with HTTPS
CSRF_TRUSTED_ORIGINS = [
    'https://*.run.app',  # All Cloud Run URLs
]

AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

# Social Auth settings
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = 'your-key'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'your-secret'

SOCIAL_AUTH_FACEBOOK_KEY = 'your-key'
SOCIAL_AUTH_FACEBOOK_SECRET = 'your-secret'

# Email settings (for development)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # For development
# For production, use:
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'your-email@gmail.com'
# EMAIL_HOST_USER_PASSWORD = 'your-app-specific-password'

# CSRF Settings
CSRF_TRUSTED_ORIGINS = [
    'https://traveltaf.com',
    'https://*.traveltaf.com',
    'https://*.run.app',  # For default Cloud Run domain
]

# If you're using CORS, also add:
CORS_ALLOWED_ORIGINS = [
    'https://traveltaf.com',
    'https://*.traveltaf.com',
    'https://*.run.app',
]

CORS_ALLOW_CREDENTIALS = True

# Add CKEditor5 configuration
CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': [
            'heading', '|',
            'fontSize', 'bold', 'italic', 'underline', 'strikethrough', '|',
            'fontColor', 'fontBackgroundColor', '|',
            'bulletedList', 'numberedList', '|',
            'link', 'imageUpload', '|',
            'undo', 'redo'
        ],
        'heading': {
            'options': [
                {'model': 'paragraph', 'title': 'Paragraph', 'class': 'ck-heading_paragraph'},
                {'model': 'heading1', 'view': 'h1', 'title': 'Heading 1', 'class': 'ck-heading_heading1'},
                {'model': 'heading2', 'view': 'h2', 'title': 'Heading 2', 'class': 'ck-heading_heading2'},
                {'model': 'heading3', 'view': 'h3', 'title': 'Heading 3', 'class': 'ck-heading_heading3'},
            ]
        },
        'fontSize': {
            'options': [
                {'title': '8', 'model': '8px'},
                {'title': '10', 'model': '10px'},
                {'title': '12', 'model': '12px'},
                {'title': '14', 'model': '14px'},
                {'title': 'Default', 'model': 'default'},
                {'title': '18', 'model': '18px'},
                {'title': '20', 'model': '20px'},
                {'title': '22', 'model': '22px'},
                {'title': '24', 'model': '24px'},
                {'title': '26', 'model': '26px'},
                {'title': '28', 'model': '28px'},
                {'title': '36', 'model': '36px'},
                {'title': '48', 'model': '48px'}
            ]
        },
        'fontColor': {
            'colors': [
                {'color': '#000000', 'label': 'Black'},
                {'color': '#4D4D4D', 'label': 'Dark Gray'},
                {'color': '#999999', 'label': 'Gray'},
                {'color': '#E6E6E6', 'label': 'Light Gray'},
                {'color': '#FFFFFF', 'label': 'White'},
                {'color': '#22C55E', 'label': 'Primary Green'},
                {'color': '#FF0000', 'label': 'Red'},
                {'color': '#0000FF', 'label': 'Blue'},
                {'color': '#FFFF00', 'label': 'Yellow'},
                {'color': '#00FF00', 'label': 'Green'},
            ]
        },
        'fontBackgroundColor': {
            'colors': [
                {'color': '#000000', 'label': 'Black'},
                {'color': '#4D4D4D', 'label': 'Dark Gray'},
                {'color': '#999999', 'label': 'Gray'},
                {'color': '#E6E6E6', 'label': 'Light Gray'},
                {'color': '#FFFFFF', 'label': 'White'},
                {'color': '#22C55E', 'label': 'Primary Green'},
                {'color': '#FF0000', 'label': 'Red'},
                {'color': '#0000FF', 'label': 'Blue'},
                {'color': '#FFFF00', 'label': 'Yellow'},
                {'color': '#00FF00', 'label': 'Green'},
            ]
        }
    }
}

# Add media settings if not already present
#MEDIA_URL = '/media/'
#MEDIA_ROOT = BASE_DIR / 'media'


# Media files settings
#MEDIA_URL = '/media/'
#MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

""" 
# Media files configuration
if DEBUG:
    # Local development settings
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'
else:
    # the following are used in Production settings (Cloud Run)
    DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
    GS_BUCKET_NAME = os.getenv('GCS_BUCKET_NAME', 'traveltaf-media')
    GS_DEFAULT_ACL = 'publicRead'
    MEDIA_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/'

"""
# Media files configuration - Always use GCS
# At the top with imports
from google.cloud import storage
from django.core.files.storage import default_storage
import logging

# Near your GCS configuration
from google.cloud import storage
from google.oauth2 import service_account
import json

logger = logging.getLogger(__name__)

 #Media files configuration - Always use GCS
from google.oauth2 import service_account

# Explicitly set credentials
#GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
#    os.path.join(BASE_DIR, 'service-account-key.json'),
#    scopes=['https://www.googleapis.com/auth/cloud-platform']
#)

# Storage settings
DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'  # Keep this for static files

# GCS settings
GS_BUCKET_NAME = 'traveltaf-media'
GS_PROJECT_ID = 'esaasolution'
GS_DEFAULT_ACL = 'publicRead'
GS_FILE_OVERWRITE = True
MEDIA_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/'

# Add this to verify storage backend
from django.core.files.storage import default_storage
logger.info(f"Configured storage backend: {default_storage.__class__.__name__}")

# Payment settings
# Stripe and Payment Settings
STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET')  # Optional

# Django-payments configuration
PAYMENT_HOST = 'localhost:8000'  # Change in production
PAYMENT_USES_SSL = False  # Set to True in production
PAYMENT_MODEL = 'credits.CreditPayment'
PAYMENT_VARIANTS = {
    'default': ('payments.dummy.DummyProvider', {}),
    'stripe': ('payments.stripe.StripeProvider', {
        'secret_key': STRIPE_SECRET_KEY,  # Use the same key
        'public_key': STRIPE_PUBLIC_KEY,  # Use the same key
    }),
}


# Amadeus API settings
AMADEUS_CLIENT_ID = os.getenv('AMADEUS_CLIENT_ID')
AMADEUS_CLIENT_SECRET = os.getenv('AMADEUS_CLIENT_SECRET')