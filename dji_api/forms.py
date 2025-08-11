from django import forms
from .models import UserDJICredentials

class DJICredentialsForm(forms.ModelForm):
    class Meta:
        model  = UserDJICredentials
        fields = ['app_id', 'app_key', 'app_license']
        widgets = {
            'app_key': forms.PasswordInput(render_value=True),
        }