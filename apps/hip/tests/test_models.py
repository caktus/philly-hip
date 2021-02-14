from django.urls import reverse

from apps.hip.models import StaticPage


def test_static_page_sets_prev_to_referer(db, rf):
    sp = StaticPage()
    # make a fake request and set HTTP_REFERER
    request = rf.get("/foo")
    referring_url = "https://example.com"
    request.META["HTTP_REFERER"] = referring_url

    context = sp.get_context(request)
    assert context["prev_url"] == referring_url


def test_static_page_prev_defaults_to_home(db, rf):
    s = StaticPage()
    # make a fake request and leave HTTP_REFERER unset
    request = rf.get("/foo")
    assert request.META.get("HTTP_REFERER") is None

    context = s.get_context(request)
    assert context["prev_url"] == reverse("home")
