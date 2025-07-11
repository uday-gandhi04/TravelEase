from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import TravelOption, Booking, UserProfile

User = get_user_model()

class BookingFlowTest(TestCase):
    def setUp(self):
        self.client = Client()
        # create user + profile
        self.user = User.objects.create_user(username='testuser', password='pass')
        UserProfile.objects.create(user=self.user)
        # two travel options
        self.travel1 = TravelOption.objects.create(
            travel_id="T001", type='flight', source='A', destination='B',
            departure_datetime='2030-01-01T10:00:00Z',
            price=100, available_seats=5
        )
        self.travel2 = TravelOption.objects.create(
            travel_id="T002", type='train', source='X', destination='Y',
            departure_datetime='2030-02-01T15:30:00Z',
            price=50, available_seats=2
        )

    def test_login_required_views(self):
        """Anonymous users should be redirected to login on protected pages."""
        for name, args in [
            ('bookings:travel_list', []),
            ('bookings:travel_book', [self.travel1.pk]),
            ('bookings:my_bookings', []),
        ]:
            url = reverse(name, args=args)
            resp = self.client.get(url)
            self.assertEqual(resp.status_code, 302)
            self.assertIn(reverse('login'), resp.url)

    def test_register_flow(self):
        """Register page loads and creates both User and UserProfile."""
        resp = self.client.get(reverse('bookings:register'))
        self.assertEqual(resp.status_code, 200)

        data = {
            'username': 'newuser',
            'password1': 'complexpass123',
            'password2': 'complexpass123',
            'email': 'new@example.com',
            'first_name': 'New',
            'last_name': 'User',
        }
        resp = self.client.post(reverse('bookings:register'), data)
        self.assertRedirects(resp, reverse('login'))

        new = User.objects.get(username='newuser')
        self.assertTrue(hasattr(new, 'userprofile'))

    def test_travel_list_and_filters(self):
        self.client.login(username='testuser', password='pass')
        url = reverse('bookings:travel_list')

        resp = self.client.get(url)
        self.assertContains(resp, 'A → B')
        self.assertContains(resp, 'X → Y')

        # filter by source
        resp = self.client.get(f"{url}?source=A")
        self.assertContains(resp, 'A → B')
        self.assertNotContains(resp, 'X → Y')

        # filter by type
        resp = self.client.get(f"{url}?type=train")
        self.assertContains(resp, 'X → Y')
        self.assertNotContains(resp, 'A → B')

    def test_booking_and_cancel(self):
        self.client.login(username='testuser', password='pass')

        # Attempt to overbook
        url_book2 = reverse('bookings:travel_book', args=[self.travel2.pk])
        resp = self.client.post(url_book2, {'seats': 5})
        self.assertContains(resp, "Not enough seats available.")

        # Successful booking
        url_book1 = reverse('bookings:travel_book', args=[self.travel1.pk])
        resp = self.client.post(url_book1, {'seats': 2})
        self.assertRedirects(resp, reverse('bookings:my_bookings'))

        booking = Booking.objects.get(user=self.user, travel=self.travel1)
        self.assertEqual(booking.seats, 2)
        self.travel1.refresh_from_db()
        self.assertEqual(self.travel1.available_seats, 3)

        # Cancel it
        url_cancel = reverse('bookings:cancel_booking', args=[booking.pk])
        resp = self.client.post(url_cancel)
        self.assertRedirects(resp, reverse('bookings:my_bookings'))

        booking.refresh_from_db()
        self.assertEqual(booking.status, 'cancelled')
        self.travel1.refresh_from_db()
        self.assertEqual(self.travel1.available_seats, 5)

    def test_profile_detail_and_update(self):
        self.client.login(username='testuser', password='pass')

        # Detail view
        resp = self.client.get(reverse('profile'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'testuser')

        # Update view GET
        resp = self.client.get(reverse('profile_update'))
        self.assertEqual(resp.status_code, 200)

        # POST new profile data
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'phone_number': '1234567890',
            'address': '123 Main St',
            'date_of_birth': '1990-05-05',
        }
        resp = self.client.post(reverse('profile_update'), data)
        self.assertRedirects(resp, reverse('profile_update'))

        # Confirm saved
        self.user.refresh_from_db()
        p = self.user.userprofile
        self.assertEqual(self.user.first_name, 'John')
        self.assertEqual(p.phone_number, '1234567890')
        self.assertEqual(str(p.date_of_birth), '1990-05-05')
