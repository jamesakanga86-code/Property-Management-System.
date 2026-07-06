from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import models
from .models import Property
from .forms import PropertyForm
from django.contrib.auth.models import User, Group
from .forms import ClientRegistrationForm
from .models import Client
from .models import Client, Property, Unit
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Lease
from .models import Property

@login_required
def dashboard(request):

    try:
        lease = Lease.objects.get(client__user=request.user, is_active=True)
    except Lease.DoesNotExist:
        lease = None

    context = {
        "lease": lease
    }

    return render(request, "dashboard/home.html", context)
# -------------------------
# HOME (ROOT URL)
# -------------------------
def home(request):
    return redirect('login')


# -------------------------
# DASHBOARD
# -------------------------
@login_required
def dashboard(request):
    return render(request, "dashboard/home.html")


# -------------------------
# LOGIN VIEW
# -------------------------
def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            if user.is_superuser:
                return redirect('/admin/')

            elif user.groups.filter(name='Manager').exists():
                return redirect('dashboard')

            elif user.groups.filter(name='Staff').exists():
                return redirect('dashboard')
            
            elif user.groups.filter(name='Client').exists():
                return redirect('client_dashboard')

            else:
                return redirect('dashboard')

        return render(
            request,
            "accounts/login.html",
            {"error": "Invalid username or password"}
        )

    return render(request, "accounts/login.html")


# -------------------------
# MANAGER DASHBOARD
# -------------------------
@login_required
def manager_dashboard(request):
    return HttpResponse("Manager Dashboard")


# -------------------------
# STAFF DASHBOARD
# -------------------------
@login_required
def staff_dashboard(request):
    return HttpResponse("Staff Dashboard")


# -------------------------
# ADD PROPERTY
# -------------------------
@login_required
def add_property(request):

    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)  # 👈 IMPORTANT

        if form.is_valid():
            form.save()
            return redirect('add_property')

    else:
        form = PropertyForm()

    return render(request, "property/add_property.html", {
        "form": form
    })

from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect

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
                {"error": "Passwords do not match"}
            )

        if User.objects.filter(username=username).exists():
            return render(
                request,
                "accounts/register.html",
                {"error": "Username already exists"}
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name
        )
        Client.objects.create(
    user=user
)

        client_group, created = Group.objects.get_or_create(
            name="Client"
        )

        user.groups.add(client_group)

        return redirect("login")

    return render(request, "accounts/register.html")
@login_required
def client_dashboard(request):

    if not request.user.groups.filter(name='Client').exists():
        return redirect('login')

    return render(
        request,
        'client/dashboard.html'
    
    )@login_required
def client_dashboard(request):

    # get client profile for logged-in user
    try:
        client = request.user.client
    except:
        client = None

    # BASIC STATS (from admin data)
    total_properties = Property.objects.count()
    total_units = Unit.objects.count()
    vacant_units = Unit.objects.filter(status='VACANT').count()
    occupied_units = Unit.objects.filter(status='OCCUPIED').count()

    # CLIENT-SPECIFIC DATA (this is key)
    client_units = Unit.objects.filter(
        status='OCCUPIED'
    )  # later we will link to lease

    context = {
        "client": client,
        "total_properties": total_properties,
        "total_units": total_units,
        "vacant_units": vacant_units,
        "occupied_units": occupied_units,
        "client_units": client_units,
    }

    return render(request, "client/dashboard.html", context)
    def property_list(request):
     properties = Property.objects.all().order_by('-created_at')

    return render(request, "property/property_list.html", {
        "properties": properties
    })
@login_required
def property_list(request):
    properties = Property.objects.all().order_by('-created_at')

    return render(request, "property/property_list.html", {
        "properties": properties
    })