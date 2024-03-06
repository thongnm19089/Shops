from .base import *

import os

ALLOWED_HOSTS = ["*"]
DEBUG = True

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     # 'NAME': os.path.join(BASE_DIR, '..','db.sqlite3'),
    #     'NAME': os.environ.get('DATABASE_NAME', 'shop'),
    #     'HOST': os.environ.get('DATABASE_HOST', '127.0.0.1'),
    #     'USER': os.environ.get('DATABASE_USER', 'postgres'),
    #     'PASSWORD': os.environ.get('DATABASE_PASSWORD', 'minh2302'),
    #     'PORT': os.environ.get('DATABASE_PORT', '5432'),
    # }
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        # 'NAME': os.path.join(BASE_DIR, '..','db.sqlite3'),
        'NAME': os.environ.get('DATABASE_NAME', 'shops'),
        'HOST': os.environ.get('DATABASE_HOST', 'postgresql-104067-0.cloudclusters.net'),
        'USER': os.environ.get('DATABASE_USER', 'minh'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', 'minh2302'),
        'PORT': os.environ.get('DATABASE_PORT', '10029'),
    }
}

# LOGGING
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {name} {pathname} {lineno:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true'],
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'apps': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
            'propagate': False,
        },
    },
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    },
}