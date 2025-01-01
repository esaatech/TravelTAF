from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from flights.models import Flight, FlightBooking, PassengerDetail, BookingPassenger
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates test flight data for development'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating test flights...')

        # Create test flights
        test_flights = [
            {
                'flight_number': 'AF123',
                'origin': 'CDG',
                'destination': 'JFK',
                'departure_time': timezone.now() + timedelta(days=7),
                'arrival_time': timezone.now() + timedelta(days=7, hours=8),
                'duration': timedelta(hours=8),
                'status': 'SCHEDULED',
                'base_price': '499.99',
                'currency': 'USD',
                'provider_name': 'amadeus',
                'provider_reference': 'AM123456',
                'provider_data': {
                    'aircraft': 'Boeing 777',
                    'cabin_class': 'economy',
                    'available_seats': 150
                },
                'is_active': True
            },
            {
                'flight_number': 'BA456',
                'origin': 'LHR',
                'destination': 'DXB',
                'departure_time': timezone.now() + timedelta(days=14),
                'arrival_time': timezone.now() + timedelta(days=14, hours=7),
                'duration': timedelta(hours=7),
                'status': 'SCHEDULED',
                'base_price': '599.99',
                'currency': 'USD',
                'provider_name': 'amadeus',
                'provider_reference': 'AM789012',
                'provider_data': {
                    'aircraft': 'Airbus A380',
                    'cabin_class': 'business',
                    'available_seats': 76
                }
            },
            {
                'flight_number': 'EK789',
                'origin': 'DXB',
                'destination': 'SYD',
                'departure_time': timezone.now() + timedelta(days=10),
                'arrival_time': timezone.now() + timedelta(days=10, hours=14),
                'duration': timedelta(hours=14),
                'status': 'SCHEDULED',
                'base_price': '899.99',
                'currency': 'USD',
                'provider_name': 'amadeus',
                'provider_reference': 'AM345678',
                'provider_data': {
                    'aircraft': 'Airbus A380',
                    'cabin_class': 'first',
                    'available_seats': 14
                }
            }
        ]

        created_flights = []
        for flight_data in test_flights:
            flight, created = Flight.objects.get_or_create(
                flight_number=flight_data['flight_number'],
                defaults=flight_data
            )
            created_flights.append(flight)
            status = 'Created' if created else 'Already exists'
            self.stdout.write(f'{status}: Flight {flight.flight_number}')

        # Create test user if none exists
        test_user = User.objects.first()
        if not test_user:
            test_user = User.objects.create_user(
                username='testuser',
                email='test@example.com',
                password='testpass123'
            )

        if test_user and created_flights:
            # Create test passenger
            test_passenger, created = PassengerDetail.objects.get_or_create(
                passport_number='AB123456',
                defaults={
                    'first_name': 'Test',
                    'last_name': 'User',
                    'date_of_birth': '1990-01-01',
                    'passenger_type': 'ADULT',
                    'passport_expiry': '2025-01-01',
                    'nationality': 'US',
                    'email': test_user.email,
                    'phone': '+1234567890',
                    'created_by': test_user
                }
            )
            
            # Create bookings for first two flights
            for flight in created_flights[:2]:
                # Create booking
                booking = FlightBooking.objects.create(
                    user=test_user,
                    flight=flight,
                    booking_reference=f'BK{flight.flight_number}',
                    status='CONFIRMED',
                    total_price=flight.base_price,
                    currency=flight.currency,
                    provider_booking_id=f'PB{flight.provider_reference}',
                    provider_data={'booking_class': 'economy'},
                    is_active=True
                )

                # Link passenger to booking
                BookingPassenger.objects.create(
                    booking=booking,
                    passenger=test_passenger,
                    seat_number=f'A{booking.id}'
                )

                self.stdout.write(f'Created: Booking {booking.booking_reference}')

        self.stdout.write(self.style.SUCCESS('Successfully created test flight data')) 