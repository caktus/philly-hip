import uuid
from datetime import date

from apps.disease_control.tests.factories import (
    DiseaseAndConditionDetailPageFactory,
    EmergentHealthTopicListPageFactory,
)


def test_disease_and_condition_detail_page_emergent_date_range_no_dates(db):
    """A DiseaseAndConditionDetailPage with no start or end date has an empty emergent_date_range."""
    disease_and_condition_detail_page_emergent = DiseaseAndConditionDetailPageFactory(
        is_emergent=True,
        emergent_begin_date=None,
        emergent_end_date=None,
    )
    disease_and_condition_detail_page_nonemergent = (
        DiseaseAndConditionDetailPageFactory(
            is_emergent=False,
            emergent_begin_date=None,
            emergent_end_date=None,
        )
    )

    assert "" == disease_and_condition_detail_page_emergent.emergent_date_range
    assert "" == disease_and_condition_detail_page_nonemergent.emergent_date_range


def test_disease_and_condition_detail_page_emergent_date_range_only_begin_date(db):
    """Test the emergent_date_range for a DiseaseAndConditionDetailPage with only an emergent_begin_date."""
    date_2020_01_01 = date(year=2020, month=1, day=1)

    disease_and_condition_detail_page_emergent = DiseaseAndConditionDetailPageFactory(
        is_emergent=True,
        emergent_begin_date=date_2020_01_01,
        emergent_end_date=None,
    )
    disease_and_condition_detail_page_nonemergent = (
        DiseaseAndConditionDetailPageFactory(
            is_emergent=False,
            emergent_begin_date=date_2020_01_01,
            emergent_end_date=None,
        )
    )

    assert (
        "Jan 1, 2020 - Present"
        == disease_and_condition_detail_page_emergent.emergent_date_range
    )
    assert (
        "Jan 1, 2020 - Present"
        == disease_and_condition_detail_page_nonemergent.emergent_date_range
    )


def test_disease_and_condition_detail_page_emergent_date_range_only_end_date(db):
    """Test the emergent_date_range for a DiseaseAndConditionDetailPage with only an emergent_end_date."""
    date_2020_01_01 = date(year=2020, month=1, day=1)

    disease_and_condition_detail_page_emergent = DiseaseAndConditionDetailPageFactory(
        is_emergent=True,
        emergent_begin_date=None,
        emergent_end_date=date_2020_01_01,
    )
    disease_and_condition_detail_page_nonemergent = (
        DiseaseAndConditionDetailPageFactory(
            is_emergent=False,
            emergent_begin_date=None,
            emergent_end_date=date_2020_01_01,
        )
    )

    assert (
        "Until Jan 1, 2020"
        == disease_and_condition_detail_page_emergent.emergent_date_range
    )
    assert (
        "Until Jan 1, 2020"
        == disease_and_condition_detail_page_nonemergent.emergent_date_range
    )


def test_disease_and_condition_detail_page_emergent_date_range_start_and_end_date(db):
    """Test emergent_date_range for DiseaseAndConditionDetailPage with emergent_begin_date and emergent_end_date."""
    date_2019_12_12 = date(year=2019, month=12, day=12)
    date_2021_09_09 = date(year=2021, month=9, day=9)

    disease_and_condition_detail_page_emergent = DiseaseAndConditionDetailPageFactory(
        is_emergent=True,
        emergent_begin_date=date_2019_12_12,
        emergent_end_date=date_2021_09_09,
    )
    disease_and_condition_detail_page_nonemergent = (
        DiseaseAndConditionDetailPageFactory(
            is_emergent=False,
            emergent_begin_date=date_2019_12_12,
            emergent_end_date=date_2021_09_09,
        )
    )

    expected_str = "Dec 12, 2019 - Sep 9, 2021"
    assert (
        expected_str == disease_and_condition_detail_page_emergent.emergent_date_range
    )
    assert (
        expected_str
        == disease_and_condition_detail_page_nonemergent.emergent_date_range
    )


def test_emergent_health_topic_list_page_only_emergent(db, rf):
    """The EmergentHealthTopicListPage only shows emergent diseases."""
    emergent_disease_1 = DiseaseAndConditionDetailPageFactory(is_emergent=True)
    emergent_disease_2 = DiseaseAndConditionDetailPageFactory(is_emergent=True)
    non_emergent_disease = DiseaseAndConditionDetailPageFactory(is_emergent=False)
    emergent_page = EmergentHealthTopicListPageFactory()

    context = emergent_page.get_context(rf.get("/"))

    expected_diseases = [emergent_disease_1, emergent_disease_2]
    assert len(expected_diseases) == len(context["ordered_diseases"])
    for disease in expected_diseases:
        assert disease in context["ordered_diseases"]


def test_emergent_health_topic_order_by_latest_revision_created_at(db, rf):
    """The EmergentHealthTopicListPage is ordered by recently updated"""
    disease_1 = DiseaseAndConditionDetailPageFactory(is_emergent=True)
    disease_2 = DiseaseAndConditionDetailPageFactory(is_emergent=True)
    disease_3 = DiseaseAndConditionDetailPageFactory(is_emergent=True)
    disease_4 = DiseaseAndConditionDetailPageFactory(is_emergent=True)
    disease_5 = DiseaseAndConditionDetailPageFactory(is_emergent=True)
    expected_diseases = [
        disease_1,
        disease_2,
        disease_3,
        disease_4,
        disease_5,
    ]
    emergent_page = EmergentHealthTopicListPageFactory()

    for disease in expected_diseases:
        # populate latest_revision_created_at
        # otherwise value is None
        disease.save_revision()

    context = emergent_page.get_context(rf.get("/"))

    ordered_diseases = sorted(
        expected_diseases, key=lambda x: x.latest_revision_created_at, reverse=True
    )
    for i, disease in enumerate(ordered_diseases):
        if i == 0:
            assert (
                disease_5.latest_revision_created_at
                == context["ordered_diseases"][i].latest_revision_created_at
            )
        assert (
            disease.latest_revision_created_at
            == context["ordered_diseases"][i].latest_revision_created_at
        )

    # disease_3 is now the most recently updated emergent disease page
    disease_3.save_revision()

    context = emergent_page.get_context(rf.get("/"))

    for disease in context["ordered_diseases"]:
        if i == 0:
            assert (
                disease_3.latest_revision_created_at
                == context["ordered_diseases"][i].latest_revision_created_at
            )


def _make_content_sections(sections):
    """Helper to build a content_sections list for the StreamField.

    ``sections`` is a dict mapping block type names to rich text values.
    Only included block types will appear in the StreamField.
    """
    return [
        {"type": block_type, "value": value, "id": str(uuid.uuid4())}
        for block_type, value in sections.items()
    ]


def test_content_section_property_returns_value(db):
    """Property accessors return the stored rich text value from the StreamField."""
    sections = _make_content_sections(
        {
            "description": "<p>Test description</p>",
            "at_a_glance": "<p>At a glance info</p>",
            "surveillance": "<p>Surveillance data</p>",
            "vaccine_info": "<p>Vaccine details</p>",
            "diagnosis_info": "<p>Diagnosis info</p>",
            "provider_resources": "<p>Provider resources</p>",
            "current_recommendations": "<p>Recommendations</p>",
        }
    )
    page = DiseaseAndConditionDetailPageFactory(content_sections=sections)

    assert "<p>Test description</p>" in page.description
    assert "<p>At a glance info</p>" in page.at_a_glance
    assert "<p>Surveillance data</p>" in page.surveillance
    assert "<p>Vaccine details</p>" in page.vaccine_info
    assert "<p>Diagnosis info</p>" in page.diagnosis_info
    assert "<p>Provider resources</p>" in page.provider_resources
    assert "<p>Recommendations</p>" in page.current_recommendations


def test_content_section_property_returns_empty_when_block_missing(db):
    """Property accessors return empty string when a block is not in the StreamField."""
    # Only include description — all others should be empty
    sections = _make_content_sections({"description": "<p>Only this</p>"})
    page = DiseaseAndConditionDetailPageFactory(content_sections=sections)

    assert "<p>Only this</p>" in page.description
    assert page.at_a_glance == ""
    assert page.surveillance == ""
    assert page.vaccine_info == ""
    assert page.diagnosis_info == ""
    assert page.provider_resources == ""
    assert page.current_recommendations == ""


def test_content_section_property_returns_empty_when_streamfield_empty(db):
    """Property accessors return empty string when content_sections is completely empty."""
    page = DiseaseAndConditionDetailPageFactory(content_sections=[])

    assert page.description == ""
    assert page.at_a_glance == ""
    assert page.surveillance == ""
    assert page.vaccine_info == ""
    assert page.diagnosis_info == ""
    assert page.provider_resources == ""
    assert page.current_recommendations == ""


def test_right_nav_headings_all_sections_present(db, rf):
    """Right nav includes all section headings when all content sections have content."""
    sections = _make_content_sections(
        {
            "surveillance": "<p>Data</p>",
            "vaccine_info": "<p>Vaccine</p>",
            "diagnosis_info": "<p>Diagnosis</p>",
        }
    )
    page = DiseaseAndConditionDetailPageFactory(content_sections=sections)

    context = page.get_context(rf.get("/"))

    assert "Surveillance" in context["right_nav_headings"]
    assert "Vaccine Info" in context["right_nav_headings"]
    assert "Diagnosis & Management" in context["right_nav_headings"]
    assert "Resources" in context["right_nav_headings"]
    assert page.title in context["right_nav_headings"]
    assert "Health Alerts" in context["right_nav_headings"]


def test_right_nav_headings_no_optional_sections(db, rf):
    """Right nav omits Surveillance/Vaccine/Diagnosis headings when those blocks are missing."""
    sections = _make_content_sections({"description": "<p>Only description</p>"})
    page = DiseaseAndConditionDetailPageFactory(content_sections=sections)

    context = page.get_context(rf.get("/"))

    assert "Surveillance" not in context["right_nav_headings"]
    assert "Vaccine Info" not in context["right_nav_headings"]
    assert "Diagnosis & Management" not in context["right_nav_headings"]
    # These should always be present
    assert page.title in context["right_nav_headings"]
    assert "Health Alerts" in context["right_nav_headings"]
    assert "Resources" in context["right_nav_headings"]


def test_right_nav_headings_partial_sections(db, rf):
    """Right nav only includes headings for sections that have content."""
    sections = _make_content_sections(
        {
            "surveillance": "<p>Surveillance info</p>",
            "diagnosis_info": "<p>Diagnosis</p>",
        }
    )
    page = DiseaseAndConditionDetailPageFactory(content_sections=sections)

    context = page.get_context(rf.get("/"))

    assert "Surveillance" in context["right_nav_headings"]
    assert "Diagnosis & Management" in context["right_nav_headings"]
    assert "Vaccine Info" not in context["right_nav_headings"]


def test_content_section_block_with_empty_value_treated_as_empty(db, rf):
    """A block present in the StreamField but with empty value is treated as no content."""
    sections = _make_content_sections(
        {
            "surveillance": "",
            "vaccine_info": "",
            "diagnosis_info": "",
        }
    )
    page = DiseaseAndConditionDetailPageFactory(content_sections=sections)

    # Properties should return empty string
    assert page.surveillance == ""
    assert page.vaccine_info == ""
    assert page.diagnosis_info == ""

    # Right nav should not include these empty sections
    context = page.get_context(rf.get("/"))
    assert "Surveillance" not in context["right_nav_headings"]
    assert "Vaccine Info" not in context["right_nav_headings"]
    assert "Diagnosis & Management" not in context["right_nav_headings"]


def test_default_content_sections_creates_all_blocks(db):
    """New pages get all 7 content section blocks seeded with empty values."""
    from apps.disease_control.models import default_disease_detail_content_sections

    sections = default_disease_detail_content_sections()

    assert len(sections) == 7
    expected_types = {
        "description",
        "at_a_glance",
        "current_recommendations",
        "surveillance",
        "vaccine_info",
        "diagnosis_info",
        "provider_resources",
    }
    actual_types = {s["type"] for s in sections}
    assert actual_types == expected_types
    # All values should be empty strings
    for section in sections:
        assert section["value"] == ""
        assert "id" in section
