from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from Medical.models import Doctors, UserRegistration, Appointment
from Medical.static.forms.appointment import AppointmentForm
from Medical.static.forms.register import RegistrationForm, LoginForm
import boto3
import pyqrcode
import png
from pyqrcode import QRCode


def home_view(request):
    if request.session.has_key('User_Name'):
        UserName = request.session['User_Name']
    else:
        UserName = None

    form = AppointmentForm()
    doctors = Doctors.objects.order_by('doctor_name')
    return render(request, 'medical/index.html', {'form': form, 'doctors': doctors, 'username': UserName})


def lab_tests(request):
    if request.session.has_key('User_Name'):
        UserName = request.session['User_Name']
    else:
        UserName = None
    return render(request, 'medical/labtests.html', {'username': UserName})


def login_get(request):
    form = LoginForm()
    return render(request, 'medical/Login.html', {'form': form})


def registration(request):
    form = RegistrationForm()
    return render(request, 'medical/registration.html', {'form': form})


def registration_post(request):
    success_note = "Get"
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # form = RegistrationForm()
            success_note = "Registration Successful. Please Login"
            return render(request, 'medical/registration.html', {'success_note': success_note})
        else:
            form = RegistrationForm()
            success_note = "Error loading"
    else:
        form = RegistrationForm()
    return render(request, 'medical/registration.html', {'form': form, 'success_note': success_note})


def login_post(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        # user = auth.authenticate(username=username, password=password)
        print(username)
        user = UserRegistration.objects.filter(Email=username)
        UserName = None
        user_count = (user.count())
        for us in user:
            UserName = us.FirstName
        if user_count != 0:
            request.session['User_Name'] = username
            request.session.set_expiry(300)
            form = AppointmentForm()
            doctors = Doctors.objects.order_by('doctor_name')
            return render(request, 'medical/index.html', {'form': form, 'doctors': doctors, 'username': UserName})
        else:
            error_note = "Username/Password Invalid."
            form = LoginForm()
            return render(request, 'medical/Login.html', {'form': form, 'error_note': error_note})
    else:
        form = LoginForm()
    return render(request, 'medical/Login.html', {'form': form})


def load_doctors(request):
    dept_id = request.GET.get('Departments')
    print(dept_id)
    doctors = Doctors.objects.filter(department_id=dept_id).order_by('doctor_name')
    # return JsonResponse(doctors, safe=False)
    return render(request, 'medical/load_doctors.html', {'doctors': doctors})


def logout(request):
    try:
        if request.session.has_key('User_Name'):
            del request.session['User_Name']
            request.session.flush()
    except KeyError:
        pass
    form = AppointmentForm()
    doctors = Doctors.objects.order_by('doctor_name')
    return render(request, 'medical/index.html', {'form': form, 'doctors': doctors})


def appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            app_date = request.POST.get("appointment_date", None)
            name = request.POST.get("Name", None)
            responseData = {
                'date': app_date,
                'name': name
            }
            return JsonResponse(responseData, safe=False)
    else:
        if request.session.has_key('User_Name'):
            UserName = request.session['User_Name']
        form = AppointmentForm()
        doctors = Doctors.objects.order_by('doctor_name')
        return render(request, 'medical/BookAppointment.html', {'form': form, 'doctors': doctors, 'username': UserName})


def process_qrcode(request):
    appointments = Appointment.objects.filter(payment='')
    bucket = 'medico-lamda-bucket'
    for app in appointments:
        s = app.Name + " " + app.email + " " + app.appointment_date.strftime('%m/%d/%Y')
        url = pyqrcode.create(s)
        filename = app.phnumber+".svg"
        url.svg(filename, scale=8)
        fs = FileSystemStorage()
        file_url = fs.url(filename)
        print(file_url)
        s3_client = boto3.client('s3')
        response = s3_client.upload_file(filename, bucket, filename)
        print(response)
    if request.session.has_key('User_Name'):
        UserName = request.session['User_Name']
    else:
        UserName = None
    return render(request, 'medical/labtests.html', {'username': UserName})