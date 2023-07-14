"""DAS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from .import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('doctor-dashboard/',views.DOCTOR_DASHBOARD, name='doctor-dashboard'),
    path('appointments/',views.APPOINTMENTS, name='appointments'),
    path('login/',views.LOGIN, name='login'),
    path('logout/', views.LOGOUT, name='logout'),
    path('register/',views.register, name='register'),
    path('doctor-register/',views.doctor_register, name='doctor-register'),
    path('doLogin', views.DO_LOGIN, name='doLogin'),
    path('patient-dashboard/', views.PATIENT_DASHBOARD, name='patient-dashboard'),
    path('profile-settings/', views.PROFILE_SETTINGS, name='profile-settings'),
    path('change-password/', views.CustomPasswordChangeView.as_view(), name='change-password'),
    path('doctor-change-password/', views.CustomDoctorPasswordChangeView.as_view(), name='doctor-change-password'),
    path('search/', views.SEARCH, name='search'),
    path('booking/', views.BOOKING, name='booking'),
    path('doctor-profile/<slug:slug>', views.DOCTOR_PROFILE, name='doctor-profile'),
    path('doctor-profile-settings', views.DOCTOR_PROFILE_SETTINGS, name='doctor-profile-settings'),
    path('filter-data', views.filter_data, name='filter_data'),
    path('index-search', views.index_search, name='index-search'),
    path('autocomplete', views.autocomplete, name='autocomplete'),
    path('reviews', views.REVIEWS, name='reviews'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
