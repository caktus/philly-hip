from wagtail.core.models import Page

from apps.hip.tests.factories import HomePageFactory


from apps.auth_content.tests.factories import (  # isort: skip
    ClosedPODHomePageFactory,
    PCWMSAHomePageFactory,
)


from ..utils import (  # isort: skip
    get_closedpod_home_page_url,
    get_home_page_url,
    get_pcwmsa_home_page_url,
)


def test_get_home_page_url_no_homepage(db):
    """If no HomePage exists, then the function returns '/'."""
    assert "/" == get_home_page_url()


def test_get_home_page_url_no_live_homepage(db):
    """If no live HomePage exists, then the function returns '/'."""
    # Delete any Pages with a URL path of "/".
    Page.objects.all().filter(url_path="/").delete()

    home_page = HomePageFactory(live=False, url_path="/")
    assert "/" == get_home_page_url()
    assert home_page.url != get_home_page_url()


def test_get_home_page_url_with_homepage(db):
    """If a live HomePage exists, then the function returns its URL."""
    home_page = HomePageFactory(live=True, url_path="/")
    assert home_page.url == get_home_page_url()


def test_get_closedpod_home_page_url_no_closedpod_homepage(db, mocker):
    """If no ClosedPODHomePage exists, then the function returns get_home_page_url()."""
    # Mock the apps.common.utils.get_home_page_url function, since it is used
    # to determine the homepage URL.
    mock_get_home_page_url = mocker.patch("apps.common.utils.get_home_page_url")
    mock_homepage_url = "/the_home_page_url/"
    mock_get_home_page_url.return_value = mock_homepage_url

    assert mock_homepage_url == get_closedpod_home_page_url()


def test_get_closedpod_home_page_url_no_live_homepage(db, mocker):
    """If no live ClosedPODHomePage exists, then the function returns get_home_page_url()."""
    # Mock the apps.common.utils.get_home_page_url function, since it is used
    # to determine the homepage URL.
    mock_get_home_page_url = mocker.patch("apps.common.utils.get_home_page_url")
    mock_homepage_url = "/the_home_page_url/"
    mock_get_home_page_url.return_value = mock_homepage_url

    closedpod_home_page = ClosedPODHomePageFactory(live=False)
    assert mock_homepage_url == get_closedpod_home_page_url()
    assert closedpod_home_page.url != get_closedpod_home_page_url()


def test_get_closedpod_home_page_url_with_closedpod_homepage(db, mocker):
    """If a live ClosedPODHomePage exists, then the function returns its URL."""
    closedpod_home_page = ClosedPODHomePageFactory(live=True)
    assert closedpod_home_page.url == get_closedpod_home_page_url()


def test_get_pcwmsa_home_page_url_no_pcwmsa_homepage(db, mocker):
    """If no PCWMSAHomePage exists, then the function returns get_home_page_url()."""
    # Mock the apps.common.utils.get_home_page_url function, since it is used
    # to determine the homepage URL.
    mock_get_home_page_url = mocker.patch("apps.common.utils.get_home_page_url")
    mock_homepage_url = "/the_home_page_url/"
    mock_get_home_page_url.return_value = mock_homepage_url

    assert mock_homepage_url == get_pcwmsa_home_page_url()


def test_get_pcwmsa_home_page_url_no_live_homepage(db, mocker):
    """If no live PCWMSAHomePage exists, then the function returns get_home_page_url()."""
    # Mock the apps.common.utils.get_home_page_url function, since it is used
    # to determine the homepage URL.
    mock_get_home_page_url = mocker.patch("apps.common.utils.get_home_page_url")
    mock_homepage_url = "/the_home_page_url/"
    mock_get_home_page_url.return_value = mock_homepage_url

    pcwmsa_home_page = PCWMSAHomePageFactory(live=False)
    assert mock_homepage_url == get_pcwmsa_home_page_url()
    assert pcwmsa_home_page.url != get_pcwmsa_home_page_url()


def test_get_pcwmsa_home_page_url_with_pcwmsa_homepage(db, mocker):
    """If a live PCWMSAHomePage exists, then the function returns its URL."""
    pcwmsa_home_page = PCWMSAHomePageFactory(live=True)
    assert pcwmsa_home_page.url == get_pcwmsa_home_page_url()
