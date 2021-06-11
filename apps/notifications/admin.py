from django.contrib import admin

from import_export.admin import ExportMixin

from .models import InternalEmployeeAlertSubscriber


@admin.register(InternalEmployeeAlertSubscriber)
class InternalEmployeeAlertSubscriberAdmin(ExportMixin, admin.ModelAdmin):
    list_display = (
        "full_name",
        "professional_license",
        "division",
        "work_phone",
    )
    list_filter = (
        "professional_license",
        "division",
    )
    search_fields = (
        "first_name",
        "last_name",
        "work_email",
        "personal_email",
    )

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
