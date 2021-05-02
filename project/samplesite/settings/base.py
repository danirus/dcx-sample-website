"""
Django settings for samplesite project.
"""

import os
from pathlib import Path

DEBUG = True

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Quick-start development settings - unsuitable for production

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', None)

SITE_ID = os.environ.get('SITE_ID', 1)

ALLOWED_HOSTS = []

INTERNAL_IPS = ['127.0.0.1']

ADMINS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'manifest_loader',
    'rest_framework',
    'avatar',
    'django_markdown2',
    'django_comments_xtd',
    'django_comments',

    'samplesite',
    'users',
    'stories',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'samplesite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'samplesite.context_processors.settings'
            ],
        },
    },
]

WSGI_APPLICATION = 'samplesite.wsgi.application'

# Password validation
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
LANGUAGE_CODE = 'en'

LANGUAGES = (
    ('nl', 'Dutch'),
    ('en', 'English'),
    ('fi', 'Finnish'),
    ('fr', 'French'),
    ('de', 'German'),
    ('it', 'Italian'),
    ('no', 'Norwegian'),
    ('ru', 'Russian'),
    ('es', 'Spanish'),
)

LANGUAGE_COOKIE_NAME = "lang"

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_DIRS = [
    BASE_DIR / "dist",
    BASE_DIR / "static"
]

STATIC_URL = '/static/'

MEDIA_ROOT = BASE_DIR / 'media'

MEDIA_URL = '/media/'

AUTH_USER_MODEL = 'users.User'

SIGNUP_URL          = "/user/signup/"
LOGIN_URL           = "/user/login/"
LOGOUT_URL          = "/user/logout/"
LOGIN_REDIRECT_URL  = "/"
LOGOUT_REDIRECT_URL = "/"

COMMENTS_XTD_SALT = os.environ.get('COMMENTS_XTD_SALT', 1).encode('utf-8')
COMMENTS_XTD_SEND_HTML_EMAIL = True

COMMENTS_XTD_APP_MODEL_OPTIONS = {
    'default': {
        'who_can_post': 'all',  # Valid values: "users", "all"
        'allow_comment_flagging': True,
        'allow_comment_reactions': True,
        'allow_object_reactions': True
    }
}
