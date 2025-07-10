from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import TravelOption, Booking

User = get_user_model()

class BookingFlowTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.travel = TravelOption.objects.create(
            type='Flight', source='A', destination='B',
            datetime='2030-01-01T10:00:00Z', price=100, available_seats=5
        )

    def test_profile_update_view(self):
        self.client.login(username='testuser', password='pass')
        resp = self.client.get(reverse('profile_update'))
        self.assertEqual(resp.status_code, 200)
        resp = self.client.post(reverse('profile_update'), {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com'
        })
        self.assertRedirects(resp, reverse('profile_update'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'John')

    def test_booking_and_cancel(self):
        self.client.login(username='testuser', password='pass')
        # book 2 seats
        resp = self.client.post(reverse('travel_book', args=[self.travel.pk]), {'seats': 2})
        self.assertRedirects(resp, reverse('my_bookings'))
        booking = Booking.objects.get(user=self.user)
        self.assertEqual(booking.seats, 2)
        # cancel booking
        resp = self.client.post(reverse('cancel_booking', args=[booking.pk]))
        self.assertRedirects(resp, reverse('my_bookings'))
        booking.refresh_from_db()
        self.assertEqual(booking.status, 'cancelled')
        self.travel.refresh_from_db()
        self.assertEqual(self.travel.available_seats, 5)  # seats returned
