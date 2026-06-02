import uuid

import pytest
from wagtail.models import Page

from .factories import (
    DiseaseAndConditionDetailPageFactory,
    DiseaseAndConditionListPageFactory,
    DiseaseControlListPageFactory,
    DiseaseControlPageFactory,
    EmergentHealthTopicListPageFactory,
)


def _content_sections_with(block_type, value):
    """Build a content_sections list with a single block containing the given value."""
    return [{"type": block_type, "value": value, "id": str(uuid.uuid4())}]


@pytest.fixture
def disease_detail_with_content(disease_control_instances):
    """Factory fixture that creates a DiseaseAndConditionDetailPage with a single content block."""

    def _create(block_type, value="needle"):
        return DiseaseAndConditionDetailPageFactory(
            content_sections=_content_sections_with(block_type, value)
        )

    return _create


@pytest.fixture
def disease_control_instances(db):
    DiseaseControlListPageFactory(title="foo")
    DiseaseControlPageFactory(title="foo")
    DiseaseAndConditionListPageFactory(title="foo")
    DiseaseAndConditionDetailPageFactory(title="foo")
    EmergentHealthTopicListPageFactory(title="foo")


def test_no_results(disease_control_instances):
    results = Page.objects.live().search("needle")
    assert len(results) == 0


def test_disease_control_list_page(disease_control_instances):
    obj = DiseaseControlListPageFactory(title="needle")
    results = Page.objects.live().search("needle")
    assert len(results) == 1
    assert results[0].specific == obj


def test_disease_control_page_title(disease_control_instances):
    obj = DiseaseControlPageFactory(title="needle")
    results = Page.objects.live().search("needle")
    assert len(results) == 1
    assert results[0].specific == obj


def test_disease_control_page_description(disease_control_instances):
    obj = DiseaseControlPageFactory(description="needle")
    results = Page.objects.live().search("needle")
    assert len(results) == 1
    assert results[0].specific == obj


def test_disease_and_condition_list_page(disease_control_instances):
    obj = DiseaseAndConditionListPageFactory(title="needle")
    results = Page.objects.live().search("needle")
    assert len(results) == 1
    assert results[0].specific == obj


def test_emergent_health_topic_list_page(disease_control_instances):
    obj = EmergentHealthTopicListPageFactory(title="needle")
    results = Page.objects.live().search("needle")
    assert len(results) == 1
    assert results[0].specific == obj


def test_disease_and_condition_detail_page_title(disease_control_instances):
    obj = DiseaseAndConditionDetailPageFactory(title="needle")
    results = Page.objects.live().search("needle")
    assert len(results) == 1
    assert results[0].specific == obj


def test_disease_and_condition_detail_page_description(disease_detail_with_content):
    obj = disease_detail_with_content("description")
    results = Page.objects.live().search("needle")
    assert len(results) == 1
    assert results[0].specific == obj


def test_disease_and_condition_detail_page_at_a_glance(disease_detail_with_content):
    obj = disease_detail_with_content("at_a_glance")
    results = Page.objects.live().search("needle")
    assert len(results) == 1
    assert results[0].specific == obj


def test_disease_and_condition_detail_page_current_recommendations(
    disease_detail_with_content,
):
    obj = disease_detail_with_content("current_recommendations")
    results = Page.objects.live().search("needle")
    assert len(results) == 1
    assert results[0].specific == obj


def test_disease_and_condition_detail_page_surveillance(disease_detail_with_content):
    obj = disease_detail_with_content("surveillance")
    results = Page.objects.live().search("needle")
    assert len(results) == 1
    assert results[0].specific == obj


def test_disease_and_condition_detail_page_vaccine_info(disease_detail_with_content):
    obj = disease_detail_with_content("vaccine_info")
    results = Page.objects.live().search("needle")
    assert len(results) == 1
    assert results[0].specific == obj


def test_disease_and_condition_detail_page_diagnosis_info(disease_detail_with_content):
    obj = disease_detail_with_content("diagnosis_info")
    results = Page.objects.live().search("needle")
    assert len(results) == 1
    assert results[0].specific == obj


def test_disease_and_condition_detail_page_provider_resources(
    disease_detail_with_content,
):
    obj = disease_detail_with_content("provider_resources")
    results = Page.objects.live().search("needle")
    assert len(results) == 1
    assert results[0].specific == obj
