from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel, StreamFieldPanel
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.search import index

from apps.common.models import HipBasePage
from apps.hip.models import StaticPage


class ExternalReportBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        max_length=255,
        required=True,
        help_text="The title of the external report.",
    )
    url = blocks.URLBlock(required=True, help_text="The URL to the external report.")
    update_frequency = blocks.CharBlock(
        max_length=255,
        required=True,
        help_text="How often this external is udpated (Annually, Quarterly, etc.).",
    )
    last_updated = blocks.DateBlock(required=True)


class DataReportListPage(HipBasePage):
    max_count = 1

    parent_page_types = ["hip.HomePage"]
    subpage_types = ["reports.DataReportDetailPage"]

    description = RichTextField(blank=True)
    external_reports = StreamField(
        [
            ("external_reports", ExternalReportBlock()),
        ],
        blank=True,
    )

    content_panels = HipBasePage.content_panels + [
        FieldPanel("description"),
        StreamFieldPanel("external_reports"),
    ]

    search_fields = HipBasePage.search_fields + [
        index.SearchField("description"),
    ]

    def get_context(self, request):
        """
        Add reports to the page context.

        This method combines both the internal reports (DataReportDetailPages for
        this page) and external reports ('external_reports' for this page),
        alphabetizes them, and returns a list of reports as a 'reports' context
        variable.
        """
        context = super().get_context(request)

        internal_reports = [
            {
                "title": r.title,
                "url": r.url,
                "update_frequency": r.staticpage.datareportdetailpage.update_frequency,
                "last_updated": r.latest_revision_created_at.date()
                if r.latest_revision_created_at
                else None,
                "associated_disease": r.staticpage.datareportdetailpage.associated_disease,
                "external": False,
            }
            for r in self.get_children()
        ]
        external_reports = []
        for report in self.external_reports.raw_data:
            report_data = report["value"]
            report_data["external"] = True
            external_reports.append(report_data)
        reports = internal_reports + external_reports
        reports.sort(key=lambda r: r["title"].lower())

        context["reports"] = reports
        return context


class DataReportDetailPage(StaticPage):
    parent_page_types = ["reports.DataReportListPage"]
    subpage_types = ["reports.DataReportDetailArchiveListPage"]

    update_frequency = models.CharField(max_length=80, blank=True)
    associated_disease = models.ForeignKey(
        "wagtailcore.Page",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="data_report_detail_pages",
    )

    content_panels = StaticPage.content_panels + [
        FieldPanel("update_frequency"),
        PageChooserPanel(
            "associated_disease", "disease_control.DiseaseAndConditionDetailPage"
        ),
    ]

    search_fields = HipBasePage.search_fields + [
        index.SearchField("update_frequency"),
        index.SearchField("associated_disease"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context["archive"] = DataReportDetailArchiveListPage.objects.child_of(
            self
        ).first()
        return context


class DataReportDetailArchiveListPage(HipBasePage):
    max_count_per_parent = 1

    parent_page_types = ["reports.DataReportDetailPage"]
    subpage_types = ["reports.DataReportDetailArchiveDetailPage"]

    content_panels = HipBasePage.content_panels

    search_fields = HipBasePage.search_fields

    def get_context(self, request):
        context = super().get_context(request)
        context[
            "archived_reports"
        ] = DataReportDetailArchiveDetailPage.objects.child_of(self).order_by("-year")
        return context


class DataReportDetailArchiveDetailPage(StaticPage):
    parent_page_types = ["reports.DataReportDetailArchiveListPage"]
    subpage_types = []

    year = models.PositiveSmallIntegerField()

    content_panels = StaticPage.content_panels + [
        FieldPanel("year"),
    ]

    search_fields = HipBasePage.search_fields
