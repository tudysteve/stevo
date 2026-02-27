# stiv-app/urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Home page
    path('', views.home, name='home'),

    # Pages
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
    path('product/', views.product, name='product'),

    # Car renting
    path('rent/<int:car_id>/', views.rent_car, name='rent_car'),
    

    # Authentication
    path('login/', views.login_user, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),


    path('book/<int:car_id>/', views.book_car, name='book_car'),
    path('booking/success/<int:booking_id>/', views.booking_success, name='booking_success'),
    
    ]