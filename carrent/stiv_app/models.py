# cars/models.py
from django.db import models

class Car(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)  # Sedan, SUV, etc.
    description = models.TextField()
    image = models.ImageField(upload_to='cars/')  # save uploaded images in MEDIA_ROOT/cars/
    available = models.BooleanField(default=True)
    price_per_day = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name
# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Car(models.Model):
    name = models.CharField(max_length=100)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True) 
    # other fields...

    def __str__(self):
        return self.name

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, default='pending')  # pending, confirmed, completed

    def __str__(self):
        return f"{self.user.username} - {self.car.name} ({self.status})"
        