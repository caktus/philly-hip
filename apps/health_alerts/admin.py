from django.contrib import admin

from import_export.admin import ExportMixin

from .models import HealthAlertSubscriber


@admin.register(HealthAlertSubscriber)
class HealthAlertSubscriberAdmin(ExportMixin, admin.ModelAdmin):
    list_display = (
        "full_name",
        "agency_name",
        "network_email",
        "network_fax",
        "agency_type",
    )
    list_filter = (
        "agency_name",
        "agency_type",
    )
    search_fields = (
        "personal_first_name",
        "personal_last_name",
        "network_email",
        "agency_name",
        "agency_type",
    )

    def full_name(self, obj):
        return f"{obj.personal_first_name} {obj.personal_last_name}"
