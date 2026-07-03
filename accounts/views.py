from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


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
                return redirect('manager_dashboard')

            elif user.groups.filter(name='Staff').exists():
                return redirect('staff_dashboard')

            else:
                return render(
                    request,
                    "accounts/login.html",
                    {"error": "No role has been assigned to your account."}
                )

        else:
            return render(
                request,
                "accounts/login.html",
                {"error": "Invalid username or password"}
            )

    return render(request, "accounts/login.html")


@login_required
def manager_dashboard(request):
    return HttpResponse("Welcome Manager!")


@login_required
def staff_dashboard(request):
    return HttpResponse("Welcome Staff!")