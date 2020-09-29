from django import forms
from .models import AgProfile
from apps.feeder.models import SiteFeeder




class ProfileForm(forms.Form):

    #subscribe_to = forms.ModelMultipleChoiceField(queryset=SiteFeeder.objects.all(),widget = forms.CheckboxSelectMultiple,)
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        sites = SiteFeeder.objects.all()
        for site in sites:
            field_name = f'{site.name}'
            self.fields[field_name] = forms.BooleanField(required=False)