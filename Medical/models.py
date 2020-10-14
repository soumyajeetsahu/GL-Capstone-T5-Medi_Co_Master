from django.db import models
from django.core.validators import RegexValidator

from Medical.enum import Department


class Labs(models.Model):
    image = models.ImageField()
    name = models.CharField(max_length=255)
    price = models.IntegerField()


class Departments(models.Model):
    dept_id = models.IntegerField(primary_key=True)
    dept_name = models.CharField(max_length=100)
    dept_desc = models.CharField(max_length=1000)

    def __str__(self):
        return "%s" % self.dept_name


class Doctors(models.Model):
    doctor_id = models.IntegerField(primary_key=True)
    doctor_name = models.CharField(max_length=60)
    experience = models.CharField(max_length=50)
    image = models.ImageField(upload_to='Medical/static/assets/img/doctors/')
    department = models.ForeignKey(Departments, on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % self.doctor_name


class Appointment(models.Model):
    Name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 10 digits allowed.")
    phnumber = models.CharField(validators=[phone_regex], max_length=10)
    department = models.ForeignKey(Departments, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    payment = models.CharField(max_length=100, blank=True, default='')

    def __str__(self):
        return "%s" % self.Name


class UserRegistration(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    FirstName = models.CharField(max_length=50)
    LastName = models.CharField(max_length=50)
    Password = models.CharField(max_length=16)
    ConfirmPassword = models.CharField(max_length=16)
    Email = models.EmailField()
    PhoneNumber = models.CharField(max_length=10)
    Gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=None)


class UserLogin(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=16)
