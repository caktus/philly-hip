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


@admin.register(User)
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

    def get_search_results(self, request, queryset, search_term):
        if not search_term:
            return queryset, False

        email_results = queryset.filter(email__iexact=search_term)
        original_search_fields = self.search_fields
        other_fields = [f for f in original_search_fields if f != "email"]

        if not other_fields:
            return email_results, False

        self.search_fields = other_fields
        other_results, may_have_duplicates = super().get_search_results(
            request, queryset, search_term
        )
        self.search_fields = original_search_fields  # Restore
        queryset = email_results | other_results

        return queryset, may_have_duplicates

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
