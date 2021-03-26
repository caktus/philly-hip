from apps.auth_content.tests.factories import (  # isort:skip
    ClosedPODChildPageFactory,
    ClosedPODHomePageFactory,
)
from apps.disease_control.tests.factories import (
    DiseaseAndConditionDetailPageFactory,
    DiseaseAndConditionListPageFactory,
    DiseaseControlListPageFactory,
    DiseaseControlPageFactory,
    EmergentHealthTopicListPageFactory,
)
from apps.emergency_response.tests.factories import (
    EmergencyResponsePageFactory,
    HeatIndexPageFactory,
    VolunteerPageFactory,
)
from apps.health_alerts.tests.factories import (
    HealthAlertDetailPageFactory,
    HealthAlertListPageFactory,
)
from apps.hip.tests.factories import HomePageFactory, StaticPageFactory


def test_is_closedpod_page(db):
    """Test the is_closedpod_page property."""
    home_page = HomePageFactory()
    disease_control_list_page = DiseaseControlListPageFactory(parent=home_page)
    disease_and_condition_list_page = DiseaseAndConditionListPageFactory(
        parent=disease_control_list_page
    )
    emergency_response_page = EmergencyResponsePageFactory(parent=home_page)
    health_alert_list_page = HealthAlertListPageFactory(
        parent=home_page, title="Health Alerts"
    )
    non_closedpod_pages = [
        home_page,
        disease_control_list_page,
        DiseaseControlPageFactory(
            parent=disease_control_list_page, title="Disease Control"
        ),
        disease_and_condition_list_page,
        DiseaseAndConditionDetailPageFactory(parent=disease_and_condition_list_page),
        EmergentHealthTopicListPageFactory(parent=home_page),
        emergency_response_page,
        HeatIndexPageFactory(parent=emergency_response_page, title="HeatIndexPage"),
        VolunteerPageFactory(parent=emergency_response_page, title="VolunteerPage"),
        health_alert_list_page,
        HealthAlertDetailPageFactory(parent=health_alert_list_page),
        StaticPageFactory(parent=home_page, title="Static Page"),
    ]
    for page in non_closedpod_pages:
        assert page.is_closedpod_page is False

    closedpod_home_page = ClosedPODHomePageFactory()
    closedpod_pages = [
        ClosedPODChildPageFactory(parent=closedpod_home_page),
        closedpod_home_page,
    ]
    for page in closedpod_pages:
        assert page.is_closedpod_page is True
