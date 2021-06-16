from django.contrib.auth.models import Group

import pytest
from wagtail.core.models import Page, PageViewRestriction

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
)
from apps.emergency_response.tests.factories import EmergencyResponsePageFactory
from apps.hip.tests.factories import StaticPageFactory


@pytest.fixture
def bigcities_homepage():
    """Create a BigCitiesHomePage as a child of the homepage."""
    # The current home page of the site.
    homepage = (
        Page.objects.all().filter(title="Welcome to your new Wagtail site!").first()
    )
    homepage.url_path = "/"
    homepage.save()
    # Create a BigCitiesHomePage
    bigcities_home_page = BigCitiesHomePageFactory(
        parent=homepage, title="Big Cities Home Page"
    )
    # The BigCitiesHomePage is restricted to users in the "Big Cities" Group.
    page_view_restriction = PageViewRestriction.objects.create(
        page=bigcities_home_page, restriction_type="groups"
    )
    group_bigcities = Group.objects.get(name="Big Cities")
    page_view_restriction.groups.add(group_bigcities)

    return bigcities_home_page


@pytest.fixture
def closedpod_homepage():
    """Create a ClosedPODHomePage as a child of the homepage."""
    # The current home page of the site.
    homepage = (
        Page.objects.all().filter(title="Welcome to your new Wagtail site!").first()
    )
    homepage.url_path = "/"
    homepage.save()
    # Create a ClosedPODHomePage
    closedpodhomepage = ClosedPODHomePageFactory(
        parent=homepage, title="Closed POD Home Page"
    )
    # The ClosedPODHomePage is restricted to users in the "Closed POD" Group.
    page_view_restriction = PageViewRestriction.objects.create(
        page=closedpodhomepage, restriction_type="groups"
    )
    group_closedpod = Group.objects.get(name="Closed POD")
    page_view_restriction.groups.add(group_closedpod)

    return closedpodhomepage


@pytest.fixture
def pcwmsa_homepage():
    """Create a PCWMSAHomePage as a child of the homepage."""
    # The current home page of the site.
    homepage = (
        Page.objects.all().filter(title="Welcome to your new Wagtail site!").first()
    )
    homepage.url_path = "/"
    homepage.save()
    # Create a PCWMSAHomePage
    pcw_msa_home_page = PCWMSAHomePageFactory(
        parent=homepage, title="PCW MSA Home Page"
    )
    # The PCWMSAHomePage is restricted to users in the "PCW MSA" Group.
    page_view_restriction = PageViewRestriction.objects.create(
        page=pcw_msa_home_page, restriction_type="groups"
    )
    group_pcwmsa = Group.objects.get(name="PCW MSA")
    page_view_restriction.groups.add(group_pcwmsa)

    return pcw_msa_home_page


@pytest.fixture
def closedpod_homepage_with_descendants(closedpod_homepage):
    """
    Create a ClosedPODHomePage as a child of the homepage, with its own descendants.

    Note: the children and grandchildren of the ClosedPODHomePage do not have any
    PageViewRestrictions. Instead, they inherit their restrictions from the
    ClosedPODHomePage in Wagtail.
    """
    # Create some children of the ClosedPODHomePage.
    planning_page = ClosedPODChildPageFactory(
        parent=closedpod_homepage, title="Planning"
    )
    response_page = ClosedPODChildPageFactory(
        parent=closedpod_homepage, title="Response"
    )
    # Create some grandchildren of the ClosedPODHomePage.
    grandchild1 = StaticPageFactory(
        parent=planning_page, title="ClosedPOD Grandchild 1"
    )
    grandchild2 = StaticPageFactory(
        parent=planning_page, title="ClosedPOD Grandchild 2"
    )
    grandchild3 = StaticPageFactory(
        parent=response_page, title="ClosedPOD Grandchild 3"
    )

    return [
        closedpod_homepage.page_ptr,
        planning_page.page_ptr,
        response_page.page_ptr,
        grandchild1.page_ptr,
        grandchild2.page_ptr,
        grandchild3.page_ptr,
    ]


@pytest.fixture
def pcwmsa_homepage_with_descendants(pcwmsa_homepage):
    """
    Create a PCWMSAHomePage as a child of the homepage, with its own descendants.

    Note: the children and grandchildren of the PCWMSAHomePage do not have any
    PageViewRestrictions. Instead, they inherit their restrictions from the
    PCWMSAHomePage in Wagtail.
    """
    # Create some children of the PCWMSAHomePage.
    leadagency_page = StaticPageFactory(parent=pcwmsa_homepage, title="Lead Agency")
    excerices_page = StaticPageFactory(
        parent=pcwmsa_homepage, title="Full Scale Exercices"
    )
    # Create some grandchildren of the PCWMSAHomePage.
    grandchild1 = StaticPageFactory(parent=leadagency_page, title="PCWMSA Grandchild 1")
    grandchild2 = StaticPageFactory(parent=excerices_page, title="PCWMSA Grandchild 2")
    grandchild3 = StaticPageFactory(parent=excerices_page, title="PCWMSA Grandchild 3")

    return [
        pcwmsa_homepage.page_ptr,
        leadagency_page.page_ptr,
        excerices_page.page_ptr,
        grandchild1.page_ptr,
        grandchild2.page_ptr,
        grandchild3.page_ptr,
    ]


@pytest.fixture
def bigcities_homepage_with_descendants(bigcities_homepage):
    """
    Create a BigCitiesHomePage as a child of the homepage, with its own descendants.

    Note: the children and grandchildren of the BigCitiesHomePage do not have any
    PageViewRestrictions. Instead, they inherit their restrictions from the
    BigCitiesHomePage in Wagtail.
    """
    # Create some children of the BigCitiesHomePage.
    meetings_page = StaticPageFactory(parent=bigcities_homepage, title="Meetings")
    extreme_heat_page = StaticPageFactory(
        parent=bigcities_homepage, title="Extreme Heat"
    )
    # Create some grandchildren of the BigCitiesHomePage.
    grandchild1 = StaticPageFactory(
        parent=meetings_page, title="BigCities Grandchild 1"
    )
    grandchild2 = StaticPageFactory(
        parent=meetings_page, title="BigCities Grandchild 2"
    )
    grandchild3 = StaticPageFactory(
        parent=extreme_heat_page, title="BigCities Grandchild 3"
    )

    return [
        bigcities_homepage.page_ptr,
        meetings_page.page_ptr,
        extreme_heat_page.page_ptr,
        grandchild1.page_ptr,
        grandchild2.page_ptr,
        grandchild3.page_ptr,
    ]


@pytest.fixture
def public_pages_with_descendants():
    """Create some pages (with descendants) that should be visible to all users."""
    # Some public Pages that already exist.
    root_page = Page.objects.get(title="Root")
    home_page = Page.objects.get(title="Welcome to your new Wagtail site!")
    # Create some more public pages.
    disease_control_list_page = DiseaseControlListPageFactory(
        parent=home_page, title="Disease Control List Page"
    )
    disease_control_detail_page = DiseaseControlPageFactory(
        parent=disease_control_list_page, title="Disease Control Detail Page"
    )
    disease_and_condition_list_page = DiseaseAndConditionListPageFactory(
        parent=disease_control_list_page, title="Diseases and Conditions"
    )
    disease_and_condition_ebola_page = DiseaseAndConditionDetailPageFactory(
        parent=disease_and_condition_list_page, title="Ebola"
    )
    emergency_response_page = EmergencyResponsePageFactory(
        parent=home_page, title="Emergency Response"
    )

    return [
        root_page,
        home_page,
        disease_control_list_page.page_ptr,
        disease_control_detail_page.page_ptr,
        disease_and_condition_list_page.page_ptr,
        disease_and_condition_ebola_page.page_ptr,
        emergency_response_page.page_ptr,
    ]


@pytest.fixture
def internal_alert_data():
    """Create data for an InternalAlertsSubscriber."""
    return dict(
        first_name="SpongeBob",
        last_name="SquarePants",
        professional_license="Other",
        languages_spoken="English",
        division="Get Healthy Philly",
        work_phone="(215) 555-0123",
        work_email="spongebob@phila.gov",
        cell_phone="(215)333-4567",
        personal_email="spongebob@squarepants.net",
        home_phone="(215) 444-1234",
        street_address="124 Conch St",
        city="Bikini Bottom",
        state="HI",
        zip_code=98765,
    )


@pytest.fixture
def community_response_notification_data():
    """Create data for a CommunityResponseSubscriber."""
    return dict(
        first_name="SpongeBob",
        last_name="SquarePants",
        organization_name="Krabby Patty Organization",
        title="Fry Cook",
        email_address="spongebob@phila.gov",
        cell_phone="(215)333-4567",
        organization_street_address="831 Bottom Feeder Lane",
        organization_po_box="1",
        organization_zip_code=98765,
        organization_zip_codes_served="98765,99999",
        organization_community_members_served="All of these",
    )


@pytest.fixture
def opioid_overdose_notification_data():
    """Create data for a OpioidOverdoseSubscriber."""
    return dict(
        first_name="SpongeBob",
        last_name="SquarePants",
        medical_specialty="Laughter",
        company_name="Krusty Krab",
        title="Fry Cook",
        work_phone="(215)333-4567",
        notification_group="Community Members",
        email_address="spongebob@phila.gov",
        mobile_phone="(215)333-4567",
    )


@pytest.fixture
def codered_codeblue_notification_data():
    """Create data for a CodeRedCodeBlueSubscriber."""
    return dict(
        first_name="SpongeBob",
        last_name="SquarePants",
        agency_name="Krusty Krab",
        work_phone="(215)333-4567",
        work_email="spongebob@phila.gov",
        cell_phone="(215)333-4567",
        personal_email="spongebob@phila.gov",
    )
