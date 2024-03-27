from django.http import Http404

import pytest

from apps.hip.tests.factories import DocumentFactory

from .factories import HealthAlertDetailPageFactory


@pytest.mark.parametrize(
    "page_is_live,page_has_alert_file,expected_response_status_code",
    [
        (True, True, 302),
        (True, False, 404),
        (False, True, 302),
        (False, False, 404),
    ],
)
def test_serve_health_alert_detail_page(
    db,
    client,
    request,
    page_is_live,
    page_has_alert_file,
    expected_response_status_code,
):
    """Assert that loading a HealthAlertDetailPage does not cause a server error."""
    health_alert_page = HealthAlertDetailPageFactory(live=page_is_live, alert_file=None)
    if page_has_alert_file:
        health_alert_page.alert_file = DocumentFactory()
        health_alert_page.save()

    # Call the serve() method, and verify that the response is as expected.
    if expected_response_status_code == 404:
        with pytest.raises(Http404):
            health_alert_page.serve(request)
    else:
        response_serve = health_alert_page.serve(request)
        assert expected_response_status_code == response_serve.status_code
        if expected_response_status_code == 302:
            assert health_alert_page.alert_file.url == response_serve.url

    # Call the serve_preview() method, and verify that the response is as expected.
    if expected_response_status_code == 404:
        with pytest.raises(Http404):
            health_alert_page.serve_preview(request, "")
    else:
        response_serve_preview = health_alert_page.serve_preview(request, "")
        assert expected_response_status_code == response_serve_preview.status_code
        if expected_response_status_code == 302:
            assert health_alert_page.alert_file.url == response_serve_preview.url
