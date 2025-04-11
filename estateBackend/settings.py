"""
Django settings for estateBackend project.

Generated by 'django-admin startproject' using Django 5.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
from pathlib import Path
#from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
#env_path = BASE_DIR / '.env'  # Define env_path

#load_dotenv(env_path)  
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-!01(9e5x0=62%-bif#!+%fkye58u5x*t9kl0$xgkqa91kiw@!)'

# # SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-dev-key')  # Use env var in production
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'  # False in production

ALLOWED_HOSTS = [
    "estate-frontend-bay.vercel.app",
    "https://www.estateone.in/",
    "estateone.in",
     ".onrender.com",
    "127.0.0.1",
    "localhost",
]
CORS_ALLOWED_ORIGINS = [
    "https://estate-frontend-bay.vercel.app", 
    "https://www.estateone.in",
    "https://estateone.in",  # ✅ Add root domain without www
]

CSRF_TRUSTED_ORIGINS = [
    "https://estate-frontend-bay.vercel.app",
    "https://e-state-6xcr.vercel.app",
    "https://www.estateone.in",
    "https://estateone.in",  # ✅ Add root domain without www
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "corsheaders",
    'rest_framework',
    'panel',
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    
]



ROOT_URLCONF = 'estateBackend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = 'estateBackend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'estate',
#         'USER': 'postgres',  
#         'PASSWORD': 'admin',  
#         'HOST': 'localhost', 
#         'PORT': '5432',  
#     }
# }


import dj_database_url
import os
# DATABASES = {
#     "default": dj_database_url.config(
#         default="postgresql://estate_one_user:eSO1sAjk4TzxMwhxyFjKku2vTXcMa7tI@dpg-cvfb1ipopnds73b8er7g-a.oregon-postgres.render.com/estate_one",
#         engine="django.db.backends.postgresql",
#     )
# }
DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),  # Read from environment
        engine='django.db.backends.postgresql',
    )
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

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage' 
# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'  
# EMAIL_PORT = 587  
# EMAIL_USE_TLS = True  
# EMAIL_HOST_USER = 'rehankhan.upr@gmail.com' 
# EMAIL_HOST_PASSWORD = 'wkeidudcklbwvqby' 

# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtpout.secureserver.net'  # GoDaddy's SMTP server
EMAIL_PORT = 465  # Use 465 for SSL (recommended) or 587 for TLS
EMAIL_USE_SSL = True  # For port 465 (use EMAIL_USE_TLS=True for port 587)
EMAIL_HOST_USER = 'connect@estateone.in'  # Full GoDaddy email
EMAIL_HOST_PASSWORD = 'Arpitarora@12'  # Your email password

import os

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
