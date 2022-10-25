from django.db import models

from phonenumber_field.modelfields import PhoneNumberField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.search import index

from apps.common.models import HipBasePage
from apps.hip.models import StaticPage
from apps.users.models import User


class ClosedPODHomePage(HipBasePage):
    max_count = 1
    parent_page_types = ["hip.HomePage"]

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
        FieldPanel("body"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context["closedpod_children_pages"] = self.get_siblings()
        context["closedpod_home_url"] = self.get_parent().url
        return context


class PCWMSAHomePage(StaticPage):
    max_count = 1
    parent_page_types = ["hip.HomePage"]
    subpage_types = ["hip.StaticPage", "hip.ListPage"]

    subtitle = models.CharField(
        max_length=255,
        blank=True,
        help_text="A subtitle for the page.",
    )

    content_panels = HipBasePage.content_panels + [
        FieldPanel("subtitle"),
        FieldPanel("action_section"),
        FieldPanel("body"),
    ]

    search_fields = StaticPage.search_fields + [
        index.SearchField("subtitle"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context["pcwmsa_home_url"] = self.url
        return context


class BigCitiesHomePage(StaticPage):
    max_count = 1
    parent_page_types = ["hip.HomePage"]
    subpage_types = ["hip.StaticPage", "hip.ListPage"]

    def get_context(self, request):
        context = super().get_context(request)
        context["bigcities_home_url"] = self.url
        return context


class ClosedPODContactInformation(models.Model):
    """Contact information for a user of the ClosedPOD section of the site."""

    class CELLPHONE_PROVIDERS(models.TextChoices):
        AT_T = "AT&T", "AT&T"
        VERIZON = "Verizon", "Verizon"
        T_MOBILE = "T-Mobile", "T-Mobile"
        DISH = "Dish", "Dish"
        OTHER = "Other", "Other"

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    facility_name = models.CharField("Facility Name*", max_length=255)
    facility_id = models.CharField("Facility ID*", max_length=20)
    phone_number = PhoneNumberField(
        "Phone Number*",
    )
    extension = models.PositiveSmallIntegerField("Extension", blank=True, null=True)
    available_24_7 = models.BooleanField("Available 24/7", default=False)
    special_instructions = models.CharField(
        "Special Instructions for calling this number", max_length=255, blank=True
    )

    primary_contact_name = models.CharField(
        "Name*", max_length=255, help_text="The name of the primary contact"
    )
    primary_contact_work_email = models.EmailField(
        "Work Email*", max_length=255, help_text="The work email of the primary contact"
    )
    primary_contact_personal_email = models.EmailField(
        "Personal / Home Email",
        max_length=255,
        help_text="The personal email of the primary contact",
        blank=True,
    )
    primary_contact_cell_phone = PhoneNumberField(
        "Cell Phone*", help_text="The cell phone number of the primary contact"
    )
    primary_contact_cell_phone_provider = models.CharField(
        "Provider*",
        max_length=8,
        choices=CELLPHONE_PROVIDERS.choices,
        help_text="The cell phone provider of the primary contact",
    )

    secondary_contact_name = models.CharField(
        "Name",
        max_length=255,
        help_text="The name of the secondary contact",
        blank=True,
    )
    secondary_contact_work_email = models.EmailField(
        "Work Email",
        max_length=255,
        help_text="The work email of the secondary contact",
        blank=True,
    )
    secondary_contact_personal_email = models.EmailField(
        "Personal / Home Email",
        max_length=255,
        help_text="The person email of the secondary contact",
        blank=True,
    )
    secondary_contact_cell_phone = PhoneNumberField(
        "Cell Phone",
        help_text="The cell phone number of the secondary contact",
        blank=True,
    )
    secondary_contact_cell_phone_provider = models.CharField(
        "Provider",
        max_length=8,
        choices=CELLPHONE_PROVIDERS.choices,
        help_text="The cell phone provider of the secondary contact",
        blank=True,
    )

    class Meta:
        verbose_name_plural = "Closed POD Contacts"

    def __str__(self):
        return f"ClosedPOD Contact for '{self.facility_name}'"
