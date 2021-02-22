from django.conf import settings

from apps.hip.models import HomePage


def sentry_dsn(request):
    return {"SENTRY_DSN": settings.SENTRY_DSN}


def commit_sha(request):
    return {"COMMIT_SHA": settings.COMMIT_SHA}


def home_page_url(request):
    """Return the URL for the home page."""
    home_page = HomePage.objects.live().first()
    return {"home_page_url": home_page.url if home_page else "/"}
