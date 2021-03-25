from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel
from wagtail.core.fields import RichTextField
from wagtail.search import index

from apps.common.models import HipBasePage


class DataReportListPage(HipBasePage):
    max_count = 1

    parent_page_types = ["hip.HomePage"]
    subpage_types = ["reports.DataReportDetailPage"]

    description = RichTextField(blank=True)

    content_panels = HipBasePage.content_panels + [
        FieldPanel("description"),
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
