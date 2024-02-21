"""
Django settings for django_project project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
import sys
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6~*~Xdyl-?;olY*T2~)oWxviJ56fybpki{V<%RgGjkTGtJ;4Bz<R-i&Ts:1Sq<)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# EMAIL_BACKEND = 'crm.email_backend.GmailOAuth2EmailBackend'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 't.javkhlantugs1@gmail.com'
DEFAULT_FROM_EMAIL = 'support@estates.solutions'
EMAIL_HOST_PASSWORD = 'epdrtvfjbnkppphz'

GMAIL_CLIENT_ID = '526155639435-ol30a40frn2bk3tmr60gmah7l55jbc33.apps.googleusercontent.com'
GMAIL_CLIENT_SECRET = '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'
GMAIL_REFRESH_TOKEN = 'user_refresh_token'
GMAIL_USER = 't.javkhlantugs1@gmail.com'


# ALLOWED_HOSTS = os.getenv('127.0.0.1','DJANGO_ALLOWED_HOSTS').split(',')
ALLOWED_HOSTS = [
    '127.0.0.1',
    'estates.solutions',
    '206.189.130.94',
    'www.estates.solutions'
    # Add other hosts as needed
]

AUTH_USER_MODEL = 'accounts.CustomUser'

LOGIN_URL = 'user_login'  # Make sure this URL is the same as your login view name
LOGIN_TEMPLATE = 'accounts/login.html'
LOGIN_REDIRECT_URL = ('/crm/')
# Application definition

INSTALLED_APPS = [
    'accounts',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'Realtor',
    'django.contrib.humanize',
    'CRM',
    'dal',
    'dal_select2',
    'suggest_properties',
    'widget_tweaks',
    'bootstrap4',
    'corsheaders',
    'crispy_forms',
    'crispy_bootstrap5',
    "phonenumber_field",
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]


STRIPE_LIVE_PUBLIC_KEY = 'pk_test_51OgfM8BIrM9ZDI85O6mfWKFXHOlNtZhP3osHJtaeRTjFBiCHIeZGqOoBHvpHpZ9yZyBrTnp00e0T9YgHGxYYo6cl00NziFi9ww'
STRIPE_LIVE_SECRET_KEY = 'sk_test_51OgfM8BIrM9ZDI85iqjmY2m9KAesJ2EQSWno9oqSd3cSlfmnCEKvDePLTIoMQDXUbgyRnVsEY2pey4TqRdEg7H5P00Kx1ygJCN'
STRIPE_TEST_PUBLIC_KEY = 'pk_test_51OgfM8BIrM9ZDI85O6mfWKFXHOlNtZhP3osHJtaeRTjFBiCHIeZGqOoBHvpHpZ9yZyBrTnp00e0T9YgHGxYYo6cl00NziFi9ww'
STRIPE_TEST_SECRET_KEY = 'sk_test_51OgfM8BIrM9ZDI85iqjmY2m9KAesJ2EQSWno9oqSd3cSlfmnCEKvDePLTIoMQDXUbgyRnVsEY2pey4TqRdEg7H5P00Kx1ygJCN'
STRIPE_LIVE_MODE = False  # Change to True in production
REDIRECT_DOMAIN = 'localhost:8000'

SITE_ID = 1
SOCIALACCOUNT_LOGIN_ON_GET = True
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/crm/'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

AUTHENTICATION_BACKENDS = [
    # ...
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    # ...
]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {'access_type': 'online'},
        'redirect_uri': 'http://127.0.0.1:8000/crm/settings/google-authenticate/',
    }
}

ROOT_URLCONF = 'django_project.urls'

CSRF_TRUSTED_ORIGINS = ['https://*.estates.solutions',
                        'https://estates.solutions',
                        'http://167.71.237.142',
                        'https://167.71.237.142',]

CORS_ALLOWED_ORIGINS = [
    "https://estates.solutions",
    'http://167.71.237.142',
    'https://167.71.237.142',
]

CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'None'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        # [os.path.join(BASE_DIR, 'CRM', 'templates')]
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

WSGI_APPLICATION = 'django_project.wsgi.application'

SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_SECURE = True
# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_ROOT = BASE_DIR / "assets"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = [
    BASE_DIR / "assets/static",
]

# Media files
MEDIA_ROOT = BASE_DIR / "assets"/"static"/"media"
MEDIA_URL = '/media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'
