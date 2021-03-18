from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.core.fields import RichTextField
from wagtail.documents import get_document_model
from wagtail.search import index

from apps.common.models import HipBasePage


class DiseaseControlListPage(HipBasePage):
    max_count = 1

    parent_page_types = ["hip.HomePage"]
    subpage_types = [
        "disease_control.DiseaseAndConditionListPage",
        # Generic Placeholder until other subpages are added
        "disease_control.DiseaseControlPage",
    ]

    def get_context(self, request):
        from .utils import (
            get_disease_control_services_qs,
            get_facility_specific_guidance_qs,
            get_topic_specific_guidance_qs,
            get_visible_section_headers,
        )

        context = super().get_context(request)
        context["right_nav_headings"] = get_visible_section_headers()
        context["topic_pages"] = get_topic_specific_guidance_qs()
        context["facility_pages"] = get_facility_specific_guidance_qs()
        context["disease_control_pages"] = get_disease_control_services_qs()
        return context


class DiseaseControlPage(HipBasePage):
    parent_page_types = ["disease_control.DiseaseControlListPage"]
    subpage_types = []
    description = RichTextField(blank=True)

    class Type(models.IntegerChoices):
        TOPIC_SPECIFIC_GUIDANCE = 1
        FACILITY_SPECIFIC_GUIDANCE = 2
        DISEASE_CONTROL_SERVICES = 3

    page_type = models.IntegerField(
        choices=Type.choices, help_text=("Under which sub-heading does this page go?")
    )

    content_panels = HipBasePage.content_panels + [
        FieldPanel("description"),
        FieldPanel("page_type"),
    ]

    search_fields = HipBasePage.search_fields + [
        index.SearchField("description"),
    ]


class DiseaseAndConditionListPage(DiseaseControlPage):
    subpage_types = [
        "disease_control.DiseaseAndConditionDetailPage",
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context["ordered_diseases"] = self.get_children().order_by("title")
        return context


class DiseaseAndConditionDetailPage(HipBasePage):
    parent_page_types = ["disease_control.DiseaseAndConditionListPage"]
    subpage_types = []

    description = RichTextField(
        blank=True,
        help_text="Enter a short description which will be shown on the page listing diseases and conditions.",
    )
    at_a_glance = RichTextField(blank=True)
    current_recommendations = RichTextField(blank=True)
    surveillance = RichTextField(blank=True)
    vaccine_info = RichTextField(blank=True)
    diagnosis_info = RichTextField(blank=True)
    provider_resources = RichTextField(
        blank=True,
        help_text="List resources that will be useful for healthcare providers. Resources for patients and community will be pulled automatically by including any documents that are tagged with the title of this disease/condition.",
    )

    is_emergent = models.BooleanField(
        default=False,
        help_text="Should this disease be tagged as emergent?",
    )
    emergent_begin_date = models.DateField(
        blank=True,
        null=True,
        help_text=("Choose the date this disease became an emergent concern"),
    )
    emergent_end_date = models.DateField(
        blank=True,
        null=True,
        help_text=(
            "Choose the date this disease stopped being an emergent concern. Leave "
            "blank if it is still an emergent concern."
        ),
    )

    content_panels = HipBasePage.content_panels + [
        FieldPanel("description"),
        FieldPanel("at_a_glance"),
        FieldPanel("current_recommendations"),
        FieldPanel("surveillance"),
        FieldPanel("vaccine_info"),
        FieldPanel("diagnosis_info"),
        FieldPanel("provider_resources"),
        MultiFieldPanel(
            [
                FieldPanel("is_emergent"),
                FieldPanel("emergent_begin_date"),
                FieldPanel("emergent_end_date"),
            ],
            heading="Emergent Data",
        ),
    ]

    search_fields = HipBasePage.search_fields + [
        index.SearchField("description"),
        index.SearchField("at_a_glance"),
        index.SearchField("current_recommendations"),
        index.SearchField("surveillance"),
        index.SearchField("vaccine_info"),
        index.SearchField("diagnosis_info"),
        index.SearchField("provider_resources"),
    ]

    def get_context(self, request):
        """
        Add right_nav_headings, the max number of health alerts we show, and any tagged
        documents to the context.
        """
        context = super().get_context(request)

        context["right_nav_headings"] = [
            self.title,
            "Health Alerts",
            "Surveillance",
            "Vaccine Info",
            "Diagnosis & Management",
            "Resources",
        ]

        # prepare health alerts
        HEALTH_ALERT_MAX = 5
        health_alerts = self.health_alerts.order_by("-alert_date")
        if health_alerts.count() > HEALTH_ALERT_MAX:
            show_more_health_alerts = True
        else:
            show_more_health_alerts = False
        context["health_alerts"] = health_alerts[:HEALTH_ALERT_MAX]
        context["show_more_health_alerts"] = show_more_health_alerts

        # find documents tagged with this condition's title
        Document = get_document_model()
        context["documents"] = Document.objects.filter(tags__name__iexact=self.title)
        return context

    @property
    def emergent_date_range(self):
        """Return a string representing the date range that this disease was emergent."""
        begin_date = (
            self.emergent_begin_date.strftime("%b %-d, %Y")
            if self.emergent_begin_date
            else None
        )
        end_date = (
            self.emergent_end_date.strftime("%b %-d, %Y")
            if self.emergent_end_date
            else None
        )

        if begin_date and end_date:
            return f"{begin_date} - {end_date}"
        elif begin_date and not end_date:
            return f"{begin_date} - Present"
        elif not begin_date and end_date:
            return f"Until {end_date}"
        else:
            return ""


class EmergentHealthTopicListPage(HipBasePage):
    template = "disease_control/disease_and_condition_list_page.html"

    def get_context(self, request):
        context = super().get_context(request)
        context["ordered_diseases"] = DiseaseAndConditionDetailPage.objects.filter(
            is_emergent=True
        ).order_by("-latest_revision_created_at")
        return context
