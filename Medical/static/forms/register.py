from django import forms
from Medical.models import UserRegistration, UserLogin


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = UserRegistration
        fields = ['FirstName', 'LastName', 'Password', 'Email', 'PhoneNumber', 'Gender', 'ConfirmPassword']
        widgets = {
            'FirstName': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "First Name *",
                                                'data-msg': "Please enter your First name"}),
            'LastName': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Last Name *",
                                               'data-msg': "Please enter your Last name"}),
            'Email': forms.TextInput(attrs={'class ': 'form-control', 'placeholder': "Your Email *"}),
            'Password': forms.TextInput(
                attrs={'class ': 'form-control', 'placeholder': "password *", 'type': "password"}),
            'ConfirmPassword': forms.TextInput(
                attrs={'class ': 'form-control', 'placeholder': "Confirm Password *", 'type': "password"}),
            'PhoneNumber': forms.TextInput(attrs={'class ': 'form-control', 'placeholder': "Your Phone *",
                                                  'minlength': '10', 'maxlength': '10'}),
            'Gender': forms.RadioSelect()
            # 'doctor': forms.Select(attrs={'class ': 'form-control', 'placeholder': "Select Doctor"}),
            # 'appointment_date': forms.TextInput(
            #     attrs={'class ': 'form-control datepicker', 'placeholder': "Appointment Date", 'type': "datetime"}),

        }
        # Name = forms.CharField(max_length=100)
        # email = forms.EmailField()
        # phnumber = forms.IntegerField()
        # department = forms.CharField(max_length=255, choices= Department.choices())


class LoginForm(forms.ModelForm):
    class Meta:
        model = UserLogin
        fields = ['username', 'password']
        widgets = {
            'password': forms.TextInput(
                attrs={'class ': 'form-control', 'placeholder': "password", 'type': "password"}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Email address",
                                               'data-msg': "Please enter your First name"}),
        }
