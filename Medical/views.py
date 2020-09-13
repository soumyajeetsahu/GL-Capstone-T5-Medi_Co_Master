from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from Medical.static.forms.appointment import AppointmentForm


def home_view(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            app_date = request.POST.get("appointment_date", None)
            name = request.POST.get("Name", None)

            responseData = {
                'date': app_date,
                'name': name
            }
            return JsonResponse(responseData, safe=False)
    else:
        form = AppointmentForm()

    return render(request, 'medical/index.html', {'form': form})


def doctor_view(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AppointmentForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            message = messages.success("This is my success message")
            return JsonResponse(form)

        # if a GET (or any other method) we'll create a blank form
    else:
        form = AppointmentForm()

    return render(request, 'medical/doctors.html', {'form': form})


def lab_tests(request):
    return render(request, 'medical/labtests.html')
