from django.db import models
from django.core.validators import RegexValidator
from django.conf import settings
from django.urls import reverse


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


class LabTests(models.Model):
    title = models.CharField(max_length=255)
    price = models.FloatField()
    details = models.CharField(max_length=500)
    slug = models.SlugField()
    discount_price = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("test_detail", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("remove-from-cart", kwargs={
            'slug': self.slug
        })


class OrderItem(models.Model):
    item = models.ForeignKey(LabTests, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        # if self.coupon:
        #     total -= self.coupon.amount
        return total
