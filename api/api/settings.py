from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-i5)qbh(d+++%#3#jraogzku=j)anscapctthxgofksjvpy3b$t'
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

INSTALLED_APPS = [
    "myapi",
    'rest_framework',
    'rest_framework.authtoken',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'authentification',
    'django_auto_logout',  # Added for auto logout functionality
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # This handles sessions
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_auto_logout.middleware.auto_logout',
    #'api.middleware.ip_security.IPSecurityMiddleware',
    
]

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'api.urls'

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
                'django_auto_logout.context_processors.auto_logout_client',
            ],
        },
    },
]

WSGI_APPLICATION = 'api.wsgi.application'

# Database configuration
DATABASES = {

    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'sami01',
        'HOST': 'localhost',
        'PORT': '5432',
        'OPTIONS': {
            'options': '-c search_path="MOHAMMEDIA-SAT"'
        }
    },

    'default1': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'sami01',
        'HOST': 'localhost',
        'PORT': '5432',
        'OPTIONS': {
            'options': '-c search_path="UM5-EOSAT"'
        }
    },

    'auth_db': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'authentification',
        'USER': 'postgres',
        'PASSWORD': 'sami01',
        'HOST': 'localhost',
        'PORT': '5432',
        'OPTIONS': {
            'options': '-c search_path=public'
        }
    },
}

DATABASE_ROUTERS = ['api.routers.AuthRouter']

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# Enhanced Session Configuration for Expiring Sessions
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_NAME = 'sessionid'
SESSION_COOKIE_AGE = 20  # in seconds
SESSION_SAVE_EVERY_REQUEST = True  # Update session on every request
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # Session expires when browser closes
SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access to session cookie
SESSION_COOKIE_SAMESITE = 'Lax'

# Token expiration (for DRF Token Authentication)
TOKEN_EXPIRED_AFTER_SECONDS = 1800  # 30 minutes

# Auto logout configuration
AUTO_LOGOUT = {
    'IDLE_TIME': 20,  # 20 secs
    'REDIRECT_TO_LOGIN_IMMEDIATELY': True,
    'MESSAGE': 'Your session has expired due to inactivity.',
}

# CSRF Configuration
CSRF_COOKIE_SECURE = False  # Set to True in production
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = False  # Set to True in production

# Session timeout settings
SESSION_TIMEOUT_REDIRECT = '/auth/login/'
SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True
SESSION_EXPIRE_AFTER_LAST_ACTIVITY_GRACE_PERIOD = 60  # 1 minute grace period

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
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'






'''
# IP Security Settings for EMI network
ALLOWED_IP_NETWORKS = [
    '127.0.0.1/32',      # localhost
    '10.72.177.0/24',    # Specific EMI network subnet
    '192.168.56.1/32',   # Specific VirtualBox IP
]

# For stricter security, you could use specific IP ranges:
# ALLOWED_IP_RANGES = [
#     '127.0.0.1/32',        # Localhost
#     '10.72.177.0/24',      # Only the devices on your specific subnet
#     '192.168.56.0/24',     # Your VirtualBox host-only network
# ]

# For the strictest security (only your specific machine):
# ALLOWED_IP_RANGES = [
#     '127.0.0.1/32',        # Localhost
#     '10.72.177.60/32',     # Only your specific Wi-Fi IP
#     '192.168.56.1/32',     # Your VirtualBox host-only adapter
# ]

# Paths that bypass IP restriction (useful for health checks, etc.)
ALLOWED_IP_BYPASS_PATHS = [

    '/health/',
    '/api/public/',
]


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'ip_restriction.log',  # Adjust path as needed
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'ip_restriction': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}


IP_RESTRICTION_EXEMPT_PATHS = [
    '/api/access-denied/',    # Access denied API endpoint
    '/access-denied/',        # Access denied page
    '/static/',               # Static files
    '/media/',                # Media files
    '/login/',                # Login page
    '/auth/login/',           # Auth login endpoint
    '/api/client-ip/',        # Client IP endpoint
    '/admin/login/',          # Admin login
]
'''