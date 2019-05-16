from django import forms

class NewCampaignForm(forms.Form):
    name = forms.CharField()
    subject = forms.CharField()
    from_email = forms.CharField()
    csv = forms.FileField()
    template = forms.CharField()
    emailvar = forms.CharField()
