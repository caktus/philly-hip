from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page


class DiseaseControlIndexPage(Page):
    max_count = 1

    subpage_types = [
        "disease_control.DiseasesAndConditionsPage",
    ]

    def get_context(self, request):
        from .utils import (
            get_disease_control_services_qs,
            get_facility_specific_guidance_qs,
            get_topic_specific_guidance_qs,
        )

        context = super().get_context(request)
        context["topic_pages"] = get_topic_specific_guidance_qs()
        context["facility_pages"] = get_facility_specific_guidance_qs()
        context["disease_control_pages"] = get_disease_control_services_qs()
        return context


class DiseaseControlPage(Page):
    parent_page_types = ["disease_control.DiseaseControlIndexPage"]
    description = RichTextField(blank=True)

    class Type(models.IntegerChoices):
        TOPIC_SPECIFIC_GUIDANCE = 1
        FACILITY_SPECIFIC_GUIDANCE = 2
        DISEASE_CONTROL_SERVICES = 3

    page_type = models.IntegerField(
        choices=Type.choices, help_text=("Under which sub-heading does this page go?")
    )

    content_panels = [
        FieldPanel("title"),
        FieldPanel("description"),
        FieldPanel("page_type"),
    ]


class DiseasesAndConditionsPage(DiseaseControlPage):
    subpage_types = [
        "disease_control.DiseasePage",
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context["ordered_diseases"] = self.get_children().order_by("title")
        return context


class DiseasePage(Page):
    parent_page_types = ["disease_control.DiseasesAndConditionsPage"]

    description = RichTextField(blank=True)

    is_emergent = models.BooleanField(
        default=False,
        help_text="Is this an emergent disease?",
    )
    emergent_begin_date = models.DateField(
        blank=True,
        null=True,
        help_text=("If this is an emergent disease, choose the date it emerged"),
    )
    emergent_end_date = models.DateField(
        blank=True,
        null=True,
        help_text=(
            "If this is an emergent disease, choose the date it stopped emerging. "
            "Leave blank if it is still emerging"
        ),
    )

    content_panels = [
        FieldPanel("title"),
        FieldPanel("description"),
        MultiFieldPanel(
            [
                FieldPanel("is_emergent"),
                FieldPanel("emergent_begin_date"),
                FieldPanel("emergent_end_date"),
            ],
            heading="Emergent Data",
        ),
    ]

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
