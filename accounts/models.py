from django.contrib.auth.models import User
from django.db import models


class Property(models.Model):
    manager = models.ForeignKey(User,on_delete=models.CASCADE,related_name="managed_properties")
    name = models.CharField(max_length=100)
    address = models.TextField()
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='property_images/', null=True, blank=True)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    PROPERTY_TYPES = [('APARTMENT', 'Apartment'),('RENTAL', 'Rental'),('CONDO', 'Condo'),]
    property_type = models.CharField(max_length=20,choices=PROPERTY_TYPES)
    total_units = models.PositiveIntegerField(default=1)
    occupied_units = models.PositiveIntegerField(default=0)
    monthly_rent = models.DecimalField(max_digits=12,decimal_places=2)  
    created_at = models.DateTimeField(auto_now_add=True)
    def vacant_units(self):return self.total_units - self.occupied_units
    def __str__(self):return self.name

class PropertyImage(models.Model):
    property = models.ForeignKey(Property,on_delete=models.CASCADE,related_name="images")
    image = models.ImageField(upload_to="property_gallery/")
    caption = models.CharField( max_length=100,blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):return f"{self.property.name} Image"


class Unit(models.Model):
    property = models.ForeignKey(Property,on_delete=models.CASCADE,related_name='units')
    unit_number = models.CharField(max_length=20)
    monthly_rent = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20,choices=[('VACANT', 'Vacant'),('OCCUPIED', 'Occupied'),('MAINTENANCE', 'Maintenance'),], default='VACANT')
    def __str__(self):return f"{self.property.name} - {self.unit_number}"

class Client(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone_number = models.CharField( max_length=20, blank=True)
    national_id = models.CharField(max_length=50,blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):return self.user.username 

class PropertyApplication(models.Model):

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='applications'
    )

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='applications'
    )

    manager = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_applications'
    )

    message = models.TextField(
        blank=True
    )

    move_in_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    applied_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.client.user.username} → {self.property.name}"


class Lease(models.Model):
    client = models.ForeignKey('Client',on_delete=models.CASCADE)
    unit = models.ForeignKey('Unit',on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):return f"{self.client} - {self.unit}"  
