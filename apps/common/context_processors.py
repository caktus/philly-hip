from django.conf import settings

from wagtail.documents import get_document_model

from .utils import (
    get_bigcities_home_page_url,
    get_closedpod_home_page_url,
    get_home_page_url,
    get_pcwmsa_home_page_url,
)


from apps.auth_content.models import (  # isort: skip
    BigCitiesHomePage,
    ClosedPODHomePage,
    PCWMSAHomePage,
)


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


def authenticated_home_pages(request):
    """
    Return a list of authenticated home pages for the request.user.

    Some parts of the site require authentication, as well as Group membership.
    When a user is authenticated, it can be helpful to have a context variable
    that lists which authticated pages the user may visit.
    """
    if not request.user.is_authenticated:
        return {"authenticated_home_pages": []}
    else:
        auth_pages = []

        closed_pod_home_page = ClosedPODHomePage.objects.first()
        if closed_pod_home_page and all(
            [
                pageviewrestriction.accept_request(request)
                for pageviewrestriction in closed_pod_home_page.get_view_restrictions()
            ]
        ):
            auth_pages.append(
                {"name": "Closed POD Home", "url": get_closedpod_home_page_url()}
            )

        pcw_msa_home_page = PCWMSAHomePage.objects.first()
        if pcw_msa_home_page and all(
            [
                pageviewrestriction.accept_request(request)
                for pageviewrestriction in pcw_msa_home_page.get_view_restrictions()
            ]
        ):
            auth_pages.append(
                {"name": "PCW-MSA Home", "url": get_pcwmsa_home_page_url()}
            )

        bigcities_home_page = BigCitiesHomePage.objects.first()
        if bigcities_home_page and all(
            [
                pageviewrestriction.accept_request(request)
                for pageviewrestriction in bigcities_home_page.get_view_restrictions()
            ]
        ):
            auth_pages.append(
                {"name": "Big Cities PDPH Home", "url": get_bigcities_home_page_url()}
            )

        return {"authenticated_home_pages": auth_pages}


def right_to_know_pdf_url(request):
    """Return the URL for Document named "Right_to_Know.pdf"."""
    document = get_document_model().objects.filter(title__iexact="right_to_know.pdf")
    url = document.first().url if document.exists() else ""
    return {"right_to_know_pdf_url": url}
