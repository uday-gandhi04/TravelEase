from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import TravelOption, Booking, UserProfile

User = get_user_model()

class BookingFlowTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Create user + profile
        self.user = User.objects.create_user(username='testuser', password='pass')
        UserProfile.objects.create(user=self.user)
        # Create one travel option
        self.travel = TravelOption.objects.create(
            travel_id="T001",
            type='flight',
            source='CityA',
            destination='CityB',
            departure_datetime='2030-01-01T10:00:00Z',
            price=100,
            available_seats=5
        )

    def test_profile_update_view(self):
        self.client.login(username='testuser', password='pass')
        # GET profile edit form
        resp = self.client.get(reverse('profile_update'))
        self.assertEqual(resp.status_code, 200)
        # POST updated name/email
        resp = self.client.post(reverse('profile_update'), {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
        })
        # Should redirect back to profile_update
        self.assertRedirects(resp, reverse('profile_update'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'John')
        self.assertEqual(self.user.email, 'john@example.com')

    def test_booking_and_cancel(self):
        self.client.login(username='testuser', password='pass')

        # Book 2 seats
        resp = self.client.post(
            reverse('bookings:travel_book', args=[self.travel.pk]),
            {'seats': 2}
        )
        # Booking success should redirect to My Bookings
        self.assertRedirects(resp, reverse('bookings:my_bookings'))

        booking = Booking.objects.get(user=self.user)
        self.assertEqual(booking.seats, 2)
        self.assertEqual(booking.status, 'confirmed')

        # Cancel the booking
        resp = self.client.post(
            reverse('bookings:cancel_booking', args=[booking.pk])
        )
        # Cancel should redirect back to My Bookings
        self.assertRedirects(resp, reverse('bookings:my_bookings'))

        booking.refresh_from_db()
        self.assertEqual(booking.status, 'cancelled')

        # Seats should be returned
        self.travel.refresh_from_db()
        self.assertEqual(self.travel.available_seats, 5)
