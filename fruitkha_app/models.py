from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

userchoices = (
    (1, "ADMIN"),
    (2, "EMPLOYEE"),
    (3, "CLIENT")
)
orderstatus = (
    (1, "ORDERED"),
    (2, "PENDING"),
    (3, "DELIVERED"),
    (4, "CANCELLED")
)

class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'username']

    # user_name = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=30, null=True, blank=True)
    phone_number = models.CharField(max_length=13, null=True, blank=True)
    email = models.EmailField(null=True, blank=True, unique=True)
    user_type = models.IntegerField(default=1, choices=userchoices)
    address = models.CharField(max_length=255, null=True, blank=True)
    pincode = models.CharField(max_length=6, null=True, blank=True)
    def __str__(self):
        return self.username



class PRODUCT(models.Model):
    item_name = models.CharField(max_length=30, null=True, blank=True)
    item_code = models.CharField(max_length=6, null=True, blank=True, unique=True)
    category = models.CharField(max_length=15, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to="images/")
    price = models.DecimalField(decimal_places=2, max_digits=7, null=True, blank=True)

class CART(models.Model):
    item = models.ForeignKey(PRODUCT, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(decimal_places=2, max_digits=7, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)


class ORDER(models.Model):
    item = models.ForeignKey(PRODUCT, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(null=True,blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    total = models.DecimalField(decimal_places=2, max_digits=7, null=True, blank=True)
    status = models.IntegerField(default=1, choices=orderstatus)

class DELIVERY_ADDRESS(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=25, null=True, blank=True)
    phone_number = models.CharField(max_length=13, null=True, blank=True)
    email = models.EmailField(null=True, blank=True, unique=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    pincode = models.CharField(max_length=6, null=True, blank=True)

class OFFER(models.Model):
    item = models.ForeignKey(PRODUCT, on_delete=models.CASCADE)
    description = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to="images/")
    validity = models.DateTimeField(blank=True, null=True)
    percentage = models.IntegerField(null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    offer_price = models.DecimalField(decimal_places=2, max_digits=7, null=True, blank=True)

class CONTACT(models.Model):
    name = models.CharField(max_length=30, null=True, blank=True)
    phone_number = models.CharField(max_length=13, null=True, blank=True)
    email = models.EmailField(null=True, blank=True, unique=True)
    subject = models.CharField(max_length=6, null=True, blank=True)
    message = models.CharField(max_length=555, null=True, blank=True)
    enquiry_time = models.DateTimeField(blank=True, null=True)


class NOTIFICATION(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    table_no = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.text

