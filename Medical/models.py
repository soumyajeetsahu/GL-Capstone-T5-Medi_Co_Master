from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
from Medical.enum import Department


class Appointment(models.Model):
    Name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 10 digits allowed.")
    phnumber = models.CharField(validators=[phone_regex], max_length=10)
    department = models.CharField(max_length=255, choices=Department.choices(),default=0)
    appointment_date = models.DateField()
    doctor = models.CharField(max_length=255)
