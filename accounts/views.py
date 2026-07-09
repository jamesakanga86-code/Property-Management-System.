from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Property, Unit, Client, Lease
from .forms import PropertyForm, PropertyApplicationForm
from django.shortcuts import get_object_or_404
from .models import PropertyApplication
from django.shortcuts import redirect
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PropertyApplicationForm
from .models import Property, PropertyApplication
from django.contrib import messages

def home(request):
    return redirect("login")


def get_dashboard_redirect(user):
    if user.is_superuser:
        return redirect("/admin/")

    if user.groups.filter(name="Manager").exists():
        return redirect("manager_dashboard")

    if user.groups.filter(name="Client").exists():
        return redirect("property_list")

    if user.groups.filter(name="Staff").exists():
        return redirect("dashboard")

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

# MAIN DASHBOARD
@login_required
def dashboard(request):

    lease = Lease.objects.filter(client__user=request.user,is_active=True).first()
    context = {"lease": lease}
    return render(request,"dashboard/home.html",context)

# MANAGER DASHBOARD
@login_required
def manager_dashboard(request):

    if not request.user.groups.filter(name="Manager").exists():
        return redirect("login")

    properties = Property.objects.filter(manager=request.user)
    applications = PropertyApplication.objects.filter(manager=request.user).order_by("-applied_at")
    pending_count = applications.filter(status="PENDING").count()

    context = {
        "properties": properties,
        "applications": applications[:5],
        "pending_count": pending_count,
    }

    return render(request, "manager/dashboard.html", context)

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


@login_required
def property_detail(request, property_id):

    property = get_object_or_404(
        Property,
        id=property_id
    )

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

    if not (request.user.is_superuser or request.user.groups.filter(name="Manager").exists()):
        return redirect("login")

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

@login_required
def apply_property(request, property_id):

    property = get_object_or_404(
        Property,
        id=property_id
    )

    client = request.user.client

    if request.method == "POST":

        form = PropertyApplicationForm(request.POST)

        if form.is_valid():

            application = form.save(commit=False)

            application.client = client
            application.property = property
            application.manager = property.manager

            application.save()
            messages.success(request,"Your application has been submitted successfully.")

            return redirect("property_detail", property.id)

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
def apply_property(request, property_id):

    property = get_object_or_404(
        Property,
        id=property_id
    )

    client = request.user.client

    if request.method == "POST":

        form = PropertyApplicationForm(request.POST)

        if form.is_valid():

            application = form.save(commit=False)

            application.client = client
            application.property = property
            application.manager = property.manager

            application.save()
            messages.success( request,
                               "Your application has been submitted successfully."
)
            return redirect("property_detail", property_id=property.id)

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