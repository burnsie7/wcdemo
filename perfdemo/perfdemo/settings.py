import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


MY_POD_NAME = os.getenv('MY_POD_NAME', 'local')
MY_POD_NAMESPACE = os.getenv('MY_POD_NAMESPACE', 'local')
MY_POD_IP = os.getenv('MY_POD_IP', 'localhost')
MY_SVC_NAMESPACE = 'wcdemo.default.svc.cluster.local'  # TODO: dynamic
MY_SVC_PORT= '80'  # TODO: dynamic

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=_c22@6n=x+cl^1#k=a)r=hw^jb@e33hsm62&x!ksnguuag)%9'  # TODO: env var

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']  # TODO: Restrict to proper hosts


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'perfdemo.demo',
    'rest_framework',
    'ddtrace.contrib.django',
]

MIDDLEWARE = [
    'ddtrace.contrib.django.TraceMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'perfdemo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_ROOT, 'templates')],
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

WSGI_APPLICATION = 'perfdemo.wsgi.application'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'TEST_REQUEST_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DATABASE_ENGINE', 'django.db.backends.postgresql_psycopg2'),
        'NAME': os.getenv('DATABASE_NAME', 'perfdemo'),  # TODO: Fix all of these defaults
        'USER': os.getenv('DATABASE_USER', 'perfdemo'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', 'abc123'),
        'HOST': os.getenv('DATABASE_SERVICE_HOST', '127.0.0.1'),
        'PORT': os.getenv('DATABASE_SERVICE_PORT', 5432),
    }
}

DATADOG_TRACE = {
    'DEFAULT_SERVICE': os.getenv('DATADOG_SERVICE_NAME', 'wcdemo'),
    'DEFAULT_DATABASE_PREFIX': os.getenv('DATADOG_DATABASE_NAME', 'wcdemo'),
    'TAGS': {'env': os.getenv('DATADOG_SERVICE_TAG', 'wcd')},
    'ENABLED': os.getenv('DATADOG_TRACE_ENABLED', True),
    'AGENT_HOSTNAME': os.getenv('DATADOG_TRACE_AGENT_HOSTNAME', 'dd-agent'),
    'AGENT_PORT': os.getenv('DATADOG_TRACE_AGENT_PORT', 8126),
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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

# CELERY STUFF
BROKER_URL = 'redis://redis.default.svc.cluster.local:6379'
CELERY_RESULT_BACKEND = 'redis://redis.default.svc.cluster.local:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Africa/Nairobi'

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

