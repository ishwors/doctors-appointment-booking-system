# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    blood_group = models.CharField(max_length=3,null=True)
    mobile = models.CharField(max_length=15 ,null=True)
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
    mobile = models.CharField(max_length=15, null=True)
    dob = models.DateField(null=True)
    bio = models.TextField(blank=True)
    clinic_name = models.CharField(max_length=50, null=True)
    clinic_address = models.CharField(max_length=150, null=True)
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
        if instance.patient.profile_pic == "":
            instance.patient.profile_pic = "default.png"
        instance.patient.save()

    elif instance.last_name == "Doctor":
        if instance.doctor.profile_pic == "":
            instance.doctor.profile_pic = "default.png"
        instance.doctor.save()




