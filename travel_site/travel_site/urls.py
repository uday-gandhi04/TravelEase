# travel_site/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from bookings import views as booking_views
from bookings.views import (
    TravelListView, BookView, MyBookingsView,
    CancelBookingView, ProfileUpdateView, logout_view
)

# travel_site/urls.py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/logout/', logout_view, name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),

    # Profile
    path('profile/', booking_views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile_update'),

    # Use ONLY the namespaced bookings URLs below:
    path('bookings/', include(('bookings.urls', 'bookings'), namespace='bookings')),
]
