from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, RegexValidator
from datetime import date


class Instrument(models.Model):
    instrument_id = models.AutoField(primary_key=True)
    model = models.CharField(max_length=100, null=False)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    rating = models.FloatField(blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='instruments', null=True)

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    instrument = models.CharField(max_length=50, null=False) # poate fi chitara, bas, tobe, etc.
    type = models.TextField(blank=True, null=True) # poate fi acustica, electrica, etc.

class Stock(models.Model):
    stock_id = models.AutoField(primary_key=True)
    instrument = models.OneToOneField(Instrument, on_delete=models.CASCADE, related_name='stock')
    quantity = models.PositiveIntegerField(null=False, default=0)
    warehouse_location = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Intrumentul {self.instrument.name} are {self.quantity} bucati in stoc in {self.warehouse_location} "

class Supplier(models.Model):
    supplier_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    contact = models.CharField(max_length=50, blank=True, null=True)  
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Furnizorul {self.name} are contactul {self.contact} si adresa {self.address} "

class Order(models.Model):
    STATUS_CHOICES = [
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]

    order_id = models.AutoField(primary_key=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='orders')
    instrument = models.ManyToManyField(Instrument,related_name='orders')
    order_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PROCESSING')

    def __str__(self):
        return f"Comanda de la furnizorul {self.supplier} pentru instrumentul {self.instrument} care are {self.quantity} bucati si este in starea de {self.status} "


class OrderItem(models.Model):
    order_item_id = models.AutoField(primary_key=True)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, related_name='order_items')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField(null=False)

    def __str__(self):
        return f"S-au comandat {self.quantity} bucati din instrumentul {self.instrument} care apartine comenzii {self.order} "
    

class ProductImage(models.Model):
    image_id = models.AutoField(primary_key=True)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField(null=False)
    alter_img = models.URLField(null=False)

    def __str__(self):
        return f"Imagine pentru instrumentul {self.instrument.name}"


class Discount(models.Model):
    discount_id = models.AutoField(primary_key=True)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, related_name='discounts')
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=False)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=False)

    def __str__(self):
        return f"Discount {self.discount_percentage}% pentru {self.instrument.name}"
