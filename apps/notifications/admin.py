from django.contrib import admin

from import_export.admin import ExportMixin

from .models import (
    CodeRedCodeBlueSubscriber,
    CommunityResponseSubscriber,
    DrugOverdoseSubscriber,
    InternalEmployeeAlertSubscriber,
    PublicHealthPreparednessSubscriber,
)


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


@admin.register(CommunityResponseSubscriber)
class CommunityResponseSubscriberAdmin(ExportMixin, admin.ModelAdmin):
    list_display = (
        "full_name",
        "organization_name",
        "title",
    )
    list_filter = ("organization_community_members_served",)
    search_fields = (
        "first_name",
        "last_name",
        "organization_name",
        "title",
        "email_address",
    )

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


@admin.register(DrugOverdoseSubscriber)
class DrugOverdoseSubscriberAdmin(ExportMixin, admin.ModelAdmin):
    list_display = (
        "full_name",
        "title",
        "email_address",
    )
    list_filter = ("notification_group",)
    search_fields = (
        "first_name",
        "last_name",
        "medical_specialty",
        "title",
        "email_address",
    )

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


@admin.register(CodeRedCodeBlueSubscriber)
class CodeRedCodeBlueSubscriberAdmin(ExportMixin, admin.ModelAdmin):
    list_display = (
        "full_name",
        "work_email",
        "personal_email",
    )
    search_fields = (
        "first_name",
        "last_name",
        "work_email",
        "personal_email",
    )

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


@admin.register(PublicHealthPreparednessSubscriber)
class PublicHealthPreparednessSubscriberAdmin(ExportMixin, admin.ModelAdmin):
    list_display = (
        "full_name",
        "email_address",
        "organization_name",
    )
    list_filter = ("outreach_request_choice",)
    search_fields = (
        "first_name",
        "last_name",
        "email_address",
    )

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
