"""
Django settings for MDM project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
from datetime import timedelta
from pathlib import Path
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-=$gd%7)pc!+h)an%k5%#2e!i)=s6x*2zr+7=g6+gg=f&l-&@a2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  #для режима отладки страницы

ALLOWED_HOSTS = ['127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'shop.apps.ShopConfig',
    'blog.apps.BlogConfig',
    # 'crispy_forms',  - for bootstrap не использую не разобрался как и для
    # практики решил написать свой макет HTML и свой CSS.
    'rest_framework',
    'rest_framework.authtoken',
    'django_celery_beat',
]

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': [  #для получения токенов POST
        'rest_framework.authentication.TokenAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',  Возможно если клиент Mozilla, учитывать по session id?
        # 'rest_framework.authentication.SessionAuthentication',
    ],
}

REDIS_HOST = "0.0.0.0"
REDIS_PORT = "6379"

CELERY_BROKER_URL = 'redis://localhost:6379/0' # URL Redis брокера
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0' # URL Redis для хранения результатов задач
# CELERY_IMPORTS = ('shop.tasks',)
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Moscow'
CELERY_TASK_DEFAULT_QUEUE = 'default'
CELERY_RESULT_EXPIRES = None
# определяет используемый планировщик для Celery Beat, который можно использовать для планирования периодических задач.
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# Настройки для работы с Redis  не разобрался про какой кэш идет речь.
# CACHES = {
#     'default': {
#         'BACKEND': 'django_redis.cache.RedisCache',
#         'LOCATION': 'redis://localhost:6379/0',
#         'OPTIONS': {
#             'CLIENT_CLASS': 'django_redis.client.DefaultClient',
#         }
#     },
# }


# LOGIN_REDIRECT_URL = '/'
# метод при авторизации пользователя возвращает домой

#строку при развертывании сайта удалить, только для локального сревера
# CSRF_TRUSTED_ORIGINS=["http://127.0.0.1:8000"]

LOGIN_URL = '/login/'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.mail.ru'
EMAIL_PORT = 2525  #for yandex: 465
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = '***@mail.ru'
EMAIL_HOST_PASSWORD = '***'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'MDM.urls'

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

WSGI_APPLICATION = 'MDM.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mdm_db',
        'USER': 'postgres',
        'PASSWORD': 'Zrhfcfdxbr',
        'HOST': 'localhost',
        'PORT': '5432',
        'HARBOR': ''
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'shop.CustomUser'

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'ru'
#для руссофикации админ панели и Джанго

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# для пути к папке со статическим файлом
STATIC_DIRS =[]
#для не стандартных путей к папке со статическ.файлами

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        },
        'myapp': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}
DJANGO_LOG_LEVEL=DEBUG

# SIMPLE_JWT = {
#     'AUTH_HEADER_TYPES': ('JWT',),
#     'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
#     'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
# }

# CRISPY_TEMPLATE_PACK = 'bootstrap4'
#параметр, который устанавливает Bootstrap 4 в качестве структуры стилей по умолчанию для django-crispy-forms:
