# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add your custom fields here
    profile_pic = models.ImageField(upload_to="media/patient",null=True) #stored in a separate media folder
    dob = models.DateField(null=True)
    blood_group = models.CharField(max_length=3,null=True)
    mobile = models.CharField(max_length=15 ,null=True)
    address = models.CharField(max_length=150 ,null=True)
    city = models.CharField(max_length=50 ,null=True)
    state = models.CharField(max_length=50 ,null=True)
    zip_code = models.CharField(max_length=10 ,null=True)
    country = models.CharField(max_length=100 ,null=True)

class Doctor(models.Model):
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Add your custom fields here 
    profile_pic = models.ImageField(default='default.png', null=True, blank=True)
    gender = models.CharField(choices=GENDER, max_length=10, null=True)
    mobile = models.CharField(max_length=15, null=True)
    dob = models.DateField(null=True)
    bio = models.TextField(blank=True)
    clinic_name = models.CharField(max_length=50, null=True)
    clinic_address = models.CharField(max_length=150, null=True)
    specialization = models.CharField(max_length=150 , null=True)
    address = models.CharField(max_length=150, null=True)
    pricing = models.IntegerField(null=True)
    degree = models.CharField(max_length=10, null=True)
    experience = models.CharField(max_length=5, null=True)
    designation = models.CharField(max_length=30, null=True)

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
        instance.patient.save()

    elif instance.last_name == "Doctor":
        instance.doctor.save()




