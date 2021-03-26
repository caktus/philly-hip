from apps.disease_control.tests.factories import DiseaseAndConditionDetailPageFactory

from .factories import DataReportDetailPageFactory, DataReportListPageFactory


def test_datareportslistpage_context_no_internal_or_external_reports(db, rf):
    """A DataReportListPage with no children and no external_reports has empty 'reports'."""
    reports_list_page = DataReportListPageFactory()
    context = reports_list_page.get_context(rf.get("/someurl/"))
    assert [] == context["reports"]


def test_datareportslistpage_context_only_internal_reports(db, rf):
    """A DataReportListPage with no children and no external_reports has empty 'reports'."""
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
        },
        {
            "title": report_hep_b.title,
            "url": report_hep_b.url,
            "update_frequency": report_hep_b.update_frequency,
            "last_updated": report_hep_b.latest_revision_created_at,
            "associated_disease": hep_b.page_ptr,
        },
        {
            "title": report_hiv_aids.title,
            "url": report_hiv_aids.url,
            "update_frequency": report_hiv_aids.update_frequency,
            "last_updated": report_hiv_aids.latest_revision_created_at,
            "associated_disease": hiv.page_ptr,
        },
    ]
    assert expected_results == context["reports"]


def test_datareportslistpage_context_only_external_reports(db, rf):
    """A DataReportListPage with no children and no external_reports has empty 'reports'."""
    # Create a DataReportListPage with some external reports.
    external_report_hep_a = {
        "title": "Hepatitis A",
        "url": "example.com/report-hepatitis-a",
        "update_frequency": "Annually",
        "last_updated": "2020-01-01",
    }
    external_report_hiv = {
        "title": "HIV/AIDS",
        "url": "example.com/report-hiv-aids",
        "update_frequency": "Sometime",
        "last_updated": "2021-01-01",
    }
    reports_list_page = DataReportListPageFactory(
        external_reports__0__external_reports__title=external_report_hiv["title"],
        external_reports__0__external_reports__url=external_report_hiv["url"],
        external_reports__0__external_reports__update_frequency=external_report_hiv[
            "update_frequency"
        ],
        external_reports__0__external_reports__last_updated=external_report_hiv[
            "last_updated"
        ],
        external_reports__1__external_reports__title=external_report_hep_a["title"],
        external_reports__1__external_reports__url=external_report_hep_a["url"],
        external_reports__1__external_reports__update_frequency=external_report_hep_a[
            "update_frequency"
        ],
        external_reports__1__external_reports__last_updated=external_report_hep_a[
            "last_updated"
        ],
    )

    context = reports_list_page.get_context(rf.get("/someurl/"))

    # The results should be data for the external reports alphabetical order.
    assert [external_report_hep_a, external_report_hiv] == context["reports"]


def test_datareportslistpage_context_internal_and_external_reports(db, rf):
    """A DataReportListPage with no children and no external_reports has empty 'reports'."""
    # Create a DataReportListPage with an external report.
    external_report_hiv = {
        "title": "HIV/AIDS",
        "url": "example.com/report-hiv-aids",
        "update_frequency": "Sometime",
        "last_updated": "2021-01-01",
    }
    reports_list_page = DataReportListPageFactory(
        external_reports__0__external_reports__title=external_report_hiv["title"],
        external_reports__0__external_reports__url=external_report_hiv["url"],
        external_reports__0__external_reports__update_frequency=external_report_hiv[
            "update_frequency"
        ],
        external_reports__0__external_reports__last_updated=external_report_hiv[
            "last_updated"
        ],
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

    # The results should be data for the external reports alphabetical order.
    expected_results = [
        {
            "title": report_annual.title,
            "url": report_annual.url,
            "update_frequency": report_annual.update_frequency,
            "last_updated": report_annual.latest_revision_created_at,
            "associated_disease": None,
        },
        external_report_hiv,
        {
            "title": report_tuberculosis.title,
            "url": report_tuberculosis.url,
            "update_frequency": report_tuberculosis.update_frequency,
            "last_updated": report_tuberculosis.latest_revision_created_at,
            "associated_disease": tuberculosis.page_ptr,
        },
    ]
    assert expected_results == context["reports"]
