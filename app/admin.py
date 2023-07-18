from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Gender)
admin.site.register(Specialization)
admin.site.register(Review)
admin.site.register(Timing)
admin.site.register(Booking)