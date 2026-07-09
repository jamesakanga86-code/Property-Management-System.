from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Property, Unit, Client, Lease
from .forms import PropertyForm


# HOME
def home(request):
    return redirect("login")
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
            if user.is_superuser:
                return redirect("/admin/")
            elif user.groups.filter(name="Manager").exists():
                return redirect("dashboard")
            elif user.groups.filter(name="Staff").exists():
                return redirect("dashboard")
            elif user.groups.filter(name="Client").exists():
                return redirect("property_list")
            else:
                return redirect("dashboard")
        return render(
            request,
            "accounts/login.html",
            {
                "error": "Invalid username or password"
            }
        )
    return render(request, "accounts/login.html")

# MAIN DASHBOARD
@login_required
def dashboard(request):

    lease = Lease.objects.filter(client__user=request.user,is_active=True).first()
    context = {"lease": lease}
    return render(request,"dashboard/home.html",context)

# MANAGER DASHBOARD
@login_required
def manager_dashboard(request):
    return HttpResponse("Manager Dashboard")

# STAFF DASHBOARD
@login_required
def staff_dashboard(request):
    return HttpResponse("Staff Dashboard")

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

# ADD PROPERTY
@login_required
def add_property(request):

    if request.method == "POST":

        form = PropertyForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            property = form.save(commit=False)
            property.save()

            return redirect("add_property")

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

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name,
        )

        Client.objects.create(user=user)

        client_group, created = Group.objects.get_or_create(name="Client")

        user.groups.add(client_group)

        return redirect("login")

    return render(
        request,
        "accounts/register.html"
    )