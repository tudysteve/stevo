from django.contrib import admin
from .models import Car  # <-- import the model

# Register the Car model so it appears in the admin
admin.site.register(Car)
# Register your models here.
