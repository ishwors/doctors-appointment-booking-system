
import datetime
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from .forms import CustomPasswordChangeForm, CustomPasswordResetForm, CustomPasswordResetConfirmForm
from app.models import Booking, Doctor, Gender, Patient, Review, Specialization, Schedule, Timing, Invoice
from django.template.loader import render_to_string
from django.db.models import Q
from django.template.defaultfilters import date as format_date
from django.db.models import Avg, Count
from dateutil import parser
import requests as req
from datetime import date


from DAS import email_backend

class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'main/change-password.html'
    success_url = reverse_lazy('patient-dashboard')

class CustomDoctorPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'main/doctor-change-password.html'
    success_url = reverse_lazy('doctor-dashboard')

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'main/forgot-password.html'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'main/forgot-password.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Manually add the default and custom success messages to the context
        context['default_success_message'] = "Password reset email has been sent."
        return context

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomPasswordResetConfirmForm
    template_name = 'main/reset-password.html'
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'main/login.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Manually add the default and custom success messages to the context
        context['default_success_message'] = "Password reset complete. You can now log in with your new password."
        return context

def index(request):
    doctors = Doctor.objects.all().order_by('id')

    for doctor in doctors:
        doctor.aggregated_review = doctor.review_set.aggregate(average_rating=Avg('rating'), total_reviews=Count('rating'))
    
    context = { 
        'doctor': doctors
    }

    return render(request,'main/index.html',context)

@login_required(login_url="login")
def DOCTOR_DASHBOARD(request):
    if request.user.last_name == "Doctor":
        user = request.user
        doctor = user.doctor

        # Get today's date
        today = date.today()

        # Filter bookings for the doctor for today's date and upcoming dates
        history_bookings = Booking.objects.filter(doctor=doctor, date__lte=today, status__in=['Completed'])
        today_bookings = Booking.objects.filter(doctor=doctor, date=today, status__in=['Confirmed'])
        upcoming_bookings = Booking.objects.filter(doctor=doctor, date__gt=today, status__in=['Confirmed'])
        booking = Booking.objects.all().order_by('id')

        # Find Total Patients (unique patients associated with the doctor)
        total_patients = Patient.objects.filter(booking__doctor=doctor).distinct().count()

        # Find Today's Patient Count (unique patients with appointments today)
        today_patient_count = Patient.objects.filter(booking__doctor=doctor, booking__date=today).distinct().count()

        # Find Total Appointments (appointments associated with the doctor)
        total_appointments = Booking.objects.filter(doctor=doctor).count()

        context = {
            'booking': booking,
            'history_bookings': history_bookings,
            'today_bookings': today_bookings,
            'upcoming_bookings': upcoming_bookings,
            'total_patients': total_patients,
            'today_patient_count': today_patient_count,
            'total_appointments': total_appointments,
        }
        return render(request, 'main/doctor-dashboard.html', context)
    
    return redirect('login')

def LOGIN(request):

    # Get today's date
    today = date.today()
    booking = Booking.objects.filter(date__lt=today, status__in=['Confirmed'])

    for i in booking:
        i.status = 'Completed'
        i.save()

    return render(request,'main/login.html')

def LOGOUT(request):
    logout(request)
    return redirect('login')

def SEARCH(request):
    doctors = Doctor.objects.all().order_by('id')
    gender = Gender.objects.all().order_by('id')
    specialization = Specialization.objects.all().order_by('id')


    for doctor in doctors:
        doctor.aggregated_review = doctor.review_set.aggregate(average_rating=Avg('rating'), total_reviews=Count('rating'))

    context = { 
        'doctors':doctors,    
        'gender':gender,
        'specialization':specialization,
    }

    return render(request, 'main/search.html',context)

from django.db.models import Avg, Count

def filter_data(request):
    genders = request.GET.getlist('gender[]')
    specializations = request.GET.getlist('specialization[]')

    doctors = Doctor.objects.all()

    # Filter based on genders if genders are provided
    if genders:
        doctors = doctors.filter(gender__id__in=genders)
    
    # Filter based on specializations if specializations are provided
    if specializations:
        doctors = doctors.filter(specialization__id__in=specializations)

    aggregated_reviews = {}  # Dictionary to store aggregated reviews

    for doctor in doctors:
        aggregated_reviews[doctor.id] = doctor.review_set.aggregate(average_rating=Avg('rating'), total_reviews=Count('rating'))
        doctor.aggregated_review = aggregated_reviews[doctor.id]

    t = render_to_string('ajax/doctor-list.html', {'doctors': doctors})

    return JsonResponse({'data': t})


def index_search(request):
    q=request.GET['search']
    
    doctors = Doctor.objects.all().order_by('id')
    doctors = doctors.filter(Q(address__icontains=q) 
                       | Q(clinic_name__icontains=q) 
                       | Q(clinic_address__icontains=q) 
                       | Q(user__first_name__icontains=q) 
                       | Q(gender__title__icontains=q) 
                       | Q(specialization__title__icontains=q)) .order_by('id')
    
    for doctor in doctors:
        doctor.aggregated_review = doctor.review_set.aggregate(average_rating=Avg('rating'), total_reviews=Count('rating'))

    gender = Gender.objects.all().order_by('id')
    specialization = Specialization.objects.all().order_by('id')

    context = { 
        'doctors':doctors,    
        'gender':gender,
        'specialization':specialization,
    }

    return render(request, 'main/search.html',context)

def autocomplete(request):
    if 'term' in request.GET:
        user = User.objects.filter(last_name='Doctor')
        search_term = request.GET.get('term')

        users_by_first_name = user.filter(first_name__icontains=search_term)
        titles = [user.first_name for user in users_by_first_name]

        users_by_clinic_name = user.filter(doctor__clinic_name__icontains=search_term)
        titles += [user.doctor.clinic_name for user in users_by_clinic_name]

        users_by_clinic_address = user.filter(doctor__clinic_address__icontains=search_term)
        titles += [user.doctor.clinic_address for user in users_by_clinic_address]

        return JsonResponse(titles, safe=False)

    return render(request, 'main/search.html')

def DOCTOR_PROFILE(request, slug):
    doctors = Doctor.objects.get(slug=slug)
    id = doctors.id
    doctor = Doctor.objects.filter(slug = slug)
    
    if doctor.exists():
        doctor = doctor.first()
    else:
        return redirect(request,'error/404.html')

    patient_id = request.user.id

    review_filter = Review.objects.filter(doctor_id=id)

    aggregated_review = Review.objects.filter(doctor=doctor).aggregate(
        average_rating=Avg('rating'),
        total_reviews=Count('id')
    )

    # For Patient :
    user = User.objects.filter(last_name = 'Patient').order_by('id')

    # For Doctor Schedule
    schedule = Schedule.objects.filter(doctor_id = id)
    
    context = {
        'review': review_filter,
        'user' : user,
        'doctor' : doctor,
        'aggregated_review': aggregated_review,
        'schedule' : schedule,
    }

    if request.method == 'POST' and patient_id is not None:
        rating = request.POST.get('rating')
        review_text = request.POST.get('review_text')

        patient = request.user.patient
        patient_id = patient.id
   
        review = Review(
                rating=rating,
                review_text=review_text,
                patient_id=patient_id,
                doctor_id= id,
            )
         
        review.save()
        return redirect('doctor-profile', slug=doctor.slug)
    
    elif request.method == 'POST' and patient_id is None:
        return redirect('login')
        # Note : Please login to write review message needs to be displayed
        
    return render(request, 'main/doctor-profile.html', context)

def register(request):
    if request.method == "POST":
        fname = request.POST.get('fname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # check username
        if User.objects.filter(username=username).exists():
           messages.warning(request,'That username has already been taken!')
           return redirect('register')
        
        # check email
        if User.objects.filter(email=email).exists():
           messages.warning(request,'Email already exists!')
           return redirect('register')
        
        user = User(
            first_name = fname,
            last_name = "Patient",
            username = username,
            email = email,
        )

        user.set_password(password)
        user.save()

        return redirect('login')
    return render(request,'main/register.html')

def doctor_register(request):
    if request.method == "POST":
        fname = request.POST.get('fname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # check username
        if User.objects.filter(username=username).exists():
           messages.warning(request,'That username has already been taken!')
           return redirect('doctor-register')
        
        # check email
        if User.objects.filter(email=email).exists():
           messages.warning(request,'Email already exists!')
           return redirect('doctor-register')
        
        user = User(
            first_name = fname,
            last_name = "Doctor",
            username = username,
            email = email,
        )

        user.set_password(password)
        user.save()

        return redirect('login')
    return render(request,'main/doctor-register.html')

def DO_LOGIN(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = email_backend.EmailBackEnd.authenticate(request,
                                     username=email,
                                     password=password)
        if user!=None:
           if user.last_name == "Patient":
                login(request,user)
                return redirect('patient-dashboard')
           elif user.last_name == "Doctor":
                login(request,user)
                return redirect('doctor-dashboard')
        else:
           messages.error(request,'Invalid Email or Password !')
           return redirect('login')

@login_required(login_url="login")
def PATIENT_DASHBOARD(request):
    if request.user.last_name == "Patient":
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        patient_id = user.patient.id
        doctors = Doctor.objects.all().order_by('id')

        for doctor in doctors:
            doctor.aggregated_review = doctor.review_set.aggregate(average_rating=Avg('rating'), total_reviews=Count('rating'))

        booking_filter = Booking.objects.filter(patient_id=patient_id, status__in=['Confirmed']).order_by('-date')
        invoice_filter = Invoice.objects.filter(patient_id=patient_id).order_by('-issued_on')
        history_filter = Booking.objects.filter(patient_id=patient_id, status__in=['Completed']).order_by('-date')
        
        context = {
            'booking': booking_filter,
            'invoice': invoice_filter,
            'history': history_filter,
            'doctor': doctors,
        }
        return render(request,'main/patient-dashboard.html', context)
    return redirect('login')


def PROFILE_SETTINGS(request):
    # Important code to access user and patient table
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    patient = user.patient
    dob = user.patient.dob.strftime('%Y-%m-%d') if user.patient.dob else ''

    if request.method == "POST":
        image = request.FILES.get('image')
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        email = request.POST.get('email')
        blood = request.POST.get('blood')
        gender= request.POST.get('gender')
        dob = request.POST.get('dob')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip = request.POST.get('zip')
        country = request.POST.get('country')

        # To update existing records
        if image is None:
            patient.profile_pic = patient.profile_pic
        else:
            patient.profile_pic = image

        patient.dob = dob
        patient.blood_group = blood
        patient.gender_id = gender
        patient.mobile = mobile
        patient.address = address
        patient.city = city
        patient.state = state
        patient.zip_code = zip
        patient.country = country
        
        patient.save()

        user.first_name = fname
        user.username = username
        user.email = email
            
        user.save()

        context = {
            'user': user,
            'dob': dob,
        }

        return render(request, 'main/profile-settings.html', context)
    
    context = {
        'dob': dob,
    }

    return render(request, 'main/profile-settings.html', context)


def DOCTOR_PROFILE_SETTINGS(request):
# Important code to access user and patient table
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    doctor = user.doctor
    dob = user.doctor.dob.strftime('%Y-%m-%d') if user.doctor.dob else ''

    if request.method == "POST":
        image = request.FILES.get('image')
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        email = request.POST.get('email')
        specialization = request.POST.get('specialization')
        dob= request.POST.get('dob')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        bio = request.POST.get('bio')
        pricing = request.POST.get('pricing')
        degree = request.POST.get('degree')
        designation = request.POST.get('designation')
        experience = request.POST.get('experience')
        gender= request.POST.get('gender')
        clinic_name = request.POST.get('clinic_name')
        clinic_address = request.POST.get('clinic_address')

    # To update existing records
        if image is None:
            doctor.profile_pic = doctor.profile_pic
        else:
            doctor.profile_pic = image
        
        doctor.dob = dob
        doctor.mobile = mobile
        doctor.address = address
        doctor.specialization_id = specialization
        doctor.degree = degree
        doctor.pricing = pricing
        doctor.bio = bio
        doctor.designation =  designation 
        doctor.experience =  experience
        doctor.gender_id = gender
        doctor.clinic_name = clinic_name
        doctor.clinic_address = clinic_address
        doctor.save()

        user.first_name = fname
        user.username = username
        user.email = email
            
        user.save()

        context = {
            'user': user,
            'dob': dob,
        }

        return render(request,'main/doctor-profile-settings.html',context)
    
    context = {
    'dob': dob,
    }

    return render(request,'main/doctor-profile-settings.html',context)

def REVIEWS(request):
    doctorid = request.user.id
    doctor = Doctor.objects.get(user_id=doctorid)
    id = doctor.id

    review_filter = Review.objects.filter(doctor_id=id)

    # For Patient :
    patient = Patient.objects.all().order_by('id')

    context = {
        'review': review_filter,
        'patient' : patient,
    }

    return render(request, 'main/reviews.html', context)

@login_required(login_url="login") 
def complete_booking(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
        if booking.status == "Confirmed":
            # Change the booking status to "Completed"
            booking.status = "Completed"
            booking.save()
    except Booking.DoesNotExist:
        pass

    # Redirect back to the doctor's dashboard or any relevant page
    return redirect('doctor-dashboard')  # Replace 'doctor-dashboard' with your actual URL name

@login_required(login_url="login")  # Requires the user to be logged in to access the view
def INVOICE_VIEW(request, invoice_id):
    user = request.user
    patient = user.patient

    if patient:
        invoice = get_object_or_404(Invoice, id=invoice_id)

        # Check if the current user is the owner of the invoice
        if patient == invoice.patient:
            context = {
                'invoice': invoice
            }

            return render(request, 'main/invoice-view.html', context)

    # Redirect to the index page for unauthorized users or patients without access
    return redirect('login')

def SCHEDULE_TIMINGS(request):
    doctorid = request.user.id
    doctor = Doctor.objects.get(user_id=doctorid)
    id = doctor.id

    schedule = Schedule.objects.filter(doctor_id = id)   

    context = {
        'schedule' : schedule,
    }

    return render(request, 'main/schedule-timings.html', context)

def DOCTOR_SCHEDULE(request):
    doctorid = request.user.id
    doctor = Doctor.objects.get(user_id=doctorid)
    id = doctor.id

    if request.method == "POST":
        day = request.POST.get('day')
        time = request.POST.getlist('time')

        # Fetch existing schedule for the doctor
        existing_schedule = Schedule.objects.filter(doctor_id=id)

        # Update the schedule for the provided day
        for schedule_entry in existing_schedule:
            if schedule_entry.day == day and str(schedule_entry.timing_id) not in time:
                # Unchecked schedule entry, delete it
                schedule_entry.delete()

        # Create or update the selected schedule entries
        for data in time:
            schedule_entry = existing_schedule.filter(day=day, timing_id=data).first()
            if schedule_entry:
                # Schedule entry exists, update the timing_id
                schedule_entry.timing_id = data
                schedule_entry.save()
            else:
                # Create a new schedule entry
                schedule = Schedule(day=day, doctor_id=id, timing_id=data)
                schedule.save()

    return redirect('schedule-timings')

@login_required(login_url="login")
def BOOKING(request,slug):
    if request.user.last_name == "Patient":

        doctors = Doctor.objects.get(slug=slug)
        id = doctors.id  # This id is doctor table's doctor id
        doctor = Doctor.objects.filter(slug = slug)
        
        patientid = request.user.id
        patient = Patient.objects.get(user_id = patientid)
        pat_id = patient.id

        if doctor.exists():
            doctor = doctor.first()
        else:
            return redirect(request,'error/404.html')
        
        doctor.aggregated_review = doctor.review_set.aggregate(average_rating=Avg('rating'), total_reviews=Count('rating'))

        # For Time
        if request.method == "POST": 
            date = request.POST.get('date')
            
            # Convert the date string to a datetime object
            date_obj = datetime.datetime.strptime(date, '%Y-%m-%d')

            # Get the day of the week as a string (e.g., Monday, Tuesday, etc.)
            day_of_week = date_obj.strftime('%A').lower()

            schedule = Schedule.objects.filter(doctor_id = id)
            value = schedule.filter(day = day_of_week) # value has all schedules of a perticuler day

            # Get the booked schedule IDs for the selected date
            booked_schedule_ids = Booking.objects.filter(date=date, doctor_id=id, patient_id=pat_id).values_list('schedule_id', flat=True)

            # Exclude the booked schedules from the value queryset
            filtered_value = value.exclude(id__in=booked_schedule_ids)


            context = {
            'value' : filtered_value,
            'date' : date,
            'doctor' : doctor,
            'schedule' : schedule,
            }

            # check Date
            if not value.exists() or not filtered_value.exists():
                messages.warning(request, 'No time-slots available for the selected date !')
                return render(request,'main/booking.html',context)

            return render(request,'main/booking.html',context)

        # For Date
        context = {
            'doctor' : doctor,
        }

        return render(request,'main/booking.html',context)
    return redirect('login')

def CHECKOUT(request,slug):
    if request.method == "POST":
        user = request.user.id
        patient = Patient.objects.get(user_id=user)
        patient_id = patient.id

        date = request.POST.get('date')
        time_id = request.POST.get('time')
        doctor = Doctor.objects.filter(slug = slug)

        if doctor.exists():
            doctor = doctor.first()
        else:
            return redirect(request,'error/404.html')
        
        # Convert the date string to a datetime object
        date_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
        formatted_date = format_date(date_obj, 'd M Y')

        # Getting time from time id
        time = Timing.objects.get(id = time_id)

        doctor.aggregated_review = doctor.review_set.aggregate(average_rating=Avg('rating'), total_reviews=Count('rating'))
        doctor_id = doctor.id

        # Get the day of the week as a string (e.g., Monday, Tuesday, etc.)
        day_of_week = date_obj.strftime('%A').lower()

        schedule = Schedule.objects.filter(doctor_id = doctor_id, timing = time_id, day = day_of_week).first()

        booking = Booking(
            patient_id = patient_id,
            doctor_id = doctor_id,
            timing_id = time_id,
            schedule_id = schedule.id,
            date = date,
            status = "Pending"
        )

        booking.save()
        
        context = {
            'date' : formatted_date,
            'time' : time,
            'doctor' : doctor,
            'patient' : patient,
            'schedule' : schedule,
        }

    return render(request,'main/checkout.html',context)

@login_required(login_url="login")
def CANCEL_BOOKING(request):
    if request.method == "POST":
        user = request.user
        patient = user.patient

        # Get the latest booking record for the current patient
        booking = Booking.objects.filter(patient=patient).latest('created_at')

        # Delete the booking record
        booking.delete()

    return redirect('search')  # Redirect to the search page or any other appropriate page

@login_required(login_url="login")
def EsewaCancel(request):
    user = request.user
    patient = user.patient

    # Get the latest booking record for the current patient
    booking = Booking.objects.filter(patient=patient).latest('created_at')

    # Delete the booking record
    booking.delete()

    return redirect('search')  # Redirect to the search page or any other appropriate page
    
def EsewaVerifyView(request):
    import xml.etree.ElementTree as ET
    oid = request.GET.get("oid")
    amt = request.GET.get("amt")
    refId = request.GET.get("refId")

    url ="https://uat.esewa.com.np/epay/transrec"
    d = {
        'amt': amt,
        'scd': 'EPAYTEST',
        'rid': refId,
        'pid': oid,
    }
    
    resp = req.post(url, d)
    root = ET.fromstring(resp.content)
    status = root[0].text.strip()


    user = request.user.id
    patient = Patient.objects.get(user_id=user)
    patient_id = patient.id
    
    schedule_id = oid
    booking = Booking.objects.filter(schedule_id = oid).first()
    doctor_id = booking.doctor_id
    timing_id = booking.timing_id
    date = booking.date

    doctor = Doctor.objects.get(id = doctor_id)
    timing = Timing.objects.get(id = timing_id)


    if status == "Success":
        booking.status = "Confirmed"
        booking.save()

        invoice = Invoice(
            patient_id = patient_id,
            doctor_id = doctor_id,
            booking_id = booking.id,
            amount = amt
        )
    
        invoice.save()

        context = {
            'doctor': doctor,
            'date': date,
            'time' : timing,
            'invoice' : invoice,
        }
        return render(request,'main/booking-success.html',context)
    else:
        return redirect("/esewa-request/?s_id="+schedule_id)


# def FORGOT_PASSWORD(request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             messages.error(request, 'User with this email does not exist.')
#             return render(request, 'main/forgot-password.html')

#         # Generate and send the reset password email
#         token = default_token_generator.make_token(user)
#         reset_url = f'http://http://127.0.0.1:8000/reset-password/{user.pk}/{token}/'
#         send_mail(
#             'Password Reset',
#             f'Click the link to reset your password: {reset_url}',
#             'maknees321@gmail.com',  # Replace with your sender email
#             [email],
#             fail_silently=False,
#         )

#         messages.success(request, 'Password reset email sent. Please check your email.')
#         return redirect('login')  # Redirect to login page after sending the email

#     return render(request,'main/forgot-password.html')


# def reset_password(request, uid, token):
#     try:
#         user = User.objects.get(pk=uid)
#     except User.DoesNotExist:
#         # Handle invalid user ID
#         return render(request, 'main/invalid_reset_link.html')

#     if default_token_generator.check_token(user, token):
#         # Show the reset password form
#         return auth_views.PasswordResetConfirmView.as_view(
#             template_name='main/reset_password.html',
#             success_url='/login/',
#         )(request, uidb64=uid, token=token)
#     else:
#         # Handle invalid token
#         return render(request, 'main/invalid_reset_link.html')

   







