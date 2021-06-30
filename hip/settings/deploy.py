import os

from hip.settings.base import *  # noqa: F403


# For more information about deploy settings, see:
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

#### Critical settings

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

### Environment-specific settings

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost").split(":")

### SMTP settings
EMAIL_HOST = os.getenv("EMAIL_HOST", "localhost")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", False)
EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL", False)
# use TLS or SSL, not both:
assert not (EMAIL_USE_TLS and EMAIL_USE_SSL)
if EMAIL_USE_TLS:
    default_smtp_port = 587
elif EMAIL_USE_SSL:
    default_smtp_port = 465
else:
    default_smtp_port = 25
EMAIL_PORT = os.getenv("EMAIL_PORT", default_smtp_port)
EMAIL_SUBJECT_PREFIX = "[hip %s] " % ENVIRONMENT.title()
DEFAULT_FROM_EMAIL = "healthresponse@phila.gov"
SERVER_EMAIL = DEFAULT_FROM_EMAIL

### HTTPS

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "True") == "True"

### Performance optimizations

CACHE_HOST = os.getenv("CACHE_HOST", "cache:11211")
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
        "LOCATION": CACHE_HOST,
    }
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"

# Use template caching on deployed servers
for backend in TEMPLATES:
    if backend["BACKEND"] == "django.template.backends.django.DjangoTemplates":
        default_loaders = ["django.template.loaders.filesystem.Loader"]
        if backend.get("APP_DIRS", False):
            default_loaders.append("django.template.loaders.app_directories.Loader")
            # Django gets annoyed if you both set APP_DIRS True and specify your own loaders
            backend["APP_DIRS"] = False
        loaders = backend["OPTIONS"].get("loaders", default_loaders)
        for loader in loaders:
            if (
                len(loader) == 2
                and loader[0] == "django.template.loaders.cached.Loader"
            ):
                # We're already caching our templates
                break
        else:
            backend["OPTIONS"]["loaders"] = [
                ("django.template.loaders.cached.Loader", loaders)
            ]

### ADMINS and MANAGERS
ADMINS = []  # we use sentry for this

### 3rd-party appplications

SENTRY_DSN = os.getenv("SENTRY_DSN")
if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        environment=ENVIRONMENT,
    )


WEBPACK_LOADER = {
    "DEFAULT": {
        "CACHE": True,
        "BUNDLE_DIR_NAME": "js/bundles/",  # must end with slash
        "STATS_FILE": os.path.join(BASE_DIR, "webpack-stats-production.json"),
        # 'POLL_INTERVAL': 0.1,
        # 'TIMEOUT': None,
        "IGNORE": [r".+\.hot-update.js", r".+\.map"],
    }
}
