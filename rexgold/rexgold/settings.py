from pathlib import Path
from jdatetime import timedelta
import os
import redis

BASE_DIR = Path(__file__).resolve().parent.parent



SECRET_KEY = 'django-insecure-lx!0&ry0=a!)9(ncdur4mydqalu$#emow2wa4oj)^ew_8jigh6'

DEBUG = True

ALLOWED_HOSTS = ['app-rxg.ir', "www.app-rxg.ir", 'localhost','127.0.0.1','185.10.75.158', '94.182.155.166']
#just for test time
CORS_ALLOW_ALL_ORIGINS = True 

# Application definition

AUTH_USER_MODEL = 'Account_Module.User'  # یا هر ماژولی که User شما توش هست

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # tools
    'drf_spectacular',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist', 
    'django_redis',
    #'django-redis',

    # internal apps
    'Account_Module',
    'Admin_Pannel_Module',
    'User_Pannel_Module',
    'Home_Module',
    'Product_Data_Module',
    'Price_Mnage_Module',
    'Order_Module',
    'DocumentManag_Module',

]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', 
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'rexgold.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'rexgold.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field




DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# ──────────────────────────────────────────────────────────────
# ۱. کش + Channel Layers → redis-cache
# ──────────────────────────────────────────────────────────────
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis-cache:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "KEY_PREFIX": "rexgold",
    }
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": ["redis://redis-cache:6379/1"],  # دیتابیس 1 برای Channel Layers
        },
    },
}

# ──────────────────────────────────────────────────────────────
# ۲. اتصال مستقیم به redis-price برای دریافت قیمت زنده (pub/sub)
# ──────────────────────────────────────────────────────────────
REDIS_PRICE = redis.Redis(
    host='redis-price',
    port=6379,
    db=0,
    decode_responses=True,
    socket_keepalive=True,
    retry_on_timeout=True,
    health_check_interval=30,
)

# اسم چنل قیمت — حتماً با پروژه اول یکسان باشه!
CHANNEL_PRICE_LIVE = "prices:livedata"

# ──────────────────────────────────────────────────────────────
# ۳. سلری (اگر دارید) → redis-celery
# ──────────────────────────────────────────────────────────────
CELERY_BROKER_URL = "redis://redis-celery:6379/0"
CELERY_RESULT_BACKEND = "redis://redis-celery:6379/1"
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = "Asia/Tehran"
CELERY_ENABLE_UTC = False

# ──────────────────────────────────────────────────────────────
# تنظیمات آنلاین کاربر (در redis-cache)
# ──────────────────────────────────────────────────────────────
ONLINE_TIMEOUT_SECONDS = 15 * 60
USER_ONLINE_KEY_PREFIX = "online_user_"



REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'rest_framework.authentication.TokenAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
       "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    # 'DEFAULT_RENDERER_CLASSES': (
    #     'rest_framework.renderers.JSONRenderer',
    # ),

     'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

}

SPECTACULAR_SETTINGS = {
    'TITLE': 'rex gold project api',
    'DESCRIPTION': '',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,

}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=150),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}




