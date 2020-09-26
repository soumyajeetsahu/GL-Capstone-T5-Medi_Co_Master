from django.contrib import admin

# Register your models here.
from Medical.models import Appointment, Labs, Departments, Doctors

admin.site.register(Appointment)
admin.site.register(Labs)
admin.site.register(Departments)
admin.site.register(Doctors)
