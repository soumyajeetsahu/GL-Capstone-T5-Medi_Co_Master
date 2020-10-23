from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.models import User
from allauth.account.views import SignupView, LoginView
from Medical.models import Doctors, UserRegistration, Appointment, OrderItem, Order
from Medical.static.forms.appointment import AppointmentForm
from Medical.static.forms.register import RegistrationForm, LoginForm
import boto3
import pyqrcode
import png
import os
from pyqrcode import QRCode
from .models import LabTests
from django.views.generic import ListView, DetailView, View
from django.db.models import Case, Value, When


def home_view(request):
    form = AppointmentForm()
    doctors = Doctors.objects.order_by('doctor_name')
    return render(request, 'medical/index.html', {'form': form, 'doctors': doctors})


def load_doctors(request):
    dept_id = request.GET.get('Departments')
    #print(dept_id)
    doctors = Doctors.objects.filter(department_id=dept_id).order_by('doctor_name')
    # return JsonResponse(doctors, safe=False)
    return render(request, 'medical/load_doctors.html', {'doctors': doctors})


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
        form = AppointmentForm()
        doctors = Doctors.objects.order_by('doctor_name')
        return render(request, 'medical/BookAppointment.html', {'form': form, 'doctors': doctors})


def process_qrcode(request):
    appointments = Appointment.objects.filter(payment='')
    bucket = 'medico-lamda-bucket'
    for app in appointments:
        s = app.Name + " " + app.email + " " + app.appointment_date.strftime('%m/%d/%Y')
        url = pyqrcode.create(s)
        filename = "AppointmentQrcode_" + str(app.id) + ".png"
        url.png(filename, scale=8)
        fs = FileSystemStorage()
        file_url = fs.url(filename)
        s3_client = boto3.client('s3')
        response = s3_client.upload_file(filename, bucket, filename)
        if os.path.exists(file_url):
            os.remove(file_url)
        else:
        # FileSystemStorage.delete(file_url)
    return render(request, 'medical/request_processing.html')


def process_qrcode_lab(request):
    userdata = User.objects.get(username=request.user)
    # order_qs = Order.objects.filter(user=request.user, ordered=False)
    # Order.objects.filter(user=request.user).update(ordered=True)
    bucket = 'medico-lamda-bucket'
    s = userdata.email
    url = pyqrcode.create(s)
    filename = "Qrcode_" + str(userdata.id) + ".png"
    url.png(filename, scale=8)
    fs = FileSystemStorage()
    file_url = fs.url(filename)
    s3_client = boto3.client('s3')
    response = s3_client.upload_file(filename, bucket, filename)
    if os.path.exists(file_url):
        os.remove(file_url)
    else:
    # FileSystemStorage.delete(file_url)
    return render(request, 'medical/request_processing.html')


class LabLists(ListView):
    model = LabTests
    template_name = "medical/labtests.html"


class LabDetailView(DetailView):
    model = LabTests
    template_name = "medical/lab_details.html"


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(LabTests, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("order-summary")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(LabTests, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("test_detail", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("test_detail", slug=slug)


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'medical/order-summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(LabTests, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("test_detail", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("test_detail", slug=slug)


class CheckOutView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'medical/checkout.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")


class Check_OutView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            # order = Order.objects.get(user=self.request.user, ordered=False)
            # context = {
            #     'object': order
            # }
            return render(self.request, 'medical/check_out.html')
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")
