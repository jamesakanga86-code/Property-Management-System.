from django import forms
from .models import Property


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'name',
            'property_type',
            'address',
            'total_units',
            'occupied_units',
            'monthly_rent'
        ]