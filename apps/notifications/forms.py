from django.forms import ModelForm, ValidationError

from .models import (
    CodeRedCodeBlueSubscriber,
    CommunityResponseSubscriber,
    DrugOverdoseSubscriber,
    InternalEmployeeAlertSubscriber,
    PublicHealthPreparednessSubscriber,
)


class InternalAlertsSubscriberForm(ModelForm):
    use_required_attribute = False
    form_id = "internal-alerts-subscriber-form"

    class Meta:
        model = InternalEmployeeAlertSubscriber
        fields = "__all__"

    def about_you_fields(self):
        about_you_field_names = [
            "first_name",
            "last_name",
            "professional_license",
            "languages_spoken",
            "division",
            "ambulatory_health_center",
            "disease_control_program",
            "ehs_program",
        ]
        return [self[name] for name in self.fields if name in about_you_field_names]

    def contact_information_fields(self):
        # return [self[name] for name in self.fields if name.startswith("agency_")]
        contact_info_field_names = [
            "work_phone",
            "work_email",
            "cell_phone",
            "personal_email",
            "home_phone",
            "street_address",
            "city",
            "state",
            "zip_code",
        ]
        return [self[name] for name in self.fields if name in contact_info_field_names]

    def form_sections(self):
        """Return the sections of this form, including a header, and the fields in the section."""
        return [
            {"header": "About You", "fields": self.about_you_fields()},
            {
                "header": "Contact Information",
                "fields": self.contact_information_fields(),
            },
        ]

    def clean(self):
        """
        If the user chooses a specific "division", then another field becomes required.

        A user in the AMBULATORY_HEALTH_SERVICES division must fill in their
        "ambulatory_health_center".
        A user in the DIVISION_OF_DISEASE_CONTROL division must fill in their
        "disease_control_program".
        A user in the ENVIRONMENTAL_HEALTH_SERVICES division must fill in their
        "ehs_program".
        """
        division = self.cleaned_data.get("division")

        required_field_msg = "This field is required."
        if division == str(
            InternalEmployeeAlertSubscriber.DIVISION_CHOICES.AMBULATORY_HEALTH_SERVICES
        ):
            if not self.cleaned_data.get("ambulatory_health_center"):
                raise ValidationError({"ambulatory_health_center": required_field_msg})
        elif division == str(
            InternalEmployeeAlertSubscriber.DIVISION_CHOICES.DIVISION_OF_DISEASE_CONTROL
        ):
            if not self.cleaned_data.get("disease_control_program"):
                raise ValidationError({"disease_control_program": required_field_msg})
        elif division == str(
            InternalEmployeeAlertSubscriber.DIVISION_CHOICES.ENVIRONMENTAL_HEALTH_SERVICES
        ):
            if not self.cleaned_data.get("ehs_program"):
                raise ValidationError({"ehs_program": required_field_msg})


class CommunityResponseSubscriberForm(ModelForm):
    use_required_attribute = False
    form_id = "community-response-subscriber-form"

    class Meta:
        model = CommunityResponseSubscriber
        fields = "__all__"

    def about_you_fields(self):
        about_you_field_names = [
            "first_name",
            "last_name",
            "organization_name",
            "title",
        ]
        return [self[name] for name in self.fields if name in about_you_field_names]

    def contact_information_fields(self):
        contact_info_field_names = [
            "email_address",
            "cell_phone",
        ]
        return [self[name] for name in self.fields if name in contact_info_field_names]

    def organization_info_fields(self):
        organization_info_field_names = [
            "organization_street_address",
            "organization_po_box",
            "organization_zip_code",
            "organization_zip_codes_served",
            "organization_community_members_served",
        ]
        return [
            self[name] for name in self.fields if name in organization_info_field_names
        ]

    def form_sections(self):
        """Return the sections of this form, including a header, and the fields in the section."""
        return [
            {"header": "About You", "fields": self.about_you_fields()},
            {
                "header": "Contact Information",
                "fields": self.contact_information_fields(),
            },
            {
                "header": "Organization Information",
                "fields": self.organization_info_fields(),
            },
        ]


class DrugOverdoseSubscriberForm(ModelForm):
    use_required_attribute = False
    form_id = "opioid-overdose-subscriber-form"

    class Meta:
        model = DrugOverdoseSubscriber
        fields = "__all__"

    def personal_information_fields(self):
        personal_info_field_names = ["first_name", "last_name", "medical_specialty"]
        return [self[name] for name in self.fields if name in personal_info_field_names]

    def company_info_fields(self):
        company_info_field_names = ["company_name", "title", "work_phone"]
        return [self[name] for name in self.fields if name in company_info_field_names]

    def notification_group_fields(self):
        notification_group_field_names = ["notification_group"]
        return [
            self[name] for name in self.fields if name in notification_group_field_names
        ]

    def contact_info_fields(self):
        contact_info_field_names = ["email_address", "mobile_phone"]
        return [self[name] for name in self.fields if name in contact_info_field_names]

    def form_sections(self):
        """Return the sections of this form, including a header, and the fields in the section."""
        return [
            {
                "header": "Personal Information",
                "fields": self.personal_information_fields(),
            },
            {"header": "Company Information", "fields": self.company_info_fields()},
            {
                "header": "Notification Group",
                "fields": self.notification_group_fields(),
            },
            {"header": "Contact Information", "fields": self.contact_info_fields()},
        ]


class CodeRedCodeBlueSubscriberForm(ModelForm):
    use_required_attribute = False
    form_id = "codered-codeblue-subscriber-form"

    class Meta:
        model = CodeRedCodeBlueSubscriber
        fields = "__all__"

    def about_you_fields(self):
        personal_info_field_names = ["first_name", "last_name", "agency_name"]
        return [self[name] for name in self.fields if name in personal_info_field_names]

    def contact_info_fields(self):
        contact_info_field_names = [
            "work_phone",
            "work_email",
            "cell_phone",
            "personal_email",
        ]
        return [self[name] for name in self.fields if name in contact_info_field_names]

    def form_sections(self):
        """Return the sections of this form, including a header, and the fields in the section."""
        return [
            {"header": "About You", "fields": self.about_you_fields()},
            {"header": "Contact Information", "fields": self.contact_info_fields()},
        ]

    def clean(self):
        """
        At least 1 field must not be blank.

        Since all CodeRedCodeBlueSubscriber fields are optional, we must verify
        that at least 1 field has been filled in. Otherwise, we could end up with
        CodeRedCodeBlueSubscriber objects with all empty fields.
        """
        if not [field_name for field_name, value in self.cleaned_data.items() if value]:
            raise ValidationError("Please fill in at least 1 field.")


class PublicHealthPreparednessSubscriberForm(ModelForm):
    use_required_attribute = False
    form_id = "public-health-preparedness-subscriber-form"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Give the 'outreach_request_additional_info' field a CSS class.
        self.fields["outreach_request_additional_info"].widget.attrs.update(
            {"class": "textarea"}
        )

    class Meta:
        model = PublicHealthPreparednessSubscriber
        fields = "__all__"

    def contact_info_fields(self):
        contact_info_field_names = [
            "first_name",
            "last_name",
            "phone_number",
            "email_address",
        ]
        return [self[name] for name in self.fields if name in contact_info_field_names]

    def organization_info_fields(self):
        organization_info_field_names = ["organization_name", "organization_zip_code"]
        return [
            self[name] for name in self.fields if name in organization_info_field_names
        ]

    def outreach_request_fields(self):
        outreach_request_field_names = [
            "outreach_request_choice",
            "outreach_request_additional_info",
        ]
        return [
            self[name] for name in self.fields if name in outreach_request_field_names
        ]

    def form_sections(self):
        """Return the sections of this form, including a header, and the fields in the section."""
        return [
            {"header": "Contact Information", "fields": self.contact_info_fields()},
            {
                "header": "Organization Information",
                "fields": self.organization_info_fields(),
            },
            {"header": "Outreach Request", "fields": self.outreach_request_fields()},
        ]
