"""
Django settings for ICOToday project.

Generated by 'django-admin startproject' using Django 1.11.2.
"""

import datetime
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# SECURITY WARNING: keep the secret key used in production secret!
with open(os.path.join(BASE_DIR, 'settings/secret.txt')) as f:
	SECRET_KEY = f.read().strip()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = [
	'http://www.icotoday.io',
	'http://icotoday.io',
	'https://icotoday.io',
	'icotoday.io',
	'www.icotoday.io',
	'api.icotoday.io',

]

# Set auto redirect to false
APPEND_SLASH = False

# Application definition
INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'rest_framework',
	'rest_framework_jwt',
	'corsheaders',
	'storages',

	'ICOToday.apps.accounts',
	'ICOToday.apps.posts',
	'ICOToday.apps.discussions'

]

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'corsheaders.middleware.CorsMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
	{
		'BACKEND' : 'django.template.backends.django.DjangoTemplates',
		'DIRS'    : [os.path.join(BASE_DIR, 'templates')],
		'APP_DIRS': True,
		'OPTIONS' : {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
			],
		},
	},
]

WSGI_APPLICATION = 'ICOToday.wsgi.application'

ROOT_URLCONF = 'ICOToday.urls'
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

# Database
# TODO
DATABASES = {
	'default': {
		'ENGINE'  : 'django.db.backends.mysql',
		'NAME'    : 'icotoday',
		'USER'    : 'root',
		'PASSWORD': 'billions',
		'HOST'    : '/var/lib/mysql/mysql.sock',
	}
}

# Rest Framework
REST_FRAMEWORK = {
	'DEFAULT_PERMISSION_CLASSES'    : [
		'rest_framework.permissions.IsAuthenticated',
	],
	'DEFAULT_AUTHENTICATION_CLASSES': [
		'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
	]
}

# Cors Origin Settings
CORS_ORIGIN_WHITELIST = (
	'http://www.icotoday.io',
	'http://icotoday.io',
	'https://icotoday.io',
	'icotoday.io',
	'www.icotoday.io',
	'api.icotoday.io',
)
CORS_ALLOW_HEADERS = (
	'accept',
	'accept-encoding',
	'authorization',
	'content-type',
	'dnt',
	'origin',
	'user-agent',
	'x-csrftoken',
	'x-requested-with',
	'cache-control',
	'HTTP_X_XSRF_TOKEN',
	'XMLHttpRequest',
	'Access-Control-Allow-Origin',
)

# RESTful JWT AUTH
JWT_AUTH = {
	'JWT_ENCODE_HANDLER'             : 'rest_framework_jwt.utils.jwt_encode_handler',
	'JWT_DECODE_HANDLER'             : 'rest_framework_jwt.utils.jwt_decode_handler',
	'JWT_PAYLOAD_HANDLER'            : 'rest_framework_jwt.utils.jwt_payload_handler',
	'JWT_PAYLOAD_GET_USER_ID_HANDLER': 'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',
	'JWT_RESPONSE_PAYLOAD_HANDLER'   : 'rest_framework_jwt.utils.jwt_response_payload_handler',

	'JWT_SECRET_KEY'                 : SECRET_KEY,
	'JWT_PUBLIC_KEY'                 : None,
	'JWT_PRIVATE_KEY'                : None,
	'JWT_ALGORITHM'                  : 'HS256',
	'JWT_VERIFY'                     : True,
	'JWT_VERIFY_EXPIRATION'          : True,

	'JWT_LEEWAY'                     : 0,
	'JWT_EXPIRATION_DELTA'           : datetime.timedelta(days=7),
	'JWT_AUDIENCE'                   : None,
	'JWT_ISSUER'                     : None,
	'JWT_ALLOW_REFRESH'              : True,
	'JWT_REFRESH_EXPIRATION_DELTA'   : datetime.timedelta(days=7),

	'JWT_AUTH_HEADER_PREFIX'         : 'TOKEN'
}

# Account customization
AUTH_USER_MODEL = 'accounts.Account'

# ------ Amazon S3 ------
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
# Amazon Web Services storage bucket name, as a string.
AWS_STORAGE_BUCKET_NAME = 'icotoday'

# ------ SES email settings ------

EMAIL_BACKEND = 'django_ses.SESBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# These are optional -- if they're set as environment variables they won't
# need to be set here as well
AWS_ACCESS_KEY_ID = 'AKIAIPLNT5PYIDLOIOAQ'
AWS_SECRET_ACCESS_KEY = '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'

# Additionally, if you are not using the default AWS region of us-east-1,
# you need to specify a region, like so:
AWS_SES_REGION_NAME = 'us-east-1'
AWS_SES_REGION_ENDPOINT = 'email.us-east-1.amazonaws.com'
AWS_SES_AUTO_THROTTLE = 0.5  # (default; safety factor applied to rate limit)
