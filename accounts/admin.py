from django.contrib import admin
from .models import Property, Unit


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'property_type',
        'total_units',
        'occupied_units',
        'monthly_rent',
    )

    search_fields = (
        'name',
        'address',
    )

    list_filter = (
        'property_type',
    )


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = (
        'unit_number',
        'property',
        'monthly_rent',
        'status',
    )

    search_fields = (
        'unit_number',
        'property__name',
    )

    list_filter = (
        'status',
    )