from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render

from wagtail.contrib.search_promotions.models import Query
from wagtail.models import Page

from apps.common.utils import get_all_pages_visible_to_request, get_home_page_url


SEARCH_RESULTS_PER_PAGE = 25


def search(request):
    search_query = request.GET.get("query", None)
    page = request.GET.get("page", 1)

    # Keep track of what initial_url is the first time that we load this view, and then
    # "remember" that initial_url (by setting a hidden var in the template) so that even if
    # the user clicks around the pagination links, we can always remember what page they
    # initially came from (in order for the mobile view to act like a modal when it is
    # closed)
    initial_url = request.GET.get("initial_url")
    if not initial_url:
        initial_url = get_home_page_url()
    # helper variable to use in template for each of our pagination URLs
    base_params = f"?query={ search_query }&initial_url={ initial_url }"

    # Search
    if search_query:
        pages_for_request_user = get_all_pages_visible_to_request(request)
        search_results = pages_for_request_user.live().search(
            search_query, partial_match=False
        )

        # Log the query so Wagtail can suggest promoted results
        query = Query.get(search_query).add_hit()
    else:
        search_results = Page.objects.none()

    # Pagination
    paginator = Paginator(search_results, SEARCH_RESULTS_PER_PAGE)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    return render(
        request,
        "search/search.html",
        {
            "search_query": search_query,
            "search_results": search_results,
            "initial_url": initial_url,
            "base_params": base_params,
        },
    )
