import datetime

from django.db import models

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.models import Page
from wagtail.documents.edit_handlers import DocumentChooserPanel


class HealthAlertIndexPage(Page):
    # There can be only one HealthAlertIndexPage
    max_count = 1
    # ... and its children must be HealthAlertPages
    subpage_types = ["health_alerts.HealthAlertPage"]

    def get_context(self, request):
        """
        Add health_alerts queryset and right_nav_headings to context.
        """
        context = super().get_context(request)

        # Get all live HealthAlerts, ordered date descending.
        health_alerts = (
            HealthAlertPage.objects.child_of(self).order_by("-alert_date").live()
        )
        context["health_alerts"] = health_alerts

        # Get list of each year that we have an alert for. This is used for grouping of
        # alerts on the page, as well as to trigger the right scroll bar to be created.
        years = [alert.alert_date.year for alert in health_alerts]
        # the following line removes duplicates but keeps things ordered (unlike sets)
        years = list(dict.fromkeys(years))
        context["right_nav_headings"] = years
        return context


class HealthAlertPage(Page):
    parent_page_types = ["health_alerts.HealthAlertIndexPage"]
    alert_file = models.ForeignKey(
        "wagtaildocs.Document", null=True, blank=True, on_delete=models.SET_NULL
    )

    class Priority(models.IntegerChoices):
        UPDATE = 1
        NOTIFICATION = 2
        ADVISORY = 3
        ALERT = 4

    priority = models.IntegerField(choices=Priority.choices)

    alert_date = models.DateField(default=datetime.date.today)

    # FUTURE FIXME
    # add FK field to Disease/Condition model

    content_panels = (
        [
            DocumentChooserPanel("alert_file"),
        ]
        + Page.content_panels
        + [
            FieldPanel("priority"),
            FieldPanel("alert_date"),
        ]
    )

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


# hmm, this messes with migrations. I might need to think of a better way, but for now
# we'll tell them to put 'topic' in the 'title' field.

# # Override superclass fields for the editor: https://stackoverflow.com/a/57498309/347942
# HealthAlertPage._meta.get_field(
#     "title"
# ).help_text = "Please enter the Topic for this Health Alert."
# HealthAlertPage._meta.get_field("title").verbose_name = "topic"
