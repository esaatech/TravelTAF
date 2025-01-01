from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from flights.models import Flight, FlightBooking, PassengerDetail, BookingPassenger
from django.contrib.auth import get_user_model
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates test flight history with completed and cancelled flights'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating test flight history...')

        # Get or create test user
        test_user = User.objects.first()
        if not test_user:
            test_user = User.objects.create_user(
                username='testuser',
                email='test@example.com',
                password='testpass123'
            )

        # Create some test passengers
        test_passengers = [
            {
                'passport_number': 'AB123456',
                'first_name': 'John',
                'last_name': 'Doe',
                'date_of_birth': '1990-01-01',
            },
            {
                'passport_number': 'CD789012',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'date_of_birth': '1985-06-15',
            },
            {
                'passport_number': 'EF345678',
                'first_name': 'Mike',
                'last_name': 'Johnson',
                'date_of_birth': '1995-12-30',
            }
        ]

        saved_passengers = []
        for p_data in test_passengers:
            passenger, created = PassengerDetail.objects.get_or_create(
                passport_number=p_data['passport_number'],
                defaults={
                    **p_data,
                    'passenger_type': 'ADULT',
                    'passport_expiry': '2025-01-01',
                    'nationality': 'US',
                    'email': f"{p_data['first_name'].lower()}@example.com",
                    'phone': '+1234567890',
                    'created_by': test_user
                }
            )
            saved_passengers.append(passenger)
            if created:
                self.stdout.write(f'Created passenger: {passenger.first_name} {passenger.last_name}')

        # Create historical flights
        historical_flights = [
            # Completed flights (past)
            {
                'flight_number': 'HC001',
                'origin': 'JFK',
                'destination': 'LAX',
                'departure_time': timezone.now() - timedelta(days=30),
                'status': 'COMPLETED'
            },
            {
                'flight_number': 'HC002',
                'origin': 'LAX',
                'destination': 'ORD',
                'departure_time': timezone.now() - timedelta(days=20),
                'status': 'COMPLETED'
            },
            # Cancelled flights
            {
                'flight_number': 'HC003',
                'origin': 'DFW',
                'destination': 'MIA',
                'departure_time': timezone.now() - timedelta(days=15),
                'status': 'CANCELLED'
            },
            {
                'flight_number': 'HC004',
                'origin': 'SEA',
                'destination': 'SFO',
                'departure_time': timezone.now() - timedelta(days=10),
                'status': 'CANCELLED'
            }
        ]

        for flight_data in historical_flights:
            # Create flight
            flight = Flight.objects.create(
                flight_number=flight_data['flight_number'],
                origin=flight_data['origin'],
                destination=flight_data['destination'],
                departure_time=flight_data['departure_time'],
                arrival_time=flight_data['departure_time'] + timedelta(hours=3),
                duration=timedelta(hours=3),
                status=flight_data['status'],
                base_price='299.99',
                currency='USD',
                provider_name='test_provider',
                provider_reference=f'TEST{flight_data["flight_number"]}',
                provider_data={'test': True},
                is_active=True
            )

            # Create booking
            booking = FlightBooking.objects.create(
                user=test_user,
                flight=flight,
                booking_reference=f'BK{flight_data["flight_number"]}',
                status=flight_data['status'],
                total_price='299.99',
                currency='USD',
                provider_booking_id=f'PB{flight_data["flight_number"]}',
                provider_data={'test': True},
                is_active=True
            )

            # Add random passengers to booking
            num_passengers = random.randint(1, len(saved_passengers))
            selected_passengers = random.sample(saved_passengers, num_passengers)
            
            for i, passenger in enumerate(selected_passengers):
                BookingPassenger.objects.create(
                    booking=booking,
                    passenger=passenger,
                    seat_number=f'{random.choice("ABCDEF")}{random.randint(1,30)}'
                )

            self.stdout.write(
                f'Created {flight_data["status"].lower()} flight {flight.flight_number} '
                f'with {num_passengers} passenger(s)'
            )

        self.stdout.write(self.style.SUCCESS('Successfully created test flight history')) 