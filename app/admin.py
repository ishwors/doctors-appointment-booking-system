from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Gender)
admin.site.register(Review)
admin.site.register(Slot)
admin.site.register(Timing)