# travel_site/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from bookings import views as booking_views
from bookings.views import (
    TravelListView, BookView, MyBookingsView,
    CancelBookingView, ProfileUpdateView, logout_view
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # 👇 Custom logout must come BEFORE auth.urls
    path('accounts/logout/', logout_view, name='logout'),

    # Auth routes
    path('accounts/', include('django.contrib.auth.urls')),

    # 👇 Login as home page
    path('', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),

    # Travel routes
    path('travel/', TravelListView.as_view(), name='travel_list'),
    path('travel/<int:pk>/book/', BookView.as_view(), name='travel_book'),
    path('booking/<int:pk>/cancel/', CancelBookingView.as_view(), name='cancel_booking'),

    # Profile routes
    path('profile/', booking_views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile_update'),

    # Bookings app urls
    path('bookings/', include(('bookings.urls', 'bookings'), namespace='bookings')),
]
