from django.forms import ModelForm

from .models import HealthAlertSubscriber


class HealthAlertSubscriberForm(ModelForm):
    class Meta:
        model = HealthAlertSubscriber
        fields = "__all__"

    def personal_fields(self):
        return [self[name] for name in self.fields if name.startswith("personal_")]

    def agency_fields(self):
        return [self[name] for name in self.fields if name.startswith("agency_")]

    def network_fields(self):
        return [self[name] for name in self.fields if name.startswith("network_")]
