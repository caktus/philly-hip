from django.forms import ModelForm

from .models import ClosedPODContactInformation


class ClosedPODContactInformationForm(ModelForm):
    use_required_attribute = False

    class Meta:
        model = ClosedPODContactInformation
        fields = "__all__"

    def facility_fields(self):
        return [
            self[name]
            for name in self.fields
            if not name.startswith("primary_") and not name.startswith("secondary_")
        ]

    def primary_fields(self):
        return [self[name] for name in self.fields if name.startswith("primary_")]

    def secondary_fields(self):
        return [self[name] for name in self.fields if name.startswith("secondary_")]
