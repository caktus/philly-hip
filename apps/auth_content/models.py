from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel
from wagtail.core.fields import RichTextField
from wagtail.search import index

from apps.common.models import HipBasePage
from apps.hip.models import StaticPage


class ClosedPODHomePage(HipBasePage):
    max_count = 1

    subpage_types = [
        "auth_content.ClosedPODChildPage",
    ]

    action_section = RichTextField(
        blank=True,
        help_text="This section will stand out to users, calling them to perform an action.",
    )

    plan_subtitle = models.CharField(
        max_length=255,
        blank=True,
        help_text="The title of the 'Plan' section.",
    )
    plan_text = RichTextField(
        blank=True,
        help_text="The text of the 'Plan' section.",
    )
    exercise_subtitle = models.CharField(
        max_length=255,
        blank=True,
        help_text="The title of the 'Exercise' section.",
    )
    exercise_text = RichTextField(
        blank=True,
        help_text="The text of the 'Exercise' section.",
    )
    about_subtitle = models.CharField(
        max_length=255,
        blank=True,
        help_text="The title of the 'About' section.",
    )
    about_text = RichTextField(
        blank=True,
        help_text="The text of the 'About' section.",
    )

    content_panels = HipBasePage.content_panels + [
        FieldPanel("action_section"),
        MultiFieldPanel(
            [
                FieldPanel("plan_subtitle"),
                FieldPanel("plan_text"),
            ],
            heading="Plan Section",
        ),
        MultiFieldPanel(
            [
                FieldPanel("exercise_subtitle"),
                FieldPanel("exercise_text"),
            ],
            heading="Exercise Section",
        ),
        MultiFieldPanel(
            [
                FieldPanel("about_subtitle"),
                FieldPanel("about_text"),
            ],
            heading="About Section",
        ),
    ]

    search_fields = HipBasePage.search_fields + [
        index.SearchField("action_section"),
        index.SearchField("plan_subtitle"),
        index.SearchField("plan_text"),
        index.SearchField("exercise_subtitle"),
        index.SearchField("exercise_text"),
        index.SearchField("about_subtitle"),
        index.SearchField("about_text"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context["closedpod_children_pages"] = self.get_children()
        context["closedpod_home_url"] = self.url
        return context


class ClosedPODChildPage(StaticPage):
    parent_page_types = ["auth_content.ClosedPODHomePage"]

    description = RichTextField(
        blank=True,
        help_text="The description that will appear for this page on the ClosedPODHomePage.",
    )

    content_panels = HipBasePage.content_panels + [
        FieldPanel("title"),
        FieldPanel("description"),
        StreamFieldPanel("body"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context["closedpod_children_pages"] = self.get_siblings()
        context["closedpod_home_url"] = self.get_parent().url
        return context


class PCWMSAHomePage(StaticPage):
    max_count = 1

    subtitle = models.CharField(
        max_length=255,
        blank=True,
        help_text="A subtitle for the page.",
    )
    action_section = RichTextField(
        blank=True,
        help_text="This section will stand out to users, calling them to perform an action.",
    )

    content_panels = [
        FieldPanel("title"),
        FieldPanel("subtitle"),
        FieldPanel("action_section"),
        StreamFieldPanel("body"),
    ]

    search_fields = HipBasePage.search_fields + [
        index.SearchField("subtitle"),
        index.SearchField("action_section"),
        index.SearchField("body"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context["pcwmsa_home_url"] = self.url
        return context
