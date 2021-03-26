from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel, StreamFieldPanel
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.search import index

from apps.common.models import HipBasePage


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


class DataReportDetailPage(HipBasePage):
    parent_page_types = ["reports.DataReportListPage"]
    subpage_types = []

    update_frequency = models.CharField(max_length=80, blank=True)
    associated_disease = models.ForeignKey(
        "wagtailcore.Page",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="data_report_detail_pages",
    )

    content_panels = HipBasePage.content_panels + [
        FieldPanel("update_frequency"),
        PageChooserPanel(
            "associated_disease", "disease_control.DiseaseAndConditionDetailPage"
        ),
    ]

    search_fields = HipBasePage.search_fields + [
        index.SearchField("update_frequency"),
        index.SearchField("associated_disease"),
    ]
