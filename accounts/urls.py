from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-property/', views.add_property, name='add_property'),
    path('register/', views.register_client, name='register'),
    path('client/dashboard/',views.client_dashboard,name='client_dashboard'),
    path('properties/', views.property_list, name='property_list'), 
    path('properties/',views.property_list,name='property_list'),
    path("properties/",views.property_list,name="property_list"),  
    path("property/<int:property_id>/",views.property_detail,name="property_detail"),  
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)