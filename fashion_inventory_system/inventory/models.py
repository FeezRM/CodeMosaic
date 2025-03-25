from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator

class User(AbstractUser):
    pass

class Product(models.Model):
    product_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.CharField(max_length=30)
    size = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    material = models.CharField(max_length=50)
    weight = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Weight (kg)")
    stock_quantity = models.IntegerField()
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f"{self.name} - {self.brand}"
    
