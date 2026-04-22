# stiv_app/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Car, Booking
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail


# ========================
# Home / Index
# ========================
@login_required
def home(request):
    car = Car.objects.first()

    return render(request, 'index.html', {
        'user': request.user,
        'car': car
    })


# ========================
# Pages
# ========================
@login_required
def about(request):
    return render(request, 'about.html')


@login_required
def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        subject = f"New Contact Us Message from {name}"
        message_body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        recipient_list = ['support@carrent.com']

        try:
            send_mail(subject, message_body, email, recipient_list)
            messages.success(request, "Message sent successfully! We'll get back to you soon.")
        except Exception as e:
            messages.error(request, f"Error sending message: {e}")

        return redirect('contacts')

    return render(request, 'contacts.html')


@login_required
def product(request):
    cars = Car.objects.filter(available=True)
    return render(request, 'product.html', {'cars': cars})


# ========================
# Car Renting
# ========================
@login_required
def rent_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if request.method == "POST":
        messages.warning(request, "Rental requests are not saved yet.")
        return redirect('product')

    return render(request, "rent.html", {"car": car})


# ========================
# Authentication
# ========================
def login_user(request):
    # Prevent logged-in users from seeing login page
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if user exists
        if not User.objects.filter(username=username).exists():
            messages.error(request, "Account not found")
            return redirect('login')

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            else:
                return redirect('home')
        else:
            messages.error(request, "Incorrect password")

    return render(request, 'login.html')


def register(request):
    # Prevent logged-in users from accessing register page
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Auto login after register
        login(request, user)

        messages.success(request, "Account created successfully!")

        return redirect('home')

    return render(request, 'register.html')


def logout_user(request):
    logout(request)
    return redirect('login')


# ========================
# Book Car
# ========================
@login_required
def book_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if request.method == "POST":
        new_booking = Booking.objects.create(
            user=request.user,
            car=car,
            start_date=request.POST['pickup_date'],
            end_date=request.POST['return_date'],
            status='pending'
        )
        return redirect('booking_success', booking_id=new_booking.id)

    return render(request, "rent.html", {"car": car})


# ========================
# Booking Success
# ========================
@login_required
def booking_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'booking_success.html', {'booking': booking})


# ========================
# Payment
# ========================
@login_required
def payment(request):
    return render(request, 'payment.html')