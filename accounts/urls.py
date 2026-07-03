from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),

    path('manager/dashboard/', views.manager_dashboard, name='manager_dashboard'),

    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add-property/', views.add_property, name='add_property'),
]