
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .forms import CustomPasswordChangeForm
from app.models import Doctor, Gender, Patient, Review, Specialization
from django.template.loader import render_to_string
from django.db.models import Q

from DAS import email_backend

class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'main/change-password.html'
    success_url = reverse_lazy('patient-dashboard')

class CustomDoctorPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'main/doctor-change-password.html'
    success_url = reverse_lazy('doctor-dashboard')


def index(request):
    return render(request,'main/index.html')

@login_required(login_url="login")
def DOCTOR_DASHBOARD(request):
    if request.user.last_name == "Doctor":
        return render(request,'main/doctor-dashboard.html')
    
    return render(request,'main/login.html')
    

def APPOINTMENTS(request):
    return render(request,'main/appointments.html')

def LOGIN(request):
    return render(request,'main/login.html')

def LOGOUT(request):
    logout(request)
    return redirect('login')

def SEARCH(request):
    user = User.objects.filter(last_name = 'Doctor').order_by('id')
    gender = Gender.objects.all().order_by('id')
    specialization = Specialization.objects.all().order_by('id')

    context = { 
        'user':user,    
        'gender':gender,
        'specialization':specialization,
    }

    return render(request, 'main/search.html',context)

def index_search(request):
    q=request.GET['search']
    
    user = User.objects.filter(last_name = 'Doctor')
    user = user.filter(Q(doctor__address__icontains=q) 
                       | Q(doctor__clinic_name__icontains=q) 
                       | Q(doctor__clinic_address__icontains=q) 
                       | Q(first_name__icontains=q) 
                       | Q(doctor__gender__title__icontains=q) 
                       | Q(doctor__specialization__title__icontains=q)) .order_by('id')

    gender = Gender.objects.all().order_by('id')
    specialization = Specialization.objects.all().order_by('id')

    context = { 
        'user':user,    
        'gender':gender,
        'specialization':specialization,
    }

    return render(request, 'main/search.html',context)

def autocomplete(request):
    if 'term' in request.GET:
        user = User.objects.filter(last_name = 'Doctor')
        search_term = request.GET.get('term')

        qs = user.filter(Q(first_name__icontains=search_term )) 
        titles = list()

        titles = [f"{user.first_name}" for user in qs]
        return JsonResponse(titles, safe=False)

    return render(request,'main/search.html')

def DOCTOR_PROFILE(request,slug):
    doctors = Doctor.objects.get(slug=slug)
    id = doctors.id  # This id is doctor table's doctor id
    doctor = Doctor.objects.filter(slug = slug)

    if doctor.exists():
        doctor = doctor.first()
    else:
        return redirect(request,'error/404.html')
    
    patient_id = request.user.id

    review_filter = Review.objects.filter(doctor_id=id)

    # For Patient :
    user = User.objects.filter(last_name = 'Patient').order_by('id')

    context = {
        'review': review_filter,
        'user' : user,
        'doctor' : doctor,
    }
    
    if request.method == 'POST' and patient_id is not None:
        rating = request.POST.get('rating')
        review_text = request.POST.get('review_text')

        patient_id = request.user.id
   
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

        # user_id = request.user.id
        # user = User.objects.get(id=user_id)
        # patient = user.patient
        # patient.id = user_id

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
           return redirect('register')
        
        # check email
        if User.objects.filter(email=email).exists():
           messages.warning(request,'Email already exists!')
           return redirect('register')
        
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
           messages.error(request,'Email and Password Are Invalid !')
           return redirect('login')

@login_required(login_url="login")
def PATIENT_DASHBOARD(request):
    if request.user.last_name == "Patient":
        return render(request,'main/patient-dashboard.html')
    
    return render(request,'main/login.html')

def PROFILE_SETTINGS(request):
    if request.method == "POST":
        image = request.FILES.get('image')
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        email = request.POST.get('email')
        blood = request.POST.get('blood')
        dob= request.POST.get('dob')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip = request.POST.get('zip')
        country = request.POST.get('country')

    # Important code to access user and patient table
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        patient = user.patient

    # To update existing records
        if image is None:
            patient.profile_pic = patient.profile_pic
        else:
            patient.profile_pic = image

        patient.dob = dob
        patient.blood_group = blood
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

        return render(request,'main/profile-settings.html')
    return render(request,'main/profile-settings.html')

def DOCTOR_PROFILE_SETTINGS(request):
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

    # Important code to access user and patient table
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        doctor = user.doctor
        
    # To update existing records
        if image is None:
            doctor.profile_pic = doctor.profile_pic
        else:
            doctor.profile_pic = image
        
        doctor.dob = dob
        doctor.mobile = mobile
        doctor.address = address
        doctor.specialization = specialization
        doctor.degree = degree
        doctor.pricing = pricing
        doctor.bio = bio
        doctor.designation =  designation 
        doctor.experience =  experience
        doctor.gender = gender
        doctor.clinic_name = clinic_name
        doctor.clinic_address = clinic_address
        doctor.save()

        user.first_name = fname
        user.username = username
        user.email = email
            
        user.save()

        return render(request,'main/doctor-profile-settings.html')
    return render(request,'main/doctor-profile-settings.html')

def BOOKING(request):
    return render(request,'main/booking.html')

# Filter Data
def filter_data(request):
    genders = request.GET.getlist('gender[]')
    specializations = request.GET.getlist('specialization[]')
    user = User.objects.filter(last_name='Doctor')

    # Filter based on genders if genders are provided
    if genders:
        user = user.filter(doctor__gender__id__in=genders)
    
    # Filter based on specializations if specializations are provided
    if specializations:
        user = user.filter(doctor__specialization__id__in=specializations)

    # Order the queryset by ID
    user = user.order_by('id')

    t = render_to_string('ajax/doctor-list.html', {'user': user})

    return JsonResponse({'data': t})

def REVIEWS(request):
    doctorid = request.user.id
    doctor = Doctor.objects.get(user_id=doctorid)
    id = doctor.id

    review_filter = Review.objects.filter(doctor_id=id)

    # For Patient :
    patient = User.objects.filter(last_name = 'Patient').order_by('id')

    context = {
        'review': review_filter,
        'patient' : patient,
    }

    return render(request, 'main/reviews.html', context)
