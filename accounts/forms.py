from django import forms
from .models import Property
from django.contrib.auth.models import User
from .models import PropertyApplication

from django import forms
from .models import Property


class PropertyForm(forms.ModelForm):

    class Meta:
        model = Property

        fields = [
            "name",
            "property_type",
            "address",
            "city",
            "district",
            "description",
            "image",
            "total_units",
            "occupied_units",
            "monthly_rent",
            "is_available",
            "featured",
        ]

        widgets = {

            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Property Name"
            }),

            "property_type": forms.Select(attrs={
                "class": "form-select"
            }),

            "monthly_rent": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Monthly Rent"
            }),

            "city": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "City"
            }),

            "district": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "District"
            }),

            "address": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Full Address"
            }),

            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Describe the property..."
            }),

            "total_units": forms.NumberInput(attrs={
                "class": "form-control"
            }),

            "occupied_units": forms.NumberInput(attrs={
                "class": "form-control"
            }),

            "image": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),

            "is_available": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),

            "featured": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),

        }


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
    "phone_number",
    "national_id",
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