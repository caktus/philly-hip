from django.forms import ModelForm

from .models import HealthAlertSubscriber


class HealthAlertSubscriberForm(ModelForm):
    use_required_attribute = False

    class Meta:
        model = HealthAlertSubscriber
        fields = "__all__"

    def personal_fields(self):
        return [self[name] for name in self.fields if name.startswith("personal_")]

    def agency_fields(self):
        return [self[name] for name in self.fields if name.startswith("agency_")]

    def network_fields(self):
        return [self[name] for name in self.fields if name.startswith("network_")]

    def form_sections(self):
        """Return the sections of this form, including a header, and the fields in the section."""
        return [
            {"header": "Personal Information", "fields": self.personal_fields()},
            {"header": "Agency Information", "fields": self.agency_fields()},
            {
                "header": "Health Alert Network Contact Information",
                "fields": self.network_fields(),
            },
        ]
