import pytest
from wagtail.core.models import Page

from .factories import (
    DiseaseAndConditionDetailPageFactory,
    DiseaseAndConditionListPageFactory,
    DiseaseControlListPageFactory,
    DiseaseControlPageFactory,
    EmergentHealthTopicListPageFactory,
)


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
    assert results[0].specific == obj


def test_disease_control_page(disease_control_instances):
    obj = DiseaseControlPageFactory(title="needle")
    results = Page.objects.live().search("needle")
    assert results[0].specific == obj


def test_disease_and_condition_list_page(disease_control_instances):
    obj = DiseaseAndConditionListPageFactory(title="needle")
    results = Page.objects.live().search("needle")
    assert results[0].specific == obj


def test_emergent_health_topic_list_page(disease_control_instances):
    obj = EmergentHealthTopicListPageFactory(title="needle")
    results = Page.objects.live().search("needle")
    assert results[0].specific == obj


def test_disease_and_condition_detail_page_title(disease_control_instances):
    obj = DiseaseAndConditionDetailPageFactory(title="needle")
    results = Page.objects.live().search("needle")
    assert results[0].specific == obj


def test_disease_and_condition_detail_page_description(disease_control_instances):
    obj = DiseaseAndConditionDetailPageFactory(description="needle")
    results = Page.objects.live().search("needle")
    assert results[0].specific == obj


def test_disease_and_condition_detail_page_at_a_glance(disease_control_instances):
    obj = DiseaseAndConditionDetailPageFactory(at_a_glance="needle")
    results = Page.objects.live().search("needle")
    assert results[0].specific == obj


def test_disease_and_condition_detail_page_current_recommendations(
    disease_control_instances,
):
    obj = DiseaseAndConditionDetailPageFactory(current_recommendations="needle")
    results = Page.objects.live().search("needle")
    assert results[0].specific == obj


def test_disease_and_condition_detail_page_surveillance(disease_control_instances):
    obj = DiseaseAndConditionDetailPageFactory(surveillance="needle")
    results = Page.objects.live().search("needle")
    assert results[0].specific == obj


def test_disease_and_condition_detail_page_vaccine_info(disease_control_instances):
    obj = DiseaseAndConditionDetailPageFactory(vaccine_info="needle")
    results = Page.objects.live().search("needle")
    assert results[0].specific == obj


def test_disease_and_condition_detail_page_diagnosis_info(disease_control_instances):
    obj = DiseaseAndConditionDetailPageFactory(diagnosis_info="needle")
    results = Page.objects.live().search("needle")
    assert results[0].specific == obj


def test_disease_and_condition_detail_page_provider_resources(
    disease_control_instances,
):
    obj = DiseaseAndConditionDetailPageFactory(provider_resources="needle")
    results = Page.objects.live().search("needle")
    assert results[0].specific == obj
