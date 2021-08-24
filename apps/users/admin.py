from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from import_export.admin import ExportMixin
from import_export.resources import ModelResource

from .models import User


class UserResourceBlackList(ModelResource):
    """Provides blacklist for fields that should not be exported.
    Currently this resource omits the password field from being exported.
    """

    class Meta:
        model = User
        exclude = ("password",)


class CustomUserAdmin(ExportMixin, UserAdmin):
    resource_class = UserResourceBlackList

    list_display = ("id", "email", "created", "modified")
    list_filter = ("is_active", "is_staff", "groups")
    search_fields = ("email",)
    ordering = ("email",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),
    )


admin.site.register(User, CustomUserAdmin)
