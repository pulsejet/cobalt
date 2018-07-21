from django import forms

class NewCampaignForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField(required=False)
    subject = forms.CharField()
    from_email = forms.EmailField()
    csv = forms.FileField()
    template = forms.CharField()
