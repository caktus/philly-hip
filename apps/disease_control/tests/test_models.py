from django.utils.timezone import now, timedelta

from .factories import DiseasePageFactory


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
    date_yesterday = now().date() - timedelta(days=1)

    disease_page_emergent = DiseasePageFactory(
        is_emergent=True,
        emergent_begin_date=date_yesterday,
        emergent_end_date=None,
    )
    disease_page_nonemergent = DiseasePageFactory(
        is_emergent=False,
        emergent_begin_date=date_yesterday,
        emergent_end_date=None,
    )

    assert (
        f"{date_yesterday.strftime('%b %-d, %Y')} - Present"
        == disease_page_emergent.emergent_date_range
    )
    assert (
        f"{date_yesterday.strftime('%b %-d, %Y')} - Present"
        == disease_page_nonemergent.emergent_date_range
    )


def test_disease_page_emergent_date_range_only_end_date(db):
    """Test the emergent_date_range for a DiseasePage with only an emergent_end_date."""
    date_yesterday = now().date() - timedelta(days=1)

    disease_page_emergent = DiseasePageFactory(
        is_emergent=True,
        emergent_begin_date=None,
        emergent_end_date=date_yesterday,
    )
    disease_page_nonemergent = DiseasePageFactory(
        is_emergent=False,
        emergent_begin_date=None,
        emergent_end_date=date_yesterday,
    )

    assert (
        f"Until {date_yesterday.strftime('%b %-d, %Y')}"
        == disease_page_emergent.emergent_date_range
    )
    assert (
        f"Until {date_yesterday.strftime('%b %-d, %Y')}"
        == disease_page_nonemergent.emergent_date_range
    )


def test_disease_page_emergent_date_range_start_and_end_date(db):
    """Test emergent_date_range for DiseasePage with emergent_begin_date and emergent_end_date."""
    date_yesterday = now().date() - timedelta(days=1)
    date_500_days_ago = now().date() - timedelta(days=500)

    disease_page_emergent = DiseasePageFactory(
        is_emergent=True,
        emergent_begin_date=date_500_days_ago,
        emergent_end_date=date_yesterday,
    )
    disease_page_nonemergent = DiseasePageFactory(
        is_emergent=False,
        emergent_begin_date=date_500_days_ago,
        emergent_end_date=date_yesterday,
    )

    expected_str = (
        f"{date_500_days_ago.strftime('%b %-d, %Y')} - "
        f"{date_yesterday.strftime('%b %-d, %Y')}"
    )
    assert expected_str == disease_page_emergent.emergent_date_range
    assert expected_str == disease_page_nonemergent.emergent_date_range
