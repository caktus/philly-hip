from apps.hip.models import StaticPage

from .factories import HomePageFactory


def test_static_page_sets_prev_to_referer(db, rf):
    """If a request has an HTTP_REFERER, the prev_url is the HTTP_REFERER."""
    sp = StaticPage()
    # make a fake request and set HTTP_REFERER
    request = rf.get("/foo")
    referring_url = "https://example.com"
    request.META["HTTP_REFERER"] = referring_url

    context = sp.get_context(request)
    assert context["prev_url"] == referring_url


def test_static_page_prev_defaults_to_slash(db, rf):
    """If a HomePage does not exist, and the HTTP_REFERER is None, prev_url is '/'."""
    s = StaticPage()
    # make a fake request and leave HTTP_REFERER unset
    request = rf.get("/foo")
    assert request.META.get("HTTP_REFERER") is None

    context = s.get_context(request)
    assert context["prev_url"] == "/"


def test_static_page_prev_defaults_to_home(db, rf):
    """If a HomePage exists, and the HTTP_REFERER is None, prev_url is the HomePage URL."""
    home_page = HomePageFactory()
    s = StaticPage()

    # make a fake request and leave HTTP_REFERER unset
    request = rf.get("/foo")
    assert request.META.get("HTTP_REFERER") is None

    context = s.get_context(request)
    assert context["prev_url"] == home_page.url
