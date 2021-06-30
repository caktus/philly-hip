from apps.auth_content.tests.factories import (
    BigCitiesHomePageFactory,
    ClosedPODChildPageFactory,
    ClosedPODHomePageFactory,
    PCWMSAHomePageFactory,
)
from apps.disease_control.tests.factories import (
    DiseaseAndConditionDetailPageFactory,
    DiseaseAndConditionListPageFactory,
    DiseaseControlListPageFactory,
    DiseaseControlPageFactory,
    EmergentHealthTopicListPageFactory,
)
from apps.emergency_response.tests.factories import EmergencyResponsePageFactory
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
        health_alert_list_page,
        HealthAlertDetailPageFactory(parent=health_alert_list_page),
        StaticPageFactory(parent=home_page, title="Static Page"),
        BigCitiesHomePageFactory(parent=home_page, title="Big Cities Home Page"),
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


def test_is_pcwmsa_page(db):
    """Test the is_pcwmsa_page property."""
    home_page = HomePageFactory()
    disease_control_list_page = DiseaseControlListPageFactory(parent=home_page)
    disease_and_condition_list_page = DiseaseAndConditionListPageFactory(
        parent=disease_control_list_page
    )
    emergency_response_page = EmergencyResponsePageFactory(parent=home_page)
    health_alert_list_page = HealthAlertListPageFactory(
        parent=home_page, title="Health Alerts"
    )
    closedpod_home_page = ClosedPODHomePageFactory()
    non_pcwmsa_pages = [
        home_page,
        disease_control_list_page,
        DiseaseControlPageFactory(
            parent=disease_control_list_page, title="Disease Control"
        ),
        disease_and_condition_list_page,
        DiseaseAndConditionDetailPageFactory(parent=disease_and_condition_list_page),
        EmergentHealthTopicListPageFactory(parent=home_page),
        emergency_response_page,
        health_alert_list_page,
        HealthAlertDetailPageFactory(parent=health_alert_list_page),
        StaticPageFactory(parent=home_page, title="Static Page"),
        ClosedPODChildPageFactory(parent=closedpod_home_page),
        closedpod_home_page,
        BigCitiesHomePageFactory(parent=home_page, title="Big Cities Home Page"),
    ]
    for page in non_pcwmsa_pages:
        assert page.is_pcwmsa_page is False

    pcwmsa_home_page = PCWMSAHomePageFactory(
        parent=home_page, title="PCW MSA Home Page"
    )
    pcwmsa_child_page1 = StaticPageFactory(
        parent=pcwmsa_home_page, title="PCW MSA Child Page 1"
    )
    pcwmsa_grandchild_page = StaticPageFactory(
        parent=pcwmsa_child_page1, title="PCW MSA Grandchild Page"
    )
    pcwmsa_child_page2 = StaticPageFactory(
        parent=pcwmsa_home_page, title="PCW MSA Child Page 2"
    )
    pcwmsa_pages = [
        pcwmsa_home_page,
        pcwmsa_child_page1,
        pcwmsa_grandchild_page,
        pcwmsa_child_page2,
    ]
    for page in pcwmsa_pages:
        assert page.is_pcwmsa_page is True


def test_is_bigcities_page(db):
    """Test the is_bigcities_page property."""
    home_page = HomePageFactory()
    disease_control_list_page = DiseaseControlListPageFactory(parent=home_page)
    disease_and_condition_list_page = DiseaseAndConditionListPageFactory(
        parent=disease_control_list_page
    )
    emergency_response_page = EmergencyResponsePageFactory(parent=home_page)
    health_alert_list_page = HealthAlertListPageFactory(
        parent=home_page, title="Health Alerts"
    )
    closedpod_home_page = ClosedPODHomePageFactory(title="Closed POD Home Page")
    non_bigcities_pages = [
        home_page,
        disease_control_list_page,
        DiseaseControlPageFactory(
            parent=disease_control_list_page, title="Disease Control"
        ),
        disease_and_condition_list_page,
        DiseaseAndConditionDetailPageFactory(parent=disease_and_condition_list_page),
        EmergentHealthTopicListPageFactory(parent=home_page),
        emergency_response_page,
        health_alert_list_page,
        HealthAlertDetailPageFactory(parent=health_alert_list_page),
        StaticPageFactory(parent=home_page, title="Static Page"),
        closedpod_home_page,
        ClosedPODChildPageFactory(parent=closedpod_home_page),
        PCWMSAHomePageFactory(parent=home_page, title="PCW MSA Home Page"),
    ]
    for page in non_bigcities_pages:
        assert page.is_bigcities_page is False

    bigcities_home_page = BigCitiesHomePageFactory(
        parent=home_page, title="Big Cities Home Page"
    )
    bigcities_child_page1 = StaticPageFactory(
        parent=bigcities_home_page, title="Big Cities Child Page 1"
    )
    bigcities_grandchild_page = StaticPageFactory(
        parent=bigcities_child_page1, title="Big Cities Grandchild Page"
    )
    bigcities_child_page2 = StaticPageFactory(
        parent=bigcities_home_page, title="Big Cities Child Page 2"
    )
    bigcities_pages = [
        bigcities_home_page,
        bigcities_child_page1,
        bigcities_grandchild_page,
        bigcities_child_page2,
    ]
    for page in bigcities_pages:
        assert page.is_bigcities_page is True
