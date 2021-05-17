from django.contrib import admin

from import_export.admin import ExportMixin

from .models import ClosedPODContactInformation


@admin.register(ClosedPODContactInformation)
class ClosedPODContactInformationAdmin(ExportMixin, admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "facility_name",
        "facility_id",
    )
    search_fields = (
        "user",
        "facility_name",
        "facility_id",
        "primary_contact_name",
        "secondary_contact_name",
    )
