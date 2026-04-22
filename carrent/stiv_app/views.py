# stiv_app/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Car, Booking  # Booking import fixed
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

# ========================
# Home / Index
# ========================
def home(request):
    # Get the first car to pass to the homepage
    car = Car.objects.first()  # safely gets a car from DB (or None if empty)

    return render(request, 'index.html', {
        'user': request.user,
        'car': car
    })

# ========================
# Pages
# ========================
def about(request):
    return render(request, 'about.html')


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        subject = f"New Contact Us Message from {name}"
        message_body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        recipient_list = ['support@carrent.com']  # Replace with your support email

        try:
            send_mail(subject, message_body, email, recipient_list)
            messages.success(request, "Message sent successfully! We'll get back to you soon.")
        except Exception as e:
            messages.error(request, f"Error sending message: {e}")

        return redirect('contacts')  # Stay on the same page

    return render(request, 'contacts.html')


def product(request):
    # Only show available cars
    cars = Car.objects.filter(available=True)
    return render(request, 'product.html', {'cars': cars})

# ========================
# Car Renting
# ========================
@login_required(login_url='login')  # Redirect to login if not authenticated
def rent_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if request.method == "POST":
        # RentalRequest does not exist in models.py, so we just show a message
        messages.warning(request, "Rental requests are not saved yet.")
        return redirect('product')  # or 'products'

    return render(request, "rent.html", {"car": car})    

# ========================
# Authentication
# ========================
def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Redirect to next page if present, else to home
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            else:
                return redirect('home')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')


def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if user exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Account created successfully! Please login.")
        return redirect('login')

    return render(request, 'register.html')


def logout_user(request):
    logout(request)
    return redirect('home')

# ========================
# Book Car
# ========================
@login_required
def book_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if request.method == "POST":
        # Fixed fields to match Booking model
        new_booking = Booking.objects.create(
            user=request.user,
            car=car,
            start_date=request.POST['pickup_date'],  # pickup_date → start_date
            end_date=request.POST['return_date'],    # return_date → end_date
            status='pending'
        )
        # Redirect to booking success page
        return redirect('booking_success', booking_id=new_booking.id)

    return render(request, "rent.html", {"car": car})   

# ========================
# Booking Success
# ========================
def booking_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'booking_success.html', {'booking': booking})

# ========================
# Payment
# ========================
def payment(request):
    """Handle payment processing"""
    return render(request, 'payment.html')