from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

# Travel Options like Flights, Trains, Buses
class TravelOption(models.Model):
    TYPE_CHOICES = [
        ('flight', 'Flight'),
        ('train', 'Train'),
        ('bus', 'Bus'),
    ]

    travel_id = models.CharField(max_length=20, unique=True)
    type = models.CharField(max_length=6, choices=TYPE_CHOICES)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_datetime = models.DateTimeField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    available_seats = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.get_type_display()} {self.travel_id}: {self.source} → {self.destination}"

    class Meta:
        ordering = ['departure_datetime']

# Booking model linking user with travel
class Booking(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    travel = models.ForeignKey(TravelOption, on_delete=models.CASCADE)
    seats = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='confirmed')

    def __str__(self):
        return f"Booking {self.id} by {self.user.username}"

# Extended User information
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username

from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta
import calendar

class RecurringTravelOption(models.Model):
    TYPE_CHOICES = [('flight', 'Flight'), ('train', 'Train'), ('bus', 'Bus')]
    FREQUENCY_CHOICES = [('daily', 'Daily'), ('weekly', 'Weekly'), ('custom', 'Custom')]

    travel_id = models.CharField(max_length=20, unique=True)
    type = models.CharField(max_length=6, choices=TYPE_CHOICES)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.TimeField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    available_seats = models.PositiveIntegerField()
    
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, default='daily')
    weekdays = models.CharField(
        max_length=20, blank=True, help_text="Comma-separated weekdays for custom recurrence, e.g., Mon,Wed,Fri"
    )

    def __str__(self):
        return f"{self.get_type_display()} {self.travel_id} {self.source} → {self.destination}"

    def get_next_instances(self, days_ahead=7):
        today = timezone.now().date()
        instances = []

        for i in range(days_ahead):
            day = today + timedelta(days=i)
            if self.frequency == 'daily':
                valid = True
            elif self.frequency == 'weekly':
                valid = day.weekday() == today.weekday()
            elif self.frequency == 'custom':
                day_name = calendar.day_name[day.weekday()]
                valid = day_name[:3] in self.weekdays.split(',')

            if valid:
                dt = datetime.combine(day, self.departure_time)
                instances.append({
                    'date': day,
                    'datetime': dt,
                    'travel': self
                })

        return instances
