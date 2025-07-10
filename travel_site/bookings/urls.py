from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    # Travel-related views
    path('travel/', views.TravelListView.as_view(), name='travel_list'),
    path('travel/<int:pk>/book/', views.BookView.as_view(), name='travel_book'),

    # Bookings
    path('my-bookings/', views.MyBookingsView.as_view(), name='my_bookings'),
    path('booking/<int:pk>/cancel/', views.CancelBookingView.as_view(), name='cancel_booking'),

    # User authentication & profile
    path('register/', views.register, name='register'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile_update'),
]
