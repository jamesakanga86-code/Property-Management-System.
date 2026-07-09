from django import forms
from .models import Property
from django.contrib.auth.models import User
from .models import PropertyApplication

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'name',
            'property_type',
            'address',
            'description',
            'image',
            'total_units',
            'occupied_units',
            'monthly_rent'
        ]


class ClientRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']   
    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('confirm_password'):
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data
    

class PropertyApplicationForm(forms.ModelForm):

    class Meta:
        model = PropertyApplication

        fields = [
            "move_in_date",
            "message",
        ]

        widgets = {
            "move_in_date": forms.DateInput(
                attrs={"type": "date"}
            ),
            "message": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": "Tell the property manager about yourself..."
                }
            ),
        }