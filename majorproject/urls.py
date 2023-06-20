"""
URL configuration for majorproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from majorproject import views

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('doctor-dashboard', views.doctor_dashboard, name='doctor-dashboard'),
    path('appointments', views.appointments, name='appointments'),
    path('schedule-timings', views.schedule_timings, name='schedule-timings'),
    path('patient-profile', views.patient_profile, name='patient-profile'),
    path('login', views.login, name='login'),
    path('my-patients', views.my_patients, name='my-patients'),
    path('invoices', views.invoices, name='invoices'),
    path('doctor-profile-settings', views.doctor_profile_settings, name='doctor-profile-settings'),
    path('reviews', views.reviews, name='reviews'),
    path('profile-settings', views.profile_settings, name='profile-settings'),
    path('doctor-register', views.doctor_register, name='doctor-register'),
    path('search', views.search, name='search'),
    path('doctor-profile', views.doctor_profile, name='doctor-profile'),
    path('booking', views.booking, name='booking'),
    path('checkout', views.checkout, name='checkout'),
    path('booking-success', views.booking_success, name='booking-success'),
    path('patient-dashboard', views.patient_dashboard, name='patient-dashboard'),
    path('favourites', views.favourites, name='favourites'),
    path('change-password', views.change_password, name='change-password'),
    path('calendar', views.calendar, name='calendar'),
    path('invoice-view', views.invoice_view, name='invoice-view'),
    path('register', views.register, name='register'),
    path('forgot-password', views.forgot_password, name='forgot-password'),
]


