import uuid

from django.db import models

from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.documents import get_document_model
from wagtail.fields import RichTextField, StreamField
from wagtail.search import index

from apps.common.models import HipBasePage
from apps.hip.models import ListSectionBlock, StreamAndNavHeadingBlock

from .blocks import (
    AtAGlanceBlock,
    CurrentRecommendationsBlock,
    DescriptionBlock,
    DiagnosisInfoBlock,
    ProviderResourcesBlock,
    SurveillanceBlock,
    VaccineInfoBlock,
)


CONTENT_SECTION_BLOCK_TYPES = (
    "description",
    "at_a_glance",
    "current_recommendations",
    "surveillance",
    "vaccine_info",
    "diagnosis_info",
    "provider_resources",
)


def default_disease_detail_content_sections():
    return [
        {"type": block_type, "value": "", "id": str(uuid.uuid4())}
        for block_type in CONTENT_SECTION_BLOCK_TYPES
    ]


class DiseaseControlListPage(HipBasePage):
    max_count = 1

    parent_page_types = ["hip.HomePage"]
    subpage_types = [
        "disease_control.DiseaseAndConditionListPage",
        "disease_control.DiseaseControlChildStaticPage",
        "disease_control.DiseaseControlChildListPage",
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
    description = RichTextField(
        blank=True,
        help_text="Text that that will show up as a description of this page on the disease control list page.",
    )

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


class DiseaseControlChildStaticPage(DiseaseControlPage):
    """A Page that inherits from DiseaseControlPage, and copies fields from StaticPage."""

    subpage_types = ["hip.StaticPage", "hip.ListPage"]

    show_left_nav = models.BooleanField(
        default=True,
        blank=True,
        help_text="Should this page show a navigation of the site on the left side of the page?",
    )
    show_breadcrumb = models.BooleanField(
        default=False,
        blank=True,
        help_text="Should this page show a breadcrumb at the top of the page?",
    )
    show_back_button = models.BooleanField(
        default=False,
        blank=True,
        help_text="Should this page show a back button at the top of the page?",
    )
    show_right_nav = models.BooleanField(
        default=False,
        blank=True,
        help_text="Should this page show a navigation of its sections on the right side of the page?",
    )
    body = StreamField(
        [
            ("section", StreamAndNavHeadingBlock()),
        ],
        use_json_field=True,
    )

    content_panels = HipBasePage.content_panels + [
        FieldPanel("show_left_nav"),
        FieldPanel("show_breadcrumb"),
        FieldPanel("show_back_button"),
        FieldPanel("show_right_nav"),
        FieldPanel("description"),
        FieldPanel("body"),
        FieldPanel("page_type"),
    ]
    search_fields = HipBasePage.search_fields + [
        index.SearchField("body"),
        index.SearchField("description"),
    ]

    def get_context(self, request):
        """Add right_nav_headings to the context."""
        context = super().get_context(request)

        # right nav uses the `nav_heading` variable in the template to create links
        right_nav_headings = []
        for block in self.body:
            if block.value["nav_heading"]:
                right_nav_headings.append(block.value["nav_heading"])
        context["right_nav_headings"] = right_nav_headings

        return context

    template = "hip/static_page.html"


class DiseaseControlChildListPage(DiseaseControlPage):
    """A Page that inherits from DiseaseControlPage, and copies fields from ListPage."""

    subpage_types = ["hip.StaticPage", "hip.ListPage"]

    show_breadcrumb = models.BooleanField(
        default=False,
        blank=True,
        help_text="Should this page show a breadcrumb at the top of the page?",
    )
    show_right_nav = models.BooleanField(
        default=False,
        blank=True,
        help_text="Should this page show a navigation of its sections on the right side of the page?",
    )
    list_section = StreamField(
        [
            ("list_section", ListSectionBlock()),
        ],
        use_json_field=True,
    )

    content_panels = HipBasePage.content_panels + [
        FieldPanel("show_breadcrumb"),
        FieldPanel("show_right_nav"),
        FieldPanel("list_section"),
        FieldPanel("description"),
        FieldPanel("page_type"),
    ]
    search_fields = HipBasePage.search_fields + [
        index.SearchField("description"),
        index.SearchField("list_section"),
    ]

    template = "hip/list_page.html"


class DiseaseAndConditionListPage(DiseaseControlPage):
    max_count_per_parent = 1
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

    content_sections = StreamField(
        [
            ("description", DescriptionBlock()),
            ("at_a_glance", AtAGlanceBlock()),
            ("current_recommendations", CurrentRecommendationsBlock()),
            ("surveillance", SurveillanceBlock()),
            ("vaccine_info", VaccineInfoBlock()),
            ("diagnosis_info", DiagnosisInfoBlock()),
            ("provider_resources", ProviderResourcesBlock()),
        ],
        blank=True,
        default=default_disease_detail_content_sections,
        use_json_field=True,
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
        FieldPanel("content_sections"),
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
        index.SearchField("content_sections"),
    ]

    class Media:
        js = ["js/disease_detail_page_admin.js"]

    def _get_content_section_value(self, block_type):
        for block in self.content_sections:
            if block.block_type == block_type:
                return str(block.value)
        return ""

    @property
    def description(self):
        return self._get_content_section_value("description")

    @property
    def at_a_glance(self):
        return self._get_content_section_value("at_a_glance")

    @property
    def current_recommendations(self):
        return self._get_content_section_value("current_recommendations")

    @property
    def surveillance(self):
        return self._get_content_section_value("surveillance")

    @property
    def vaccine_info(self):
        return self._get_content_section_value("vaccine_info")

    @property
    def diagnosis_info(self):
        return self._get_content_section_value("diagnosis_info")

    @property
    def provider_resources(self):
        return self._get_content_section_value("provider_resources")

    def get_context(self, request):
        """
        Add right_nav_headings, the max number of health alerts we show, and any tagged
        documents to the context.
        """
        context = super().get_context(request)

        context["right_nav_headings"] = [self.title, "Health Alerts"]
        if self.surveillance:
            context["right_nav_headings"].append("Surveillance")
        if self.vaccine_info:
            context["right_nav_headings"].append("Vaccine Info")
        if self.diagnosis_info:
            context["right_nav_headings"].append("Diagnosis & Management")
        context["right_nav_headings"].append("Resources")

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
        context["breadcrumb_is_hidden"] = True
        context["ordered_diseases"] = DiseaseAndConditionDetailPage.objects.filter(
            is_emergent=True
        ).order_by("-latest_revision_created_at")
        return context
