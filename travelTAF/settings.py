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

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-+hl-say_pic)ycn+(n_1ouysg%+li1do49k_kev6%c3u5%3bpt'



# Set DEBUG based on environment
DEBUG = False  # For production

# Security settings for production
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_TRUSTED_ORIGINS = [
    'https://traveltaf.com',
    'https://*.traveltaf.com',
    'https://*.run.app',  # For default Cloud Run domain
]










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

# Media files settings
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')



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
        'toolbar': ['heading', '|', 'bold', 'italic', 'link',
                   'bulletedList', 'numberedList', 'blockQuote', 'imageUpload', ],
    }
}

# Add media settings if not already present
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'





