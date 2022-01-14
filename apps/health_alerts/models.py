import datetime

from django.db import models
from django.shortcuts import redirect

from phonenumber_field.modelfields import PhoneNumberField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.search import index

from apps.common.models import HipBasePage
from apps.disease_control.models import DiseaseAndConditionDetailPage

from .utils import zipcode_validator


class HealthAlertListPage(HipBasePage):
    # There can be only one HealthAlertListPage
    max_count = 1
    parent_page_types = ["hip.HomePage"]
    subpage_types = ["health_alerts.HealthAlertDetailPage"]

    def get_context(self, request):
        """
        Add health_alerts queryset and right_nav_headings to context.
        """
        context = super().get_context(request)

        # Get all live HealthAlerts, ordered date descending.
        health_alerts = (
            HealthAlertDetailPage.objects.child_of(self).order_by("-alert_date").live()
        )
        context["health_alerts"] = health_alerts

        # Get list of each year that we have an alert for. This is used for grouping of
        # alerts on the page, as well as to trigger the right scroll bar to be created.
        years = [alert.alert_date.year for alert in health_alerts]
        # the following line removes duplicates but keeps things ordered (unlike sets)
        years = list(dict.fromkeys(years))
        context["right_nav_headings"] = years

        # Get list of conditions attached to all of our health alerts, ordered by title
        conditions = DiseaseAndConditionDetailPage.objects.exclude(
            health_alerts=None
        ).order_by("title")
        context["conditions"] = conditions
        return context


class HealthAlertDetailPage(HipBasePage):
    parent_page_types = ["health_alerts.HealthAlertListPage"]
    subpage_types = []
    alert_file = models.ForeignKey(
        "hip.HIPDocument", null=True, blank=True, on_delete=models.SET_NULL
    )

    class Priority(models.IntegerChoices):
        UPDATE = 1
        NOTIFICATION = 2
        ADVISORY = 3
        ALERT = 4

    priority = models.IntegerField(choices=Priority.choices)

    alert_date = models.DateField(default=datetime.date.today)

    disease = models.ForeignKey(
        DiseaseAndConditionDetailPage,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="health_alerts",
    )

    content_panels = HipBasePage.content_panels + [
        DocumentChooserPanel("alert_file"),
        FieldPanel("priority"),
        FieldPanel("alert_date"),
        FieldPanel("disease"),
    ]
    search_fields = HipBasePage.search_fields + [
        index.SearchField("get_priority_display"),
    ]

    def get_priority_icon(self):
        """
        Get the proper icon for this priority.
        """
        if self.priority == self.Priority.UPDATE:
            return "fa-arrow-alt-circle-up"
        elif self.priority == self.Priority.NOTIFICATION:
            return "fa-info-circle"
        elif self.priority == self.Priority.ADVISORY:
            return "fa-exclamation-circle"
        elif self.priority == self.Priority.ALERT:
            return "fa-exclamation-triangle"
        return ""

    def get_priority_color(self):
        """Get the proper color for the priority."""
        if self.priority == self.Priority.UPDATE:
            return "update-hip"
        elif self.priority == self.Priority.NOTIFICATION:
            return "notification-hip"
        elif self.priority == self.Priority.ADVISORY:
            return "advisory-hip"
        elif self.priority == self.Priority.ALERT:
            return "alert-hip"
        return ""

    def serve(self, request):
        return redirect(self.alert_file.url)


class HealthAlertSubscriber(models.Model):
    """Stores users that indicate they would like to
    subscribe to health alerts

    This model is a standard django model used
    to store health alert subscribers. Instances
    are made available in the django admin as opposed
    to the wagtail cms. From the information stored here
    admins will be able to send out newsletters. The
    actual sending of newsletters is a process not
    managed by the current iteration of this
    application.
    """

    personal_first_name = models.CharField(
        "First Name*",
        max_length=255,
        default="",
    )
    personal_last_name = models.CharField(
        "Last Name*",
        max_length=255,
        default="",
    )
    personal_medical_expertise = models.CharField(
        "Medical Specialty/Expertise*",
        max_length=255,
        default="",
    )
    personal_professional_license = models.CharField(
        "Professional License*",
        max_length=255,
        default="",
    )
    agency_name = models.CharField("Agency Name*", max_length=255, default="")

    class AGENCY_TYPE_CHOICES(models.TextChoices):
        ANIMAL_VETERINARY_CLINICS = "AV", "Animal and Veterinary Clinics"
        BUSINESSES_COMMUNITY_ORGANIZATIONS = (
            "BCO",
            "Businesses and Community Organizations",
        )
        CHILDCARE_SERVICES_DAYCARES = "CSD", "Child Care Services and Daycares"
        DENTAL_OFFICES_CLINICS = "DOC", "Dental Offices and Clinics"
        HOSPITALS_HEALTHCARE = "HH", "Hospitals and Healthcare"
        NURSING_PERSONAL_CARE_HOMES = "NPH", "Nursing and Personal Care Homes"
        PDPH_INTERNAL = "PDPH", "PDPH (Internal)"
        PHARMACY = "P", "Pharmacy"
        PUBLIC_HEALTH_REGIONAL_PARTNERS = "PHRP", "Public Health and Regional Partners"
        UNIVERSITY_STUDENT_HEALTH = "USH", "University and Student Health"
        OTHER = "O", "Other"

    agency_type = models.CharField(
        "Agency Type*", max_length=4, choices=AGENCY_TYPE_CHOICES.choices
    )
    agency_zip_code = models.CharField(
        "Agency Zip Code*", max_length=10, default="", validators=[zipcode_validator]
    )
    agency_position = models.CharField("Position/Title*", max_length=255, default="")
    agency_work_phone = PhoneNumberField("Work Phone", null=True, blank=True)
    network_email = models.EmailField("Email Address*", default="")
    network_fax = PhoneNumberField("Fax Number*")
