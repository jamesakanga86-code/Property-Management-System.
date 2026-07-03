from django.db import models


class Property(models.Model):
    PROPERTY_TYPES = [
        ('APARTMENT', 'Apartment'),
        ('RENTAL', 'Rental'),
        ('CONDO', 'Condo'),
    ]

    name = models.CharField(max_length=100)
    property_type = models.CharField(
        max_length=20,
        choices=PROPERTY_TYPES
    )
    address = models.TextField()

    total_units = models.PositiveIntegerField(default=1)
    occupied_units = models.PositiveIntegerField(default=0)

    monthly_rent = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def vacant_units(self):
        return self.total_units - self.occupied_units

    def __str__(self):
        return self.name
    
class Unit(models.Model):
    UNIT_STATUS = [
        ('VACANT', 'Vacant'),
        ('OCCUPIED', 'Occupied'),
        ('MAINTENANCE', 'Maintenance'),
    ]

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='units'
    )

    unit_number = models.CharField(max_length=20)

    monthly_rent = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=UNIT_STATUS,
        default='VACANT'
    )

    def __str__(self):
        return f"{self.property.name} - {self.unit_number}"