from wagtail.core.models import Page, PageViewRestriction

from apps.hip.models import HomePage


from apps.auth_content.models import (  # isort: skip
    BigCitiesHomePage,
    ClosedPODHomePage,
    PCWMSAHomePage,
)


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


def get_bigcities_home_page_url():
    """If a live BigCitiesHomePage exists, return its URL. Otherwise, return get_home_page_url()."""
    bigcities_home_page = BigCitiesHomePage.objects.live().first()
    return bigcities_home_page.url if bigcities_home_page else get_home_page_url()


def get_all_pages_visible_to_request(request):
    """Return all of the Pages that a request (user) has permission to see."""
    # Get the Pages with no view_restrictions. Note: it may seem like unauthenticated
    # users should be able to see all of the Pages without any view_restrictions, like
    # if not request.user.is_authenticated:
    #     return Page.objects.filter(view_restrictions=None)
    # However, this is not completely accurate. Children of private Pages don't
    # have any view_restrictions of their own, but they should still be considered
    # private Pages, because they are children of private Pages. Therefore, we
    # need to go through the following loop, even for unauthenticated users.
    pages_for_user = Page.objects.filter(view_restrictions=None)

    # Loop through private Pages. If the request user has permission to see the
    # Page, then add that Page (and all its descendants) to pages_for_user. If
    # the request user does not have permission to see the Page, then subtract
    # that Page (and its descendants) from pages_for_user.
    for page_view_restriction in PageViewRestriction.objects.select_related("page"):
        page_and_descendants = page_view_restriction.page.get_descendants(
            inclusive=True
        )
        if page_view_restriction.accept_request(request):
            pages_for_user = pages_for_user.union(page_and_descendants)
        else:
            pages_for_user = pages_for_user.difference(page_and_descendants)

    # Because calling .filter() after calling .difference() is not supported,
    # we get all of the relevant Page objects again here.
    return Page.objects.filter(id__in=pages_for_user.values_list("id", flat=True))


def closedpod_user_check(user):
    """A check to determine if a user is in the ClosedPOD Group."""
    return not user.is_anonymous and user.groups.filter(name="Closed POD").exists()
