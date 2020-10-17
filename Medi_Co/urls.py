"""Medi_Co URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from Medical import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),

    path('', views.home_view, name='home'),
    path('home', views.home_view, name='home'),
    path('lab_tests', views.LabLists.as_view(), name='lab_tests'),
    path('test_detail/<slug>/', views.LabDetailView.as_view(), name='test_detail'),
    path('add-to-cart/<slug>/', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', views.remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', views.remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('order-summary/', views.OrderSummaryView.as_view(), name='order-summary'),
    path('appointment', views.appointment, name='appointment'),
    path('load_doctors', views.load_doctors, name='load_doctors'),
    path('process_qrcode', views.process_qrcode, name='process_qrcode'),
    path('process_qrcode_lab', views.process_qrcode_lab, name='process_qrcode_lab'),
    path('checkout', views.CheckOutView.as_view(), name='checkout'),
    path('check_out', views.Check_OutView.as_view(), name='check_out'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
