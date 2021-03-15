from django.forms import ModelForm

from .models import HealthAlertsSignUp


class HealthAlertsSignUpForm(ModelForm):
    class Meta:
        model = HealthAlertsSignUp
        fields = "__all__"
