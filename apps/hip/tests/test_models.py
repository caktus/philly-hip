from apps.hip.models import ReportDiseasePage


def test_report_disease_page_sets_prev_to_referer(db, rf, mocker):
    """If a request has an HTTP_REFERER, the prev_url is the HTTP_REFERER."""
    # Mock the apps.common.utils.get_home_page_url function to verify that it
    # does not get called.
    mock_get_home_page_url = mocker.patch("apps.common.utils.get_home_page_url")
    mock_url = "/the_home_page_url/"
    mock_get_home_page_url.return_value = mock_url

    sp = ReportDiseasePage()
    # make a fake request and set HTTP_REFERER
    request = rf.get("/foo")
    referring_url = "https://example.com"
    request.META["HTTP_REFERER"] = referring_url

    context = sp.get_context(request)
    assert context["prev_url"] == referring_url
    # The get_home_page_url() function was not called.
    assert mock_get_home_page_url.called is False


def test_report_disease_page_prev_defaults_to_util_function(db, rf, mocker):
    """If a request does not have an HTTP_REFERER, the prev_url use get_home_page_url()."""
    # Mock the apps.common.utils.get_home_page_url function to verify that it
    # gets called.
    mock_get_home_page_url = mocker.patch("apps.common.utils.get_home_page_url")
    mock_url = "/the_home_page_url/"
    mock_get_home_page_url.return_value = mock_url

    s = ReportDiseasePage()
    # make a fake request and leave HTTP_REFERER unset
    request = rf.get("/foo")
    assert request.META.get("HTTP_REFERER") is None

    context = s.get_context(request)

    assert 1 == mock_get_home_page_url.call_count
    assert context["prev_url"] == mock_url
