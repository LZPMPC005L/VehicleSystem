"""
URL configuration for Vehicle_System project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from vehicle.views import register_owner,register_vehicle, license_plate_recognition_record


urlpatterns = [
    path("admin/", admin.site.urls),
    path("register_owner/", register_owner, name="register_owner"),
    path("register_vehicle/", register_vehicle, name="register_vehicle"),
    path("recognition_record/", license_plate_recognition_record, name="license_plate_recognition_record"),
]
