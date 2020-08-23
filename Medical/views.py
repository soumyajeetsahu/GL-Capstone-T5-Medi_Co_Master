from django.shortcuts import render


# Create your views here.
def home_view(request):
    return render(request, 'medical/index.html')


def doctor_view(request):
    return render(request, 'medical/doctors.html')
