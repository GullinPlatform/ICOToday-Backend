from .prod import *

# Add tmp path
# TMP_PATH = os.path.abspath(os.path.join(BASE_DIR, 'local'))

# Set debug to true
DEBUG = True

# Init debug toolbar
INSTALLED_APPS += ('debug_toolbar',)
MIDDLEWARE += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}
# Set secret to 42

SECRET = '42'

ALLOWED_HOSTS = '*'
# Set database to local sqlite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'tmp.sqlite3'),
    }
}

INTERNAL_IPS = ['127.0.0.1']

# Set JWT token expiration to false
JWT_AUTH['JWT_VERIFY_EXPIRATION'] = False

# ----- Cross Origin Header -----
CORS_ORIGIN_WHITELIST = (
    'localhost:4000',
    '127.0.0.1:4000',
    'localhost:4004',
    '127.0.0.1:4004'
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = '/media/'

OFFICIAL_ACCOUNT_INFO_ID = 4
