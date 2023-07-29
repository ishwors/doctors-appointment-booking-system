# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.urls import reverse

# Gender
class Gender(models.Model):
    title = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.title


# Specialization
class Specialization(models.Model):
    title = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.title

# Create your models here.
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add your custom fields here
    profile_pic = models.ImageField(default='default.png', null=True, blank=True) #stored in a separate media folder
    dob = models.DateField(null=True)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, null=True)
    blood_group = models.CharField(max_length=3,null=True)
    mobile = models.CharField(max_length=15 ,null=True, unique=True)
    address = models.CharField(max_length=150 ,null=True)
    city = models.CharField(max_length=50 ,null=True)
    state = models.CharField(max_length=50 ,null=True)
    zip_code = models.CharField(max_length=10 ,null=True)
    country = models.CharField(max_length=100 ,null=True)

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add your custom fields here 
    profile_pic = models.ImageField(default='default.png', null=True, blank=True) #stored in a separate media folder
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, null=True)
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE, null=True)
    mobile = models.CharField(max_length=15, null=True, unique=True)
    dob = models.DateField(null=True)
    bio = models.TextField(blank=True)
    clinic_name = models.CharField(max_length=50, null=True)
    clinic_address = models.CharField(max_length=150, null=True)
    address = models.CharField(max_length=150, null=True)
    pricing = models.IntegerField(null=True)
    degree = models.CharField(max_length=10, null=True)
    experience = models.CharField(max_length=5, null=True)
    designation = models.CharField(max_length=30, null=True)
    slug = models.SlugField(default='', max_length=500, null=True, blank=True)

    def get_profile_url(self):
        return reverse("doctor-profile", kwargs={'slug': self.slug})
    
    def get_booking_url(self):
        return reverse("booking", kwargs={'slug': self.slug})
    
    def get_checkout_url(self):
        return reverse("checkout", kwargs={'slug': self.slug})
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.last_name == "Patient":
            Patient.objects.create(user=instance)

        elif instance.last_name == "Doctor":
            Doctor.objects.create(user=instance)
        
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.last_name == "Patient":
        if instance.patient.profile_pic == "":
            instance.patient.profile_pic = "default.png"
        instance.patient.save()

    elif instance.last_name == "Doctor":
        if instance.doctor.profile_pic == "":
            instance.doctor.profile_pic = "default.png"
        instance.doctor.save()

# Slug
def create_slug(instance, new_slug=None):
    slug = slugify(instance.user.first_name)
    if new_slug is not None:
        slug = new_slug
    qs = Doctor.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, Doctor)


# Review 
class Review(models.Model):
    rating = models.IntegerField()
    review_text = models.TextField(max_length=150)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE , null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE , null=True)

# Timing
class Timing(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

# Schedule
class Schedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    timing = models.ForeignKey(Timing, on_delete=models.CASCADE)
    day = models.CharField(max_length=15, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Booking
class Booking(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE , null=True)
    timing = models.ForeignKey(Timing, on_delete=models.CASCADE , null=True)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE , null=True)
    date = models.DateField(null=True)
    status = models.CharField(max_length=15, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

class Invoice(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE , null=True)
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='invoice', null=True, blank=True)
    amount = models.FloatField(null=True)
    issued_on = models.DateField(auto_now_add=True)
    payment_method = models.CharField(max_length=15, null=True, default='eSewa')
    


