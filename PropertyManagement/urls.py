from django.contrib import admin
from django.urls import path, include
from accounts import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("", include("accounts.urls")),
    path("properties/", views.manager_properties, name="manager_properties"),
    path('manager/properties/', views.manager_properties, name='manager_properties'),
    path('manager/property/delete/<int:id>/', views.delete_property, name='delete_property'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)