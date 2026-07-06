from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import models

from .models import Property
from .forms import PropertyForm


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
        form = PropertyForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('add_property')

    else:
        form = PropertyForm()

    total_properties = Property.objects.count()

    total_units = Property.objects.aggregate(
        total=models.Sum('total_units')
    )['total'] or 0

    occupied_units = Property.objects.aggregate(
        total=models.Sum('occupied_units')
    )['total'] or 0

    vacant_units = total_units - occupied_units

    context = {
        'form': form,
        'total_properties': total_properties,
        'total_units': total_units,
        'occupied_units': occupied_units,
        'vacant_units': vacant_units,
    }

    return render(
        request,
        "property/add_property.html",
        context
    )