from apps.hip.models import HomePage


def get_home_page_url():
    """If a live HomePage exists, return its URL. Otherwise, return '/'."""
    home_page = HomePage.objects.live().first()
    return home_page.url if home_page else "/"
