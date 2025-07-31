from pathlib import Path
import environ

# Initialize environment variables
env = environ.Env()
environ.Env.read_env()

# Set base directory depending on debug mode
DEBUG = env.bool('DEBUG', default=False)

if DEBUG:
    BASE_DIR = Path(__file__).resolve().parent.parent
else:
    BASE_DIR = Path('/home/routine/www/routines')


DEBUG = env.bool('DEBUG', default=False)

SECRET_KEY = env.str('SECRET_KEY', default='')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])
# ALLOWED_HOSTS = ['*']


NPM_BIN_PATH = "C:/Program Files/nodejs/npm.cmd"

# Application definition
TAILWIND_APP_NAME = 'theme'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',

    'tailwind',
    'theme',
    'django_browser_reload',
    'core',
    'home',
    'my_routine',
]

CSRF_TRUSTED_ORIGINS = [
    'https://routineproject.onrender.com',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware',
]
# if DEBUG:
#     MIDDLEWARE += [
#         "django_browser_reload.middleware.BrowserReloadMiddleware",
#     ]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
            'theme/templates'
            ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


DATABASES_CHECK = env.bool('DATABASES', default=False)
if DATABASES_CHECK:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',  # Django uses mysql backend for MariaDB
            'NAME': env('DATABASE_NAME'),
            'USER': env('DATABASE_USER'),
            'PASSWORD': env('DATABASE_PASSWORD'),
            'HOST': 'localhost',
            'PORT': '3306',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db/db.sqlite3',
        }
    }




# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Dhaka'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/
import os

STATIC_URL = 'static/'
MEDIA_URL = 'media/'

STATIC_ROOT = BASE_DIR / 'static'
MEDIA_ROOT = BASE_DIR / 'media'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'core.UserAccount'
AUTHENTICATION_BACKENDS = [
    'core.backends.AuthBackend',
    'django.contrib.auth.backends.ModelBackend',
]

CSRF_TRUSTED_ORIGINS = [
    'https://routines-s070.onrender.com'
]

if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = "mail.bikoallinone.com"  # Your mail server
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_USE_SSL = False
    EMAIL_HOST_USER = "customerbiko@bikoallinone.com"
    EMAIL_HOST_PASSWORD = "Bikoallinone@MRJ"
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
else:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = env('EMAIL_HOST')  # Your mail server
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_USE_SSL = False
    EMAIL_HOST_USER = env('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER