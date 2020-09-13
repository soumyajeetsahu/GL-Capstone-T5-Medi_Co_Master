from django.contrib import admin

# Register your models here.
from Medical.models import Appointment, Labs

admin.site.register(Appointment)
admin.site.register(Labs)
