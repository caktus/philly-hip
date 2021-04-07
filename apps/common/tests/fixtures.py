import pytest
from wagtail.core.models import Page

from apps.auth_content.tests.factories import ClosedPODChildPageFactory
from apps.disease_control.tests.factories import (
    DiseaseAndConditionDetailPageFactory,
    DiseaseAndConditionListPageFactory,
    DiseaseControlListPageFactory,
    DiseaseControlPageFactory,
)
from apps.emergency_response.tests.factories import EmergencyResponsePageFactory
from apps.hip.tests.factories import StaticPageFactory


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