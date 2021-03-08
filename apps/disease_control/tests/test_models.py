from datetime import date

from .factories import DiseasePageFactory, EmergentHealthTopicsPageFactory


def test_disease_page_emergent_date_range_no_dates(db):
    """A DiseasePage with no start or end date has an empty emergent_date_range."""
    disease_page_emergent = DiseasePageFactory(
        is_emergent=True,
        emergent_begin_date=None,
        emergent_end_date=None,
    )
    disease_page_nonemergent = DiseasePageFactory(
        is_emergent=False,
        emergent_begin_date=None,
        emergent_end_date=None,
    )

    assert "" == disease_page_emergent.emergent_date_range
    assert "" == disease_page_nonemergent.emergent_date_range


def test_disease_page_emergent_date_range_only_begin_date(db):
    """Test the emergent_date_range for a DiseasePage with only an emergent_begin_date."""
    date_2020_01_01 = date(year=2020, month=1, day=1)

    disease_page_emergent = DiseasePageFactory(
        is_emergent=True,
        emergent_begin_date=date_2020_01_01,
        emergent_end_date=None,
    )
    disease_page_nonemergent = DiseasePageFactory(
        is_emergent=False,
        emergent_begin_date=date_2020_01_01,
        emergent_end_date=None,
    )

    assert "Jan 1, 2020 - Present" == disease_page_emergent.emergent_date_range
    assert "Jan 1, 2020 - Present" == disease_page_nonemergent.emergent_date_range


def test_disease_page_emergent_date_range_only_end_date(db):
    """Test the emergent_date_range for a DiseasePage with only an emergent_end_date."""
    date_2020_01_01 = date(year=2020, month=1, day=1)

    disease_page_emergent = DiseasePageFactory(
        is_emergent=True,
        emergent_begin_date=None,
        emergent_end_date=date_2020_01_01,
    )
    disease_page_nonemergent = DiseasePageFactory(
        is_emergent=False,
        emergent_begin_date=None,
        emergent_end_date=date_2020_01_01,
    )

    assert "Until Jan 1, 2020" == disease_page_emergent.emergent_date_range
    assert "Until Jan 1, 2020" == disease_page_nonemergent.emergent_date_range


def test_disease_page_emergent_date_range_start_and_end_date(db):
    """Test emergent_date_range for DiseasePage with emergent_begin_date and emergent_end_date."""
    date_2019_12_12 = date(year=2019, month=12, day=12)
    date_2021_09_09 = date(year=2021, month=9, day=9)

    disease_page_emergent = DiseasePageFactory(
        is_emergent=True,
        emergent_begin_date=date_2019_12_12,
        emergent_end_date=date_2021_09_09,
    )
    disease_page_nonemergent = DiseasePageFactory(
        is_emergent=False,
        emergent_begin_date=date_2019_12_12,
        emergent_end_date=date_2021_09_09,
    )

    expected_str = "Dec 12, 2019 - Sep 9, 2021"
    assert expected_str == disease_page_emergent.emergent_date_range
    assert expected_str == disease_page_nonemergent.emergent_date_range


def test_emergent_health_topics_page_only_emergent(db, rf):
    """The EmergentHealthTopicsPage only shows emergent diseases."""
    emergent_disease_1 = DiseasePageFactory(is_emergent=True)
    emergent_disease_2 = DiseasePageFactory(is_emergent=True)
    non_emergent_disease = DiseasePageFactory(is_emergent=False)
    emergent_page = EmergentHealthTopicsPageFactory()

    context = emergent_page.get_context(rf.get("/"))

    expected_diseases = [emergent_disease_1, emergent_disease_2]
    assert len(expected_diseases) == len(context["ordered_diseases"])
    for disease in expected_diseases:
        assert disease in context["ordered_diseases"]
