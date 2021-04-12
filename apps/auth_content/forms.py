from django.forms import ModelForm

from .models import ClosedPODContactInformation


class ClosedPODContactInformationForm(ModelForm):
    use_required_attribute = False

    class Meta:
        model = ClosedPODContactInformation
        fields = "__all__"
