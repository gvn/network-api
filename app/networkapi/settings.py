'''
Django settings for networkapi project.

Generated by 'django-admin startproject' using Django 1.10.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
'''

import os
import environ
import dj_database_url

app = environ.Path(__file__) - 1
root = app - 1

# We set defaults for values that aren't security related
# to the least permissive setting. For security related values,
# we rely on it being explicitly set (no default values) so that
# we error out first.
env = environ.Env(
    ALLOWED_HOSTS=(list, []),
    ASSET_DOMAIN=(str, ''),
    AWS_LOCATION=(str, ''),
    BUILD_DEBOUNCE_SECONDS=(int, 300),
    BUILD_THROTTLE_SECONDS=(int, 900),
    BUILD_TRIGGER_URL=(str, ''),
    CONTENT_TYPE_NO_SNIFF=bool,
    CORS_REGEX_WHITELIST=(tuple, ()),
    CORS_WHITELIST=(tuple, ()),
    DATABASE_URL=(str, None),
    DEBUG=(bool, False),
    DJANGO_LOG_LEVEL=(str, 'INFO'),
    FILEBROWSER_DEBUG=(bool, False),
    FILEBROWSER_DIRECTORY=(str, ''),
    SET_HSTS=bool,
    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=(str, None),
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=(str, None),
    SSL_REDIRECT=bool,
    USE_S3=(bool, True),
    USE_X_FORWARDED_HOST=(bool, False),
    XSS_PROTECTION=bool,
)

# Read in the environment
if os.path.exists('.env') is True:
    environ.Env.read_env('.env')
else:
    environ.Env.read_env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = root()

APP_DIR = app()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = FILEBROWSER_DEBUG = env('DEBUG')

if env('FILEBROWSER_DEBUG') or DEBUG != env('FILEBROWSER_DEBUG'):
    FILEBROWSER_DEBUG = env('FILEBROWSER_DEBUG')

ALLOWED_HOSTS = env('ALLOWED_HOSTS')
CSRF_TRUSTED_ORIGINS = ALLOWED_HOSTS
ALLOWED_REDIRECT_HOSTS = ALLOWED_HOSTS
USE_X_FORWARDED_HOST = env('USE_X_FORWARDED_HOST')

SITE_ID = 1

# Use social authentication if there are key/secret values defined
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')
SOCIAL_SIGNIN = SOCIAL_AUTH_GOOGLE_OAUTH2_KEY is not None and \
                    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET is not None

USE_S3 = env('USE_S3')

# Application definition
INSTALLED_APPS = list(filter(None, [

    'filebrowser_s3' if USE_S3 else None,
    'social_django' if SOCIAL_SIGNIN else None,

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.redirects',

    'mezzanine.boot',
    'mezzanine.conf',
    'mezzanine.core',
    'mezzanine.generic',
    'mezzanine.pages',
    'mezzanine.forms',

    'whitenoise.runserver_nostatic',
    'rest_framework',
    'django_filters',
    'gunicorn',
    'corsheaders',
    'storages',
    'adminsortable',

    # the network site
    'networkapi.people',
    'networkapi.news',
    'networkapi.utility',
    'networkapi.landingpage',
    'networkapi.highlights',
]))

MIDDLEWARE_CLASSES = [
    'mezzanine.core.middleware.UpdateCacheMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',

    'mezzanine.core.request.CurrentRequestMiddleware',
    'mezzanine.core.middleware.RedirectFallbackMiddleware',
    'mezzanine.core.middleware.TemplateForDeviceMiddleware',
    'mezzanine.core.middleware.TemplateForHostMiddleware',
    'mezzanine.core.middleware.AdminLoginInterfaceSelectorMiddleware',
    'mezzanine.core.middleware.SitePermissionMiddleware',
    'mezzanine.pages.middleware.PageMiddleware',
    'mezzanine.core.middleware.FetchFromCacheMiddleware',
]

if SOCIAL_SIGNIN:
    SOCIAL_AUTH_LOGIN_REDIRECT_URL = env(
        'SOCIAL_AUTH_LOGIN_REDIRECT_URL',
        None
    )

    AUTHENTICATION_BACKENDS = [
        'social_core.backends.google.GoogleOAuth2',
        'django.contrib.auth.backends.ModelBackend',
    ]

    # See http://python-social-auth.readthedocs.io/en/latest/pipeline.html
    SOCIAL_AUTH_PIPELINE = (
        'social_core.pipeline.social_auth.social_details',
        'social_core.pipeline.social_auth.social_uid',
        'social_core.pipeline.social_auth.auth_allowed',
        'social_core.pipeline.social_auth.social_user',
        'social_core.pipeline.user.get_username',
        'social_core.pipeline.user.create_user',
        # custom permissions when a user logs on
        'networkapi.utility.userpermissions.set_user_permissions',
        'social_core.pipeline.social_auth.associate_user',
        'social_core.pipeline.social_auth.load_extra_data',
        'social_core.pipeline.user.user_details',
    )

PACKAGE_NAME_FILEBROWSER = 'filebrowser_safe'
PACKAGE_NAME_GRAPPELLI = 'grappelli_safe'

OPTIONAL_APPS = (
    PACKAGE_NAME_FILEBROWSER,
    PACKAGE_NAME_GRAPPELLI,
)

ROOT_URLCONF = 'networkapi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            app('templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': list(filter(None, [
                'social_django.context_processors.backends'
                if SOCIAL_SIGNIN else None,
                'social_django.context_processors.login_redirect'
                if SOCIAL_SIGNIN else None,
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'mezzanine.conf.context_processors.settings',
                'mezzanine.pages.context_processors.page',
            ])),
            'builtins': [
                'mezzanine.template.loader_tags',
            ],
            'libraries': {
                'adminsortable_tags': 'networkapi.utility.templatetags'
                                      '.adminsortable_tags_custom',
                'settings_value': 'networkapi.utility.templatetags'
                                  '.settings_value'
            }
        },
    },
]

# network asset domain used in templates
ASSET_DOMAIN = env('ASSET_DOMAIN')

WSGI_APPLICATION = 'networkapi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DATABASE_URL = env('DATABASE_URL')

if DATABASE_URL is not None:
    DATABASES['default'].update(dj_database_url.config())

DATABASES['default']['ATOMIC_REQUESTS'] = True


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth'
                '.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth'
                '.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth'
                '.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth'
                '.password_validation.NumericPasswordValidator',
    },
]


# Location of root django.contrib.admin URL, use {% url 'admin:index' %}
ADMIN_URL = r'^admin/'

# Remove these classes from the admin interface
ADMIN_REMOVAL = [
    'mezzanine.pages.models.RichTextPage',
    'mezzanine.pages.models.Link',
    'mezzanine.forms.models.Form',
    'mezzanine.generic.models.ThreadedComment',
]

ADMIN_MENU_ORDER = (
    ('Content', ('pages.Page',
                 ('Media Library', 'media-library'))),
    ('Data', (
        'people.Person',
        'news.News',
        'people.InternetHealthIssue',
        'highlights.Highlight',
        )),
    ('Components', ('landingpage.Signup',)),
    ('Site', ('sites.Site', 'redirects.Redirect', 'conf.Setting')),
    ('Users', ('auth.User', 'auth.Group')),
)

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    app('static'),
)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATIC_ROOT = root('staticfiles')


# Rest Framework Settings
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ],
}


# Storage for user generated files
if USE_S3:
    # Use S3 to store user files if the corresponding environment var is set
    DEFAULT_FILE_STORAGE = 'filebrowser_s3.storage.S3MediaStorage'

    AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_CUSTOM_DOMAIN = env('AWS_S3_CUSTOM_DOMAIN')
    AWS_LOCATION = env('AWS_LOCATION')

    MEDIA_URL = 'https://' + AWS_S3_CUSTOM_DOMAIN + '/'
    MEDIA_ROOT = ''

    FILEBROWSER_DIRECTORY = env('FILEBROWSER_DIRECTORY')

else:
    # Otherwise use the default filesystem storage
    MEDIA_ROOT = root('media/')
    MEDIA_URL = '/media/'

# CORS
CORS_ALLOW_CREDENTIALS = False

if '*' in env('CORS_WHITELIST'):
    CORS_ORIGIN_ALLOW_ALL = True
else:
    CORS_ORIGIN_WHITELIST = env('CORS_WHITELIST')
    CORS_ORIGIN_REGEX_WHITELIST = env('CORS_REGEX_WHITELIST')


# Security
SECURE_BROWSER_XSS_FILTER = env('XSS_PROTECTION')
SECURE_CONTENT_TYPE_NOSNIFF = env('CONTENT_TYPE_NO_SNIFF')
SECURE_HSTS_INCLUDE_SUBDOMAINS = env('SET_HSTS')
SECURE_HSTS_SECONDS = 60 * 60 * 24 * 31 * 6
SECURE_SSL_REDIRECT = env('SSL_REDIRECT')
# Heroku goes into an infinite redirect loop without this.
# See https://docs.djangoproject.com/en/1.10/ref/settings/#secure-ssl-redirect
if env('SSL_REDIRECT') is True:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

X_FRAME_OPTIONS = env('X_FRAME_OPTIONS')

# Jenkins Build trigger URL
BUILD_TRIGGER_URL = env('BUILD_TRIGGER_URL')
BUILD_THROTTLE_SECONDS = env('BUILD_THROTTLE_SECONDS')
BUILD_DEBOUNCE_SECONDS = env('BUILD_DEBOUNCE_SECONDS')

DJANGO_LOG_LEVEL = env('DJANGO_LOG_LEVEL')

# LOGGING
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '[%(asctime)s] [%(levelname)s] %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'networkapi': {
            'handlers': ['console'],
            'level': DJANGO_LOG_LEVEL,
            'propagate': True,
        }
    },
}

try:
    from mezzanine.utils.conf import set_dynamic_settings
except ImportError:
    pass
else:
    set_dynamic_settings(globals())
