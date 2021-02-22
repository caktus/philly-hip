from apps.hip.tests.factories import HomePageFactory

from ..utils import get_home_page_url


def test_get_home_page_url_no_homepage(db):
    """If no HomePage exists, then the function returns '/'."""
    assert "/" == get_home_page_url()


def test_get_home_page_url_no_live_homepage(db):
    """If no live HomePage exists, then the function returns '/'."""
    home_page = HomePageFactory(live=False)
    assert "/" == get_home_page_url()
    assert home_page.url != get_home_page_url()


def test_get_home_page_url_with_homepage(db):
    """If a live HomePage exists, then the function returns its URL."""
    home_page = HomePageFactory(live=True)
    assert home_page.url == get_home_page_url()
