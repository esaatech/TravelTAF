# Flight Management Application

A Django application for managing flight bookings, passenger details, and travel documentation.

## Features

### 1. Flight Management
- Track flights with detailed information
- Support for multiple flight statuses (SCHEDULED, COMPLETED, CANCELLED)
- Store flight routes, times, and pricing
- Integration with provider data (e.g., Amadeus)

### 2. Passenger Management
- Store passenger details independently
- Support for different passenger types (ADULT, CHILD, INFANT)
- Track travel documents (passport, visa)
- Reusable passenger profiles across bookings

Example passenger creation:
python
passenger = PassengerDetail.objects.create(
first_name='John',
last_name='Doe',
date_of_birth='1990-01-01',
passenger_type='ADULT',
passport_number='AB123456',
passport_expiry='2025-01-01',
nationality='US',
email='john@example.com',
created_by=user
)

### 3. Booking System
- Create and manage flight bookings
- Link multiple passengers to a booking
- Track booking status and payment
- Generate unique booking references

Example booking creation:
python
booking = FlightBooking.objects.create(
user=user,
flight=flight,
booking_reference='BKAF123',
status='CONFIRMED',
total_price=499.99,
currency='USD'
)
Link passenger to booking
BookingPassenger.objects.create(
booking=booking,
passenger=passenger,
seat_number='12A'
)

### 4. Dashboard Features
- View upcoming flights
- Access flight history
- Download/email boarding passes
- Manage passenger information

## Models

### Flight
Stores flight information:
- Flight number
- Origin/Destination
- Departure/Arrival times
- Status
- Pricing
- Provider information

### PassengerDetail
Stores passenger information:
- Personal details
- Travel documents
- Contact information
- Special requirements

### FlightBooking
Manages booking information:
- Booking reference
- Flight details
- Status
- Payment information
- User reference

### BookingPassenger
Links passengers to bookings:
- Seat assignments
- Check-in status
- Boarding pass status

## Usage Examples

### 1. Creating Test Data
Use management commands to create test flights and bookings:
```bash
python manage.py create_test_flights
python manage.py create_flight_history
```


### 2. Viewing Flight Details
Access flight details through the dashboard:

python
View specific booking details
booking = FlightBooking.objects.select_related('flight').prefetch_related(
'bookingpassenger_setpassenger'
).get(booking_reference='BKAF123')



### 3. Managing Passengers
Add passengers to a booking:
python
Link existing passenger to booking
BookingPassenger.objects.create(
booking=booking,
passenger=passenger,
seat_number='14C'
)



## API Endpoints (if applicable)

- GET /api/flights/ - List available flights
- POST /api/bookings/ - Create new booking
- GET /api/passengers/ - List user's passengers

## Contributing

1. Fork the repository
2. Create your feature branch
3. Submit a pull request

## License

MIT License - feel free to use and modify as needed.