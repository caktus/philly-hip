from django.forms import Form, ModelForm

from .models import InternalEmployeeAlertSubscriber


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


# TODO for DIS-1700: make this form a ModelForm, similar to the HealthAlertSubscriberForm.
class CommunityResponseSubscriberForm(Form):
    def save(self, *args, **kwargs):
        pass


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
