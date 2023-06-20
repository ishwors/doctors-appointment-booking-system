from django.shortcuts import render

def index(request):
    return render(request, 'main/index.html')

def doctor_dashboard(request):
    return render(request, 'main/doctor-dashboard.html')

def appointments(request):
    return render(request, 'main/appointments.html')

def schedule_timings(request):
    return render(request, 'main/schedule-timings.html')

def patient_profile(request):
    return render(request, 'main/patient-profile.html')

def login(request):
    return render(request, 'main/login.html')

def my_patients(request):
    return render(request, 'main/my-patients.html')

def invoices(request):
    return render(request, 'main/invoices.html')

def profile_settings(request):
    return render(request, 'main/profile-settings.html')

def doctor_profile_settings(request):
    return render(request, 'main/doctor-profile-settings.html')

def reviews(request):
    return render(request, 'main/reviews.html')

def doctor_register(request):
    return render(request, 'main/doctor-register.html')

def search(request):
    return render(request, 'main/search.html')

def doctor_profile(request):
    return render(request, 'main/doctor-profile.html')

def booking(request):
    return render(request, 'main/booking.html')

def checkout(request):
    return render(request, 'main/checkout.html')

def booking_success(request):
    return render(request, 'main/booking-success.html')

def patient_dashboard(request):
    return render(request, 'main/patient-dashboard.html')

def favourites(request):
    return render(request, 'main/favourites.html')

def change_password(request):
    return render(request, 'main/change-password.html')

def calendar(request):
    return render(request, 'main/calendar.html')

def invoice_view(request):
    return render(request, 'main/invoice-view.html')

def register(request):
    return render(request, 'main/register.html')

def forgot_password(request):
    return render(request, 'main/forgot-password.html')