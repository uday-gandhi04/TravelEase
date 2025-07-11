from django.core.management.base import BaseCommand
from bookings.models import TravelOption
from django.utils import timezone
from datetime import timedelta
import random

class Command(BaseCommand):
    help = 'Seed the database with sample TravelOption entries'

    def handle(self, *args, **kwargs):
        TravelOption.objects.all().delete()

        sample_data = [
            ('BUS1234', 'train',  'Mumbai','Nagpur', 50, 500),
            ('TR4567', 'flight',  'Hyderabad','Pune', 40, 850),
            ('FL6789', 'bus',  'Chennai','Bangalore', 30, 3200),
            ('BUS2345', 'flight',  'Agra','Delhi', 25, 300),
            ('TR5678', 'train',  'Patna','Kolkata', 20, 700),
            ('BUS3457', 'bus',  'Udaipur','Jaipur', 15, 600),
            ('TR6784', 'train',  'Surat','Ahmedabad', 30, 550),
            ('BUS4563', 'flight',  'Varanasi','Lucknow', 20, 400),
        ]

        now = timezone.now()

        for i, (travel_id, t_type, source, dest, seats, price) in enumerate(sample_data):
            TravelOption.objects.create(
                travel_id=travel_id,
                type=t_type,
                source=source,
                destination=dest,
                departure_datetime=now + timedelta(days=i+14, hours=random.randint(1, 10)),
                price=price,
                available_seats=seats
            )

        self.stdout.write(self.style.SUCCESS("✅ Successfully seeded TravelOption data."))
