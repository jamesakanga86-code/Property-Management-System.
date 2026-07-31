from email.mime import application
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import context
from .models import Property, Unit, Client, Lease
from .forms import PropertyForm, PropertyApplicationForm
from django.shortcuts import get_object_or_404
from .models import PropertyApplication
from django.shortcuts import redirect
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PropertyApplicationForm
from .models import Property, PropertyApplication
from django.contrib import messages
from django.db.models import Sum
from django.db.models.functions import TruncDay
from django.db.models import Count
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.shortcuts import (render,redirect,get_object_or_404)
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from .utils import record_occupancy_snapshot
from .models import Unit, Client, PropertyApplication
from .models import OccupancySnapshot

def home(request):
    return redirect("login")


def get_dashboard_redirect(user):
    if user.is_superuser:
        return redirect("/admin/")
    
    elif user.groups.filter(name="Managers").exists():
        return redirect("manager_dashboard")
    
    if user.groups.filter(name="Client").exists():
        return redirect("property_list")

    return redirect("dashboard")

# LOGIN-PANNEL.
def login_view(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(
            request,
            username=username,\
            password=password
        )
        if user is not None:
            login(request, user)
            return get_dashboard_redirect(user)
        return render(
            request,
            "accounts/login.html",
            {
                "error": "Invalid username or password"
            }
        )
    return render(request, "accounts/login.html")


@login_required
def application_trend_live(request):
    now = timezone.now()
    last_24_hours = now - timedelta(hours=24)

    qs = (
        PropertyApplication.objects
        .filter(applied_at__gte=last_24_hours)
        .extra({'hour': "strftime('%%H:00', applied_at)"})  # SQLite
        .values('hour')
        .annotate(count=Count('id'))
        .order_by('hour')
    )

    # Build full 24-hour timeline (fill missing hours with 0)
    hours = [(now - timedelta(hours=i)).strftime("%H:00") for i in range(23, -1, -1)]

    data_dict = {item['hour']: item['count'] for item in qs}

    labels = []
    values = []

    for h in hours:
        labels.append(h)
        values.append(data_dict.get(h, 0))  # fill missing with 0

    return JsonResponse({
        "labels": labels,
        "values": values
    })
# MANAGER DASHBOARD
@login_required
def manager_dashboard(request):


    if not request.user.groups.filter(name="Managers").exists():
        return redirect("login")
    
    record_occupancy_snapshot(request.user)

    properties = Property.objects.filter(manager=request.user)

    total_properties = properties.count()

    total_units = Unit.objects.filter(
        property__manager=request.user
    ).count()

    occupied_units = Unit.objects.filter(
        property__manager=request.user,
        status="OCCUPIED"
    ).count()

    vacant_units = Unit.objects.filter(
        property__manager=request.user,
        status="VACANT"
    ).count()

    property_units = (
        properties.values("name")
        .annotate(units=Count("units"))
    )

    recent_applications = (
        PropertyApplication.objects
        .filter(manager=request.user)
        .select_related("client", "property")
        .order_by("-applied_at")[:5]
    )

   

    occupancy_data = [
        {"status": "Occupied", "count": occupied_units},
        {"status": "Vacant", "count": vacant_units},
    ]

    context = {
    "total_properties": total_properties,
    "total_units": total_units,
    "occupied_units": occupied_units,
    "vacant_units": vacant_units,
    "manager_properties": properties,
    "property_units": json.dumps(
        list(property_units),
        cls=DjangoJSONEncoder,
    ),
    "recent_applications": recent_applications,
    "occupancy_data": json.dumps(
        occupancy_data,
        cls=DjangoJSONEncoder,
    ),
}

    return render(
        request,
        "manager/dashboard.html",
        context,
    )

# CLIENT DASHBOARD
@login_required
def client_dashboard(request):

    if not request.user.groups.filter(name="Client").exists():
        return redirect("login")

    client = Client.objects.filter(user=request.user).first()
    context = {"client": client}
    return render( request,"client/dashboard.html",context)


# PROPERTY LIST
@login_required
def property_list(request):

    properties = Property.objects.filter(is_available=True)
    return render(
        request,
        "property/property_list.html",
        {
            "properties": properties
        }
    )



@login_required
def property_detail(request, property_id):

    property = get_object_or_404(Property,id=property_id)
    gallery = property.images.all()
    gallery_urls = []

    if property.image:
        gallery_urls.append(property.image.url)
    gallery_urls.extend(photo.image.url for photo in gallery)

    context = {
        "property": property,
        "gallery": gallery,
        "gallery_urls": gallery_urls,
    }

    return render(
        request,
        "property/property_detail.html",
        context
    )


# ADD PROPERTY
@login_required
def add_property(request):

    if not (request.user.is_superuser or request.user.groups.filter(name="Managers").exists()):
        return redirect("login")

    if request.method == "POST":

        form = PropertyForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            property = form.save(commit=False)
            property.manager = request.user
            property.save()
            return redirect("manager_dashboard")

    else:
        form = PropertyForm()

    return render(
        request,
        "property/add_property.html",
        {
            "form": form
        }
    )



# CLIENT REGISTRATION
# CLIENT REGISTRATION
def register_client(request):

    if request.method == "POST":

        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            return render(
                request,
                "accounts/register.html",
                {
                    "error": "Passwords do not match"
                }
            )

        if User.objects.filter(username=username).exists():
            return render(
                request,
                "accounts/register.html",
                {
                    "error": "Username already exists"
                }
            )

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name,
        )

        # Create client profile
        Client.objects.create(
            user=user
        )

        # Add user to Client group
        client_group, created = Group.objects.get_or_create(
            name="Client"
        )

        user.groups.add(client_group)

        return redirect("login")

    return render(
        request,
        "accounts/register.html"
    )

@login_required
def apply_property(request, property_id):

    property = get_object_or_404(
    Property,
    id=property_id
)

    client, created = Client.objects.get_or_create(
    user=request.user
)

    if request.method == "POST":

        form = PropertyApplicationForm(request.POST)

        if form.is_valid():

            application = form.save(commit=False)
            application.client = client
            application.property = property
            application.manager = property.manager
            application.save()

            messages.success(
                request,
                "Your application has been submitted successfully."
            )

            return redirect(
                "property_detail",
                property_id=property.id
            )

    else:
        form = PropertyApplicationForm()

    return render(
        request,
        "property/apply_property.html",
        {
            "form": form,
            "property": property,
        }
    )



@login_required
def manager_applications(request):
    applications = PropertyApplication.objects.filter(
        manager=request.user
    ).order_by("-applied_at")
    return render(
        request,
        "manager/applications.html",
        {
            "applications": applications
        }
    )
    application_trend = (
    Application.objects
    .annotate(day=TruncDay('created_at'))
    .values('day')
    .annotate(count=Count('id'))
    .order_by('day')
)

    context['application_trend'] = list(application_trend)

@login_required
def edit_property(request, id):

    property = get_object_or_404(
        Property,
        id=id,
        manager=request.user
    )


    if request.method == "POST":

        form = PropertyForm(
            request.POST,
            request.FILES,
            instance=property
        )

        if form.is_valid():
            form.save()

            return redirect(
                "manager_properties"
            )


    else:

        form = PropertyForm(
            instance=property
        )


    return render(
        request,
        "manager/edit_property.html",
        {
            "form": form,
            "property": property
        }
    )

@login_required
def manager_properties(request):

    if not request.user.groups.filter(name="Managers").exists():
        return redirect("login")


    properties = Property.objects.filter(
        manager=request.user
    ).order_by("-created_at")


    context = {
        "properties": properties
    }


    return render(
        request,
        "manager/properties.html",
        context
    )
@login_required
def manager_properties(request):

    if not request.user.groups.filter(name="Managers").exists():
        return redirect("login")

    properties = Property.objects.filter(
        manager=request.user
    ).order_by("-created_at")

    context = {
        "properties": properties
    }

    return render(
        request,
        "manager/properties.html",
        context
    )
@login_required
def delete_property(request, id):

    property = get_object_or_404(
        Property,
        id=id,
        manager=request.user
    )


    if request.method == "POST":

        property.delete()

        return redirect(
            "manager_properties"
        )


    return render(
        request,
        "manager/delete_property.html",
        {
            "property": property
        }
    )
