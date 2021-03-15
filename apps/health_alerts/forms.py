from django.forms import ModelForm

from .models import HealthAlertsSignUp


class HealthAlertsSignUpForm(ModelForm):
    class Meta:
        model = HealthAlertsSignUp
        fields = "__all__"

    def personal_fields(self):
        return [self[name] for name in self.fields if name.startswith("personal_")]

    def agency_fields(self):
        return [self[name] for name in self.fields if name.startswith("agency_")]

    def network_fields(self):
        return [self[name] for name in self.fields if name.startswith("network_")]
