from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200)
    warehouse = models.CharField(max_length=20, null=False, blank=True)

    def __str__(self):
        return self.name + ", " + self.warehouse


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=100)
    available = models.BooleanField(default=True)
    description = models.TextField(max_length=100, null=True, blank=True)
    interested = models.PositiveIntegerField(default=0) #Added Positive Integer Field

    def __str__(self):
        return self.name

    def refill(self):
        st = self.stock + 100  # adds 100 to the current value of stock
        t = Product.objects.get(name=self.name)
        t.stock = st
        t.save()


class Client(User):
    PROVINCE_CHOICES = [
        ('AB', 'Alberta'),
        ('MB', 'Manitoba'),
        ('ON', 'Ontario'),
        ('QC', 'Quebec'), ]
    company = models.CharField(max_length=50, null=False, blank=True)
    shipping_address = models.CharField(max_length=300, null=True, blank=True)
    city = models.CharField(max_length=20, default='windsor')
    province = models.CharField(max_length=2, choices=PROVINCE_CHOICES, default='ON')
    interested_in = models.ManyToManyField(Category)

    def __str__(self):
        return self.first_name


class Order(models.Model):
    VALID_CHOICES = [
        (0, 'Order Cancelled'),
        (1, 'Order Placed'),
        (2, 'Order Shipped'),
        (3, 'Order Delivered')
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    num_units = models.PositiveIntegerField(default=1)
    order_status = models.IntegerField(choices=VALID_CHOICES, default=1)
    status_date = models.DateField(default=timezone.now)

    def __str__(self):
        cost = self.product.price * self.num_units
        return 'Order# ' + str(self.id) + ': For ' + ' ' + self.product.name + " (#) by " + str(self.client) + ' and total amount is ' + str(cost)

    # def __str__(self):

    # return str(cost);
