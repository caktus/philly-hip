from django.db import models

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page


class DiseaseControlIndexPage(Page):
    max_count = 1

    subpage_types = [
        "disease_control.DiseaseControlPage",
    ]

    def get_context(self, request):
        from .utils import (
            get_topic_specific_guidance_qs,
            get_facility_specific_guidance_qs,
            get_disease_control_services_qs,
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
