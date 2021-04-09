from wagtail.core.models import Page

from apps.hip.tests.factories import HomePageFactory, StaticPageFactory


def test_homepage_context_recent_updates(db, rf, mocker):
    """The HomePage 'recent_updates' are limited to Pages the request.user can see."""
    home_page = HomePageFactory()
    static_page = StaticPageFactory(parent=home_page, title="Static Page")

    # Mock the apps.common.utils.get_all_pages_visible_to_request function,
    # since it should be used to get the Pages visible to the request.user.
    mock_get_all_pages_visible_to_request = mocker.patch(
        "apps.common.utils.get_all_pages_visible_to_request"
    )
    pages_visible_to_user = Page.objects.filter(id=static_page.id)
    mock_get_all_pages_visible_to_request.return_value = pages_visible_to_user
    # Mock the apps.hip.utils.get_most_recent_objects function, since it should
    # be used to get the most recent Pages.
    mock_get_most_recent_objects = mocker.patch(
        "apps.hip.utils.get_most_recent_objects"
    )

    request = rf.get("/someurl/")

    context = home_page.get_context(request)

    assert mock_get_all_pages_visible_to_request.called
    assert (request,) == mock_get_all_pages_visible_to_request.call_args_list[0][0]
    assert mock_get_most_recent_objects.called
    assert list(pages_visible_to_user) == list(
        mock_get_most_recent_objects.call_args_list[0][1]["pages_qs"]
    )
    assert context["recent_updates"] == mock_get_most_recent_objects.return_value
