from django.contrib import admin

# Register your models here.
from Medical.models import Appointment, LabTests, Departments, Doctors, UserRegistration, Order, OrderItem

admin.site.register(Appointment)
admin.site.register(LabTests)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Departments)
admin.site.register(Doctors)
admin.site.register(UserRegistration)
