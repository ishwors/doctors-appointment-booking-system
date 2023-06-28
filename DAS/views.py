
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from DAS import email_backend
# from app.models import Patient

def index(request):
    return render(request,'main/index.html')

def DOCTOR_DASHBOARD(request):
    return render(request,'main/doctor-dashboard.html')

def APPOINTMENTS(request):
    return render(request,'main/appointments.html')

def LOGIN(request):
    return render(request,'main/login.html')

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

def PATIENT_DASHBOARD(request):
    return render(request,'main/patient-dashboard.html')


# Patient
@login_required(login_url="/main/login/")
def PROFILE_SETTINGS(request):
    if request.method == "POST":
        image = request.POST.get('image')
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


# Doctor
@login_required(login_url="/main/login/")
def DOCTOR_PROFILE_SETTINGS(request):
    if request.method == "POST":
        image = request.POST.get('image')
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
