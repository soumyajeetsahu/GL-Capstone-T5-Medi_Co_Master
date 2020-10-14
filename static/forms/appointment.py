from django import forms
from Medical.models import Appointment


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['Name', 'email', 'phnumber', 'department', 'doctor', 'appointment_date']
        labels = {'email': 'Email-Id', 'phnumber': 'Phone Number', 'appointment_date': 'Appointment Date'}
        widgets = {
            'Name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Your Full Name",
                                           'data-msg': "Please enter your full name"}),
            'email': forms.TextInput(attrs={'class ': 'form-control', 'placeholder': "Your Email"}),
            'phnumber': forms.TextInput(attrs={'class ': 'form-control', 'placeholder': "Your Phone", 'type': "tel"}),
            'department': forms.Select(attrs={'class ': 'form-control', 'placeholder': "Select Department"}),
            'doctor': forms.Select(attrs={'class ': 'form-control', 'placeholder': "Select Doctor"}),
            'appointment_date': forms.TextInput(
                attrs={'class ': 'form-control datepicker', 'placeholder': "Appointment Date", 'type': "datetime"}),

        }
        # Name = forms.CharField(max_length=100)
        # email = forms.EmailField()
        # phnumber = forms.IntegerField()
        # department = forms.CharField(max_length=255, choices= Department.choices())
