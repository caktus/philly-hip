"""
Django settings for hip project.

Generated by 'django-admin startproject' using Django 3.0.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os


PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

DEBUG = os.getenv("DJANGO_DEBUG", "False") == "True"
ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")

# Application definition

INSTALLED_APPS = [
    "apps.auth_content",
    "apps.common",
    "apps.disease_control",
    "apps.emergency_response",
    "apps.health_alerts",
    "apps.hip",
    "apps.posters",
    "apps.reports",
    "apps.search",
    "apps.users",
    "taggit",
    "sass_processor",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "wagtail.contrib.table_block",
    "webpack_loader",
]


INSTALLED_APPS += [
    "wagtail.contrib.forms",
    "wagtail.contrib.postgres_search",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail.core",
    "modelcluster",
    # Full list of icons available @ https://fontawesome.com/v4.7.0/icons/
    "wagtailfontawesome",
    "wagtail.contrib.modeladmin",
    "wagtailmenus",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

ROOT_URLCONF = "hip.urls"
AUTH_USER_MODEL = "users.User"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(PROJECT_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "wagtailmenus.context_processors.wagtailmenus",
                "apps.common.context_processors.home_page_url",
                "apps.common.context_processors.previous_url",
                "apps.common.context_processors.authenticated_home_pages",
            ],
        },
    },
]

WSGI_APPLICATION = "hip.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "hip",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    }
}

if os.getenv("DATABASE_URL"):
    import dj_database_url

    db_from_env = dj_database_url.config(
        conn_max_age=500,
        ssl_require=os.getenv("DATABASE_SSL", False),
    )
    DATABASES["default"].update(db_from_env)


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/New_York"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "sass_processor.finders.CssFinder",
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, "static"),
]

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"
MEDIA_STORAGE_BUCKET_NAME = os.getenv("MEDIA_STORAGE_BUCKET_NAME", "")
MEDIA_LOCATION = os.getenv("MEDIA_LOCATION", "")
MEDIA_S3_CUSTOM_DOMAIN = os.getenv("MEDIA_S3_CUSTOM_DOMAIN", "")
DEFAULT_FILE_STORAGE = os.getenv(
    "DEFAULT_FILE_STORAGE", "django.core.files.storage.FileSystemStorage"
)
AWS_DEFAULT_ACL = os.getenv("AWS_DEFAULT_ACL") or None
AWS_S3_SIGNATURE_VERSION = os.getenv("AWS_S3_SIGNATURE_VERSION", "s3v4")
AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME", "us-east-1")
# See https://github.com/wagtail/wagtail/pull/4495#issuecomment-387434521
AWS_S3_FILE_OVERWRITE = False
AWS_QUERYSTRING_AUTH = os.getenv("AWS_QUERYSTRING_AUTH", "True") == "True"
# If not set, boto3 internally looks up IAM credentials
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

# Logging

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "formatters": {
        "basic": {"format": "%(asctime)s %(name)-20s %(levelname)-8s %(message)s"}
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "basic",
        },
    },
    "loggers": {
        "django.request": {
            # only log to console (but errors will still be sent to Sentry)
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": True,
        },
        "django.security": {
            # only log to console (but errors will still be sent to Sentry)
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": True,
        },
        "apps": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": False,
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}

# django-sass-processor
# https://pypi.org/project/django-sass-processor/
SASS_PROCESSOR_ROOT = STATIC_ROOT
SASS_PRECISION = 8

LOGIN_REDIRECT_URL = "auth_view_router"

# Wagtail settings

WAGTAIL_SITE_NAME = "hip"
WAGTAIL_FRONTEND_LOGIN_URL = "login"

WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.contrib.postgres_search.backend",
        "SEARCH_CONFIG": "english",
    },
}

# use our custom form to validate that documents are of a certain file type
WAGTAILDOCS_DOCUMENT_FORM_BASE = "apps.hip.forms.ValidateFileTypeForm"
# have to include jpeg here because even if the file extension is 'jpg', the content
# type is 'image/jpeg' and we compare against content type in our custom form
WAGTAILDOCS_EXTENSIONS = ["pdf", "png", "jpg", "jpeg"]


LOGOUT_REDIRECT_URL = "/"

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = os.getenv("DOMAIN", "http://hip.caktus-built.com")

WEBPACK_LOADER = {
    "DEFAULT": {
        "CACHE": not DEBUG,
        "BUNDLE_DIR_NAME": "bundles/",  # must end with slash
        "STATS_FILE": os.path.join(BASE_DIR, "webpack-stats.json"),
        "POLL_INTERVAL": 0.1,
        "TIMEOUT": None,
        "IGNORE": [r".+\.hot-update.js", r".+\.map"],
    }
}

VIDEOJS_HERO_ID = "video-hero"

PHONENUMBER_DB_FORMAT = "NATIONAL"
PHONENUMBER_DEFAULT_FORMAT = "NATIONAL"
PHONENUMBER_DEFAULT_REGION = "US"

SEARCH_PAGE_SIZE = 10
ADMINS = os.getenv(
    "ADMINS",
    [
        ("PDPH Health Information Portal Dev Team", "hip-philly-team@caktusgroup.com"),
    ],
)

GENERAL_INQUIRY_EMAIL_RECIPIENTS = [e[1] for e in ADMINS]
EVENT_SIGNUP_FORM_SUBMISSION_RECIPIENTS = GENERAL_INQUIRY_EMAIL_RECIPIENTS

DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "no-reply@hip.caktus-built.com")
