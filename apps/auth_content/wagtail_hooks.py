from wagtail_modeladmin.options import ModelAdmin, modeladmin_register

from .models import ClosedPODContactInformation


class ClosedPODContactInformationAdmin(ModelAdmin):
    model = ClosedPODContactInformation
    menu_icon = "form"
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = True
    exclude_from_explorer = False
    list_display = ("facility_name",)
    search_fields = (
        "facility_name",
        "facility_id",
        "primary_contact_name",
        "secondary_contact_name",
    )


modeladmin_register(ClosedPODContactInformationAdmin)
