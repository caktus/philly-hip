from django.conf import settings

from .utils import get_home_page_url


def sentry_dsn(request):
    return {"SENTRY_DSN": settings.SENTRY_DSN}


def commit_sha(request):
    return {"COMMIT_SHA": settings.COMMIT_SHA}


def home_page_url(request):
    """Return the URL for the home page."""
    return {"home_page_url": get_home_page_url()}
