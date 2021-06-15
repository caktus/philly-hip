from django.forms import Form, ModelForm

from .models import CommunityResponseSubscriber, InternalEmployeeAlertSubscriber


class InternalAlertsSubscriberForm(ModelForm):
    use_required_attribute = False

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


class CommunityResponseSubscriberForm(ModelForm):
    use_required_attribute = False

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


# TODO for DIS-1700: make this form a ModelForm, similar to the HealthAlertSubscriberForm.
class OpioidOverdoseSubscriberForm(Form):
    def save(self, *args, **kwargs):
        pass


# TODO for DIS-1700: make this form a ModelForm, similar to the HealthAlertSubscriberForm.
class CodeBlueCodeRedSubscriberForm(Form):
    def save(self, *args, **kwargs):
        pass


# TODO for DIS-1700: make this form a ModelForm, similar to the HealthAlertSubscriberForm.
class PublicHealthPreparednessSubscriberForm(Form):
    def save(self, *args, **kwargs):
        pass
