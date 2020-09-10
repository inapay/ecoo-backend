"""
Django settings for project.

Generated by 'django-admin startproject' using Django 2.2.11.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
from django.utils.translation import ugettext_lazy as _
from datetime import timedelta
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY', 'cqo_%6g)wia2h8+8u1hb95r=j9o!2l85rx39dmjdr(60ia&o83')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'apps.custom_auth',

    'raven.contrib.django.raven_compat',
    'oauth2_provider',
    'social_django',
    'rest_framework_social_oauth2',

    # 2fa
    'django_otp',
    'django_otp.plugins.otp_static',
    'django_otp.plugins.otp_totp',
    'two_factor',

    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'django_filters',

    'fcm_django',
    'django_simple_task',
    'apps.wallet',
    'apps.currency',
    'apps.profiles',
    'apps.verification',
    'project'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # 'social_django.middleware.SocialAuthExceptionMiddleware',  # <--
]

ROOT_URLCONF = 'project.urls'

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

                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]
# TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'custom_auth.User'

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'de-CH'

LANGUAGE_CHOICES = (
    ('en', _('English')),
    ('de', _('German')),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'project.renderers.CustomJsonRenderer',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',

        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'rest_framework_social_oauth2.authentication.SocialAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'project.utils.CustomCursorPagination',
    'EXCEPTION_HANDLER': 'project.utils.custom_exception_handler',
    'PAGE_SIZE': 10,
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=25),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'HS256',
    # 'SIGNING_KEY': settings.SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]


STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = './media/'

AUTHENTICATION_BACKENDS = (
    'rest_framework_social_oauth2.backends.DjangoOAuth2',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.apple.AppleIdAuth',

    'django.contrib.auth.backends.ModelBackend',
)

SITE_ID = 1

# https://python-social-auth.readthedocs.io/en/latest/backends/apple.html
# Your client_id com.application.your, aka "Service ID"
SOCIAL_AUTH_APPLE_ID_CLIENT = '__APPLE_ID_CLIENT__'
SOCIAL_AUTH_APPLE_ID_TEAM = '__APPLE_ID_TEAM__'  # Your Team ID, ie K2232113
SOCIAL_AUTH_APPLE_ID_KEY = '__APPLE_ID_KEY__'  # Your Key ID, ie Y2P99J3N81K
SOCIAL_AUTH_APPLE_ID_SECRET = """-----BEGIN PRIVATE KEY-----
__APPLE_ID_SECRET__
-----END PRIVATE KEY-----"""
SOCIAL_AUTH_APPLE_ID_SCOPE = ['email', 'name']
SOCIAL_AUTH_APPLE_ID_EMAIL_AS_USERNAME = True

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '__GOOGLE_OAUTH2_KEY__'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '__GOOGLE_OAUTH2_SECRET__'
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ['email', 'profile']

SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['username', 'first_name', 'email']
SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True
SOCIAL_AUTH_POSTGRES_JSONFIELD = True
SOCIAL_AUTH_USER_MODEL = AUTH_USER_MODEL
SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
    # 'social_core.backends.open_id.OpenIdAuth',
    'social_core.backends.apple.AppleIdAuth',
    # 'social_core.backends.google.GoogleOpenId',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.google.GoogleOAuth',
    # 'social_core.backends.twitter.TwitterOAuth',
    # 'social_core.backends.yahoo.YahooOpenId',
)
SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

TEZOS_ADMIN_ACCOUNT_PRIVATE_KEY = os.environ.get(
    'TEZOS_ADMIN_ACCOUNT_PRIVATE_KEY', "edskRqFp3Z9AqoKrMNFb9bnWNwEsRzbjqjBhzmFMLF9UqB6VBmw7F8ppTiXaAnHtysmi6xFxoHf6rMUz6Y1ipiDz2EgwZQv3pa")
TEZOS_TOKEN_CONTRACT_ADDRESS = os.environ.get(
    'TEZOS_TOKEN_CONTRACT_ADDRESS', "KT1NX1CTMYi7cttUom5KfRX2HKfRDPMygKc6")
TEZOS_CALLBACK_CONTRACT_ADDRESS = os.environ.get(
    'TEZOS_CALLBACK_CONTRACT_ADDRESS', "KT1FM1yaa8sfADNojRBGnt9QGXssCicVbeTY")
TEZOS_BLOCK_WAIT_TIME = int(os.environ.get('TEZOS_BLOCK_WAIT_TIME', "5"))
TEZOS_NODE = os.environ.get('TEZOS_NODE', "https://rpc.tzkt.io/carthagenet/")

FCM_DJANGO_SETTINGS = {
    "APP_VERBOSE_NAME": "FCM Django",
    "FCM_SERVER_KEY": '__FCM_KEY__',
    # true if you want to have only one active device per registered user at a time
    # default: False
    "ONE_DEVICE_PER_USER": False,
    # devices to which notifications cannot be sent,
    # are deleted upon receiving error response from FCM
    "DELETE_INACTIVE_DEVICES": True,
}
LOGIN_URL = 'two_factor:login'
LOGIN_REDIRECT_URL = 'admin:index'

PAIN_SERVICE_URL = "https://pain-service-backend.prod.gke.papers.tech"
MAILJET_API_URL = 'https://api.mailjet.com/v4/'
MAILJET_SMS_TOKEN = os.environ.get('MAILJET_SMS_TOKEN')
MAILJET_SENDER_ID = 'ecoo'

# Test encryption key, override for prod
ENCRYPTION_KEY = os.environ.get(
    'ENCRYPTION_KEY', '63298563e90a5d9cd751136c91cc5c7d471c362148480fe4dac2943e6e36051b')

ENABLE_SMS = False
ENABLE_POSTCARD = False

PUSH_NOTIFICATION_TITLE = 'ecoo'

POST_API_CONFIG = {
    'client_id': os.environ.get('POST_CLIENT_ID'),
    'client_secret': os.environ.get('POST_CLIENT_SECRET'),
    'base_url': 'https://apiint.post.ch/pcc/api/',
    'token_url': 'https://apiint.post.ch/OAuth/token',
    'scope': 'PCCAPI',

    'campaign_key': os.environ.get('POST_CAMPAIGN_KEY'),

    'sender': {
        'firstname': '',
        'lastname': '',
        'company': 'Papers AG',
        'street': 'Dammstrasse',
        'houseNr': '16',
        'zip': '6300',
        'city': 'Zug'
    },

    'branding': {
        'brandingText': {
            'text': 'test',
            'blockColor': '#FFFFFF',
            'textColor': '#000000'
        },
        'brandingQRCode': {
            'encodedText': 'test',
            'accompanyingText': 'test',
            'blockColor': '#FFFFFF',
            'textColor': '#000000'
        }
    }

}

SMS_TEXT = 'Bitte geben Sie diesen Code im ecoo App ein um den Verifizierungsprozess zu beenden und ihr Guthaben zu bekommen.'
POST_CARD_TEXT = """
Liebes Wetziker Gewerbe,

Es freut uns dass Sie an dieser Aktion mitmachen!

Bitte geben Sie den folgen Code in die ecoo App ein um die Verifizerung abzuschliesen:

{}

Wir wünschen Ihnen viel Erfolg!
"""

SMS_PIN_WAIT_TIME_THRESHOLD_SECONDS = 15
