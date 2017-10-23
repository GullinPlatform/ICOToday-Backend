"""
Django 1.11.2 settings for ICOToday project.
"""
import datetime
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# TODO
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# SECURITY WARNING: keep the secret key used in production secret!
with open(os.path.join(BASE_DIR, 'settings/secret.txt')) as f:
	SECRET_KEY = f.read().strip()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
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
	# installed
	'rest_framework',
	'corsheaders',
	'storages',
	# apps
	'ICOToday.apps.accounts',
	'ICOToday.apps.companies',
	'ICOToday.apps.projects',
	'ICOToday.apps.feeds',
	'ICOToday.apps.notifications',
	'ICOToday.apps.wallets',
	'ICOToday.apps.conversations',
	'ICOToday.apps.rest_framework_jwt',
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

# Account customization
AUTH_USER_MODEL = 'accounts.Account'
# TODO change to ICOToday AccountInfo ID in production mode
OFFICIAL_ACCOUNT_INFO_ID = 2

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
USE_I18N = False
USE_L10N = False
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

# Database
DATABASES = {
	'default': {
		'ENGINE'  : 'django.db.backends.mysql',
		'NAME'    : 'icotoday',
		'USER'    : 'icotoday',
		'PASSWORD': 'ICOToday888!',
		'HOST'    : 'icotodaydb-cluster.cluster-canzstryns10.us-east-2.rds.amazonaws.com',
		'PORT'    : '3306'
	}
}

# Rest Framework
REST_FRAMEWORK = {
	'DEFAULT_PERMISSION_CLASSES'    : [
		'rest_framework.permissions.IsAuthenticatedOrReadOnly',
	],
	'DEFAULT_AUTHENTICATION_CLASSES': [
		'ICOToday.apps.rest_framework_jwt.authentication.JSONWebTokenAuthentication',
	],
	'DEFAULT_RENDERER_CLASSES'      : (
		'rest_framework.renderers.JSONRenderer',
	)
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
	'X-CSRF-TOKEN',
	'XMLHttpRequest',
	'Access-Control-Allow-Origin',
	'Access-Control-Allow-Methods',
	'Access-Control-Allow-Headers',
	'Access-Control-Allow-Credentials',
	'Access-Control-Max-Age'
)

CORS_PREFLIGHT_MAX_AGE = 86400
CORS_ALLOW_CREDENTIALS = True

# Restful JWT AUTH
JWT_AUTH = {
	'JWT_ENCODE_HANDLER'             : 'ICOToday.apps.rest_framework_jwt.utils.jwt_encode_handler',
	'JWT_DECODE_HANDLER'             : 'ICOToday.apps.rest_framework_jwt.utils.jwt_decode_handler',
	'JWT_PAYLOAD_HANDLER'            : 'ICOToday.apps.rest_framework_jwt.utils.jwt_payload_handler',
	'JWT_PAYLOAD_GET_USER_ID_HANDLER': 'ICOToday.apps.rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',
	'JWT_RESPONSE_PAYLOAD_HANDLER'   : 'ICOToday.apps.rest_framework_jwt.utils.jwt_response_payload_handler',

	'JWT_PUBLIC_KEY'                 : open(os.path.join(BASE_DIR, 'settings/jwtRS256.key.pub')).read(),
	'JWT_PRIVATE_KEY'                : open(os.path.join(BASE_DIR, 'settings/jwtRS256.key')).read(),
	'JWT_ALGORITHM'                  : 'RS256',

	'JWT_VERIFY_EXPIRATION'          : True,
	'JWT_EXPIRATION_DELTA'           : datetime.timedelta(days=1),
	'JWT_ALLOW_REFRESH'              : True,
	'JWT_REFRESH_EXPIRATION_DELTA'   : datetime.timedelta(days=7),

	'JWT_AUTH_HEADER_PREFIX'         : 'TOKEN',
	'JWT_AUTH_COOKIE'                : 'icotodaytoken'
}

# ------ AWS Credentials ------
AWS_ACCESS_KEY_ID = 'AKIAJOZXNV5BDLRRO7LQ'
AWS_SECRET_ACCESS_KEY = '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'

# ------ AWS S3 ------
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_STORAGE_BUCKET_NAME = 'icotoday'
AWS_S3_HOST = 's3.us-east-2.amazonaws.com'

# ------ AWS SES ------
EMAIL_BACKEND = 'django_ses.SESBackend'
AWS_SES_REGION_NAME = 'us-east-1'
AWS_SES_REGION_ENDPOINT = 'email.us-east-1.amazonaws.com'
AWS_SES_AUTO_THROTTLE = 0.5  # (default; safety factor applied to rate limit)
