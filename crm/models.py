from django.db import models
from django.core.validators import RegexValidator
from decimal import Decimal

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} <{self.email}>"

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} (${self.price})"

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    products = models.ManyToManyField(Product, related_name='orders')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    order_date = models.DateTimeField(auto_now_add=True)

    def calculate_total(self):
        total = Decimal('0.00')
        for p in self.products.all():
            total += p.price
        return total

    def save(self, *args, **kwargs):
        # If instance already exists and products set later, total will be recalculated in mutation
        if self.pk and self.products.exists():
            self.total_amount = self.calculate_total()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.pk} by {self.customer.name} - {self.total_amount}"
