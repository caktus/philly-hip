from ..context_processors import previous_url


def test_previous_url_with_http_referrer(db, rf, mocker):
    """If the request has an HTTP_REFERER, its value is the previous_url."""
    # Mock the apps.common.utils.get_home_page_url function to verify that it
    # does not get called.
    mock_get_home_page_url = mocker.patch("apps.common.utils.get_home_page_url")
    mock_url = "/the_home_page_url/"
    mock_get_home_page_url.return_value = mock_url

    request = rf.get("/someurl")
    referrer_url = "https://example.com"
    request.META["HTTP_REFERER"] = referrer_url

    assert {"previous_url": referrer_url} == previous_url(request)
    # The get_home_page_url() function was not called.
    assert mock_get_home_page_url.called is False


def test_previous_url_with_empty_http_referrer(db, rf, mocker):
    """If the request has an empty HTTP_REFERER, its value is the previous_url."""
    # Mock the apps.common.utils.get_home_page_url function to verify that it
    # does not get called.
    mock_get_home_page_url = mocker.patch("apps.common.utils.get_home_page_url")
    mock_url = "/the_home_page_url/"
    mock_get_home_page_url.return_value = mock_url

    request = rf.get("/someurl")
    referrer_url = ""
    request.META["HTTP_REFERER"] = referrer_url

    assert {"previous_url": referrer_url} == previous_url(request)
    # The get_home_page_url() function was not called.
    assert mock_get_home_page_url.called is False


def test_previous_url_no_http_referrer(db, rf, mocker):
    """If the request has no HTTP_REFERER, previous_url is value of get_home_page_url()."""
    # Mock the apps.common.utils.get_home_page_url() function.
    mock_get_home_page_url = mocker.patch(
        "apps.common.context_processors.get_home_page_url"
    )
    mock_url = "/the_home_page_url/"
    mock_get_home_page_url.return_value = mock_url

    request = rf.get("/someurl")

    assert {"previous_url": mock_url} == previous_url(request)
    assert 1 == mock_get_home_page_url.call_count
