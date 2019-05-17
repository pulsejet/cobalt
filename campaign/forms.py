"""Forms for creating campaigns."""
from django import forms

class NewCampaignForm(forms.Form):
    """Form for creating new campaign."""

    name = forms.CharField()
    subject = forms.CharField()
    from_email = forms.CharField()
    csv = forms.FileField()
    template = forms.CharField()
    emailvar = forms.CharField()
    mailtrack = forms.BooleanField(required=False)
