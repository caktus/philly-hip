from django.forms import Form


# TODO for DIS-1700: make this form a ModelForm, similar to the HealthAlertSubscriberForm.
class InternalAlertsSubscriberForm(Form):
    def save(self, *args, **kwargs):
        pass


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
