from datetime import date

from apps.disease_control.tests.factories import DiseaseAndConditionDetailPageFactory

from .factories import (
    DataReportDetailArchiveDetailPageFactory,
    DataReportDetailArchiveListPageFactory,
    DataReportDetailPageFactory,
    DataReportListPageFactory,
)


def test_datareportslistpage_context_no_internal_or_external_reports(db, rf):
    """A DataReportListPage with no children and no external_reports has empty 'reports'."""
    reports_list_page = DataReportListPageFactory()
    context = reports_list_page.get_context(rf.get("/someurl/"))
    assert [] == context["reports"]


def test_datareportslistpage_context_only_internal_reports(db, rf):
    """Test the context for a DataReportListPage with children, but no external_reports."""
    # Create a DataReportListPage with some internal reports (DataReportDetailPages).
    reports_list_page = DataReportListPageFactory()
    hep_b = DiseaseAndConditionDetailPageFactory(title="Hepatitis B")
    report_hep_b = DataReportDetailPageFactory(
        title="Hepatitis B", parent=reports_list_page, associated_disease=hep_b
    )
    hiv = DiseaseAndConditionDetailPageFactory(title="HIV/AIDS")
    report_hiv_aids = DataReportDetailPageFactory(
        title="HIV/AIDS", parent=reports_list_page, associated_disease=hiv
    )
    report_annual = DataReportDetailPageFactory(
        title="Annual Report", parent=reports_list_page, associated_disease=None
    )

    context = reports_list_page.get_context(rf.get("/someurl/"))

    # The results should be data for the DataReportDetailPages in alphabetical order.
    expected_results = [
        {
            "title": report_annual.title,
            "url": report_annual.url,
            "update_frequency": report_annual.update_frequency,
            "last_updated": report_annual.latest_revision_created_at,
            "associated_disease": None,
            "external": False,
        },
        {
            "title": report_hep_b.title,
            "url": report_hep_b.url,
            "update_frequency": report_hep_b.update_frequency,
            "last_updated": report_hep_b.latest_revision_created_at,
            "associated_disease": hep_b.page_ptr,
            "external": False,
        },
        {
            "title": report_hiv_aids.title,
            "url": report_hiv_aids.url,
            "update_frequency": report_hiv_aids.update_frequency,
            "last_updated": report_hiv_aids.latest_revision_created_at,
            "associated_disease": hiv.page_ptr,
            "external": False,
        },
    ]
    assert expected_results == context["reports"]


def test_datareportslistpage_context_only_external_reports(db, rf):
    """Test the context for a DataReportListPage with no children, but with external_reports."""
    # Create a DataReportListPage with some external reports.
    external_report_hep_a = {
        "title": "Hepatitis A",
        "url": "example.com/report-hepatitis-a",
        "update_frequency": "Annually",
        # The context should handle if last_updated is a string
        "last_updated": "2020-01-01",
        "external": True,
    }
    external_report_hiv = {
        "title": "HIV/AIDS",
        "url": "example.com/report-hiv-aids",
        "update_frequency": "Sometime",
        # The context should handle if last_updated is a date object
        "last_updated": date(year=2021, month=1, day=1),
        "external": True,
    }
    external_reports_data = [
        {
            "type": "external_reports",  # Block type
            "value": {
                "title": external_report_hiv["title"],
                "url": external_report_hiv["url"],
                "update_frequency": external_report_hiv["update_frequency"],
                "last_updated": external_report_hiv["last_updated"],
            },
        },
        {
            "type": "external_reports",
            "value": {
                "title": external_report_hep_a["title"],
                "url": external_report_hep_a["url"],
                "update_frequency": external_report_hep_a["update_frequency"],
                "last_updated": external_report_hep_a["last_updated"],
            },
        },
    ]
    reports_list_page = DataReportListPageFactory(
        external_reports=external_reports_data
    )

    context = reports_list_page.get_context(rf.get("/someurl/"))

    expected_result_hep_a = external_report_hep_a.copy()
    expected_result_hep_a["last_updated"] = date(
        year=2020, month=1, day=1
    )  # format date to be the expected type
    expected_result_hiv = external_report_hiv.copy()
    expected_result_hiv["last_updated"] = date(
        year=2021, month=1, day=1
    )  # format date to be the expected type
    # The results should be data for the external reports alphabetical order.
    assert [expected_result_hep_a, expected_result_hiv] == context["reports"]


def test_datareportslistpage_context_internal_and_external_reports(db, rf):
    """Test the context for a DataReportListPage with children and with external_reports."""
    # Create a DataReportListPage with an external report.
    external_report_hiv = {
        "title": "HIV/AIDS",
        "url": "example.com/report-hiv-aids",
        "update_frequency": "Sometime",
        "last_updated": "2021-01-01",
        "external": True,
    }
    external_reports_data = [
        {
            "type": "external_reports",
            "value": {
                "title": external_report_hiv["title"],
                "url": external_report_hiv["url"],
                "update_frequency": external_report_hiv["update_frequency"],
                "last_updated": external_report_hiv["last_updated"],
            },
        },
    ]
    reports_list_page = DataReportListPageFactory(
        external_reports=external_reports_data
    )
    # Create  some internal reports (DataReportDetailPages) for the DataReportListPage.
    tuberculosis = DiseaseAndConditionDetailPageFactory(title="Tuberculosis")
    report_tuberculosis = DataReportDetailPageFactory(
        title="Tuberculosis", parent=reports_list_page, associated_disease=tuberculosis
    )
    report_annual = DataReportDetailPageFactory(
        title="Annual Report", parent=reports_list_page, associated_disease=None
    )

    context = reports_list_page.get_context(rf.get("/someurl/"))

    # The results should be data for the internal and external reports in alphabetical order.
    expected_result_external_report_hiv = external_report_hiv.copy()
    expected_result_external_report_hiv["last_updated"] = date(
        year=2021, month=1, day=1
    )  # format date to be the expected type
    expected_results = [
        {
            "title": report_annual.title,
            "url": report_annual.url,
            "update_frequency": report_annual.update_frequency,
            "last_updated": report_annual.latest_revision_created_at,
            "associated_disease": None,
            "external": False,
        },
        expected_result_external_report_hiv,
        {
            "title": report_tuberculosis.title,
            "url": report_tuberculosis.url,
            "update_frequency": report_tuberculosis.update_frequency,
            "last_updated": report_tuberculosis.latest_revision_created_at,
            "associated_disease": tuberculosis.page_ptr,
            "external": False,
        },
    ]
    assert expected_results == context["reports"]


def test_datareportsdetailpage_context_no_archive(db, rf):
    """
    A DataReportDetailPage with no DataReportDetailArchiveListPage children has empty 'archive'.
    """
    report_detail_page = DataReportDetailPageFactory()
    context = report_detail_page.get_context(rf.get("/someurl/"))
    assert context["archive"] is None


def test_datareportsdetailpage_context_with_archive(db, rf):
    """A DataReportDetailPage with a DataReportDetailArchiveListPage child has an 'archive'."""
    report_detail_page = DataReportDetailPageFactory()
    archivepage = DataReportDetailArchiveListPageFactory(parent=report_detail_page)

    context = report_detail_page.get_context(rf.get("/someurl/"))

    assert archivepage == context["archive"]


def test_datareportsdetailpage_context_archive_other_page(db, rf):
    """A DataReportDetailArchiveListPage does not show up for other DataReportDetailPages."""
    report_detail_page1 = DataReportDetailPageFactory()
    report_detail_page2 = DataReportDetailPageFactory()
    # A DataReportDetailArchiveListPage for the report_detail_page1.
    archivepage1 = DataReportDetailArchiveListPageFactory(parent=report_detail_page1)

    context = report_detail_page2.get_context(rf.get("/someurl/"))

    # The context for the report_detail_page2 should not have an archive.
    assert context["archive"] is None


def test_datareportarchivelistpage_context_no_archived_reports(db, rf):
    """A DataReportDetailArchiveListPage with no children has empty 'archived_reports'."""
    archive_page = DataReportDetailArchiveListPageFactory()
    context = archive_page.get_context(rf.get("/someurl/"))
    assert 0 == len(context["archived_reports"])


def test_datareportarchivelistpage_context_with_archived_reports(db, rf):
    """A DataReportDetailArchiveListPage with children has them in the context."""
    archive_page = DataReportDetailArchiveListPageFactory()
    archived_report_2019 = DataReportDetailArchiveDetailPageFactory(
        parent=archive_page, year=2019
    )
    archived_report_2020 = DataReportDetailArchiveDetailPageFactory(
        parent=archive_page, year=2020
    )
    archived_report_2018 = DataReportDetailArchiveDetailPageFactory(
        parent=archive_page, year=2018
    )
    # An archived report for a different archive page (which should not show up
    # in the context for archive_page).
    DataReportDetailArchiveDetailPageFactory(
        parent=DataReportDetailArchiveDetailPageFactory(), year=2019
    )
    # The archived reports should be ordered by year.
    expected_results = [
        archived_report_2020,
        archived_report_2019,
        archived_report_2018,
    ]

    context = archive_page.get_context(rf.get("/someurl/"))

    assert expected_results == list(context["archived_reports"])
