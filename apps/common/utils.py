from apps.auth_content.models import ClosedPODHomePage, PCWMSAHomePage
from apps.hip.models import HomePage


def get_home_page_url():
    """If a live HomePage exists, return its URL. Otherwise, return '/'."""
    home_page = HomePage.objects.live().first()
    return home_page.url if home_page else "/"


def get_closedpod_home_page_url():
    """If a live ClosedPODHomePage exists, return its URL. Otherwise, return get_home_page_url()."""
    closedpod_home_page = ClosedPODHomePage.objects.live().first()
    return closedpod_home_page.url if closedpod_home_page else get_home_page_url()


def get_pcwmsa_home_page_url():
    """If a live PCWMSAHomePage exists, return its URL. Otherwise, return get_home_page_url()."""
    pcwmsa_home_page = PCWMSAHomePage.objects.live().first()
    return pcwmsa_home_page.url if pcwmsa_home_page else get_home_page_url()
