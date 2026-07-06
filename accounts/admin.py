from django.contrib import admin
from .models import Property, Unit
from .models import Client
from .models import Client, Unit, Lease

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
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'phone_number',
        'national_id'
    )

    search_fields = (
        'user__username',
        'user__first_name',
        'user__last_name'
    )
from .models import Client, Unit, Lease

@admin.register(Lease)
class LeaseAdmin(admin.ModelAdmin):
    list_display = ('client', 'unit', 'start_date', 'end_date', 'is_active')