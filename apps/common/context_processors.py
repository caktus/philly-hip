from django.conf import settings

from .utils import get_home_page_url


def sentry_dsn(request):
    return {"SENTRY_DSN": settings.SENTRY_DSN}


def commit_sha(request):
    return {"COMMIT_SHA": settings.COMMIT_SHA}


def home_page_url(request):
    """Return the URL for the home page."""
    return {"home_page_url": get_home_page_url()}


def previous_url(request):
    """Return the user's previous URL, based on the HTTP_REFERER header."""
    # Use the HTTP_REFERER, or default to the value returned by get_home_page_url().
    # Note: we use the try/except logic here (rather than request.META.get...)
    # in order to avoid calling get_home_page_url() every time.
    try:
        return {"previous_url": request.META["HTTP_REFERER"]}
    except KeyError:
        return {"previous_url": get_home_page_url()}
