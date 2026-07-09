from django.contrib import admin
from .models import Property, Unit
from .models import Client
from .models import Client, Unit, Lease
from .models import PropertyImage
from .models import Property, Unit, Client, Lease, PropertyImage
from .models import PropertyApplication

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 3 

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name','property_type','total_units','occupied_units','monthly_rent','manager','is_available','featured')
    search_fields = ('name','address','city','district')
    list_filter = ('property_type','city','district','is_available','featured')
    list_display = ('name','property_type','monthly_rent','city','district','featured','is_available',)
    inlines = [PropertyImageInline]

@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ("property","caption","uploaded_at")

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('unit_number','property','monthly_rent','status',)
    search_fields = ('unit_number','property__name',)
    list_filter = ('status','property__name',)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('user','phone_number','national_id')
    search_fields = ('user__username','user__first_name','user__last_name')


@admin.register(Lease)
class LeaseAdmin(admin.ModelAdmin):
    list_display = ('client', 'unit', 'start_date', 'end_date', 'is_active')

@admin.register(PropertyApplication)
class PropertyApplicationAdmin(admin.ModelAdmin):

    list_display = (
        "client",
        "property",
        "manager",
        "status",
        "move_in_date",
        "applied_at",
    )

    list_filter = (
        "status",
    )

    search_fields = (
        "client__user__username",
        "property__name",
    )