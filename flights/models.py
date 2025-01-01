from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class Flight(models.Model):
    """
    Generic flight model that can work with any provider
    """
    FLIGHT_STATUS = (
        ('SCHEDULED', 'Scheduled'),
        ('DELAYED', 'Delayed'),
        ('DEPARTED', 'Departed'),
        ('ARRIVED', 'Arrived'),
        ('CANCELLED', 'Cancelled'),
    )

    # Common flight details
    flight_number = models.CharField(max_length=20)
    origin = models.CharField(max_length=5)  # IATA airport code
    destination = models.CharField(max_length=5)  # IATA airport code
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    duration = models.DurationField()
    status = models.CharField(max_length=20, choices=FLIGHT_STATUS)
    
    # Price information
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')  # ISO currency code

    # Provider information
    provider_name = models.CharField(max_length=50)  # e.g., 'amadeus', 'other_provider'
    provider_reference = models.CharField(max_length=100)  # Provider's unique identifier
    provider_data = models.JSONField(default=dict)  # Store provider-specific data

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=['flight_number']),
            models.Index(fields=['departure_time']),
            models.Index(fields=['provider_reference']),
        ]

class PassengerDetail(models.Model):
    """
    Stores passenger information independently
    """
    PASSENGER_TYPE = (
        ('ADULT', 'Adult'),
        ('CHILD', 'Child'),
        ('INFANT', 'Infant'),
    )
    
    # Personal information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    passenger_type = models.CharField(max_length=10, choices=PASSENGER_TYPE)
    
    # Travel document
    passport_number = models.CharField(max_length=50, unique=True)
    passport_expiry = models.DateField()
    nationality = models.CharField(max_length=2)  # ISO country code
    
    # Contact information
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    
    # Special requirements
    special_requirements = models.TextField(blank=True)

    # Metadata
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.passport_number})"

    class Meta:
        indexes = [
            models.Index(fields=['passport_number']),
            models.Index(fields=['created_by']),
        ]

class FlightBooking(models.Model):
    """
    Stores booking information for flights
    """
    BOOKING_STATUS = (
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
        ('COMPLETED', 'Completed'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    flight = models.ForeignKey(Flight, on_delete=models.PROTECT)
    booking_reference = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=20, choices=BOOKING_STATUS)
    
    # Booking details
    booking_date = models.DateTimeField(default=timezone.now)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    
    # Link to passengers
    passengers = models.ManyToManyField(PassengerDetail, through='BookingPassenger')
    
    # Provider booking data
    provider_booking_id = models.CharField(max_length=100)
    provider_data = models.JSONField(default=dict)

    # Metadata
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Booking {self.booking_reference}"

    class Meta:
        indexes = [
            models.Index(fields=['booking_reference']),
            models.Index(fields=['booking_date']),
        ]

class BookingPassenger(models.Model):
    """
    Through model for booking-passenger relationship
    """
    booking = models.ForeignKey(FlightBooking, on_delete=models.CASCADE)
    passenger = models.ForeignKey(PassengerDetail, on_delete=models.PROTECT)
    seat_number = models.CharField(max_length=10, blank=True)
    checked_in = models.BooleanField(default=False)
    boarding_pass_issued = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['booking', 'passenger']

    def __str__(self):
        return f"{self.passenger} on {self.booking}"

class SearchHistory(models.Model):
    """
    Stores user's flight search history
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    origin = models.CharField(max_length=5)  # IATA airport code
    destination = models.CharField(max_length=5)  # IATA airport code
    departure_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    passengers = models.JSONField(default=dict)  # Store passenger counts by type
    search_params = models.JSONField(default=dict)  # Store additional search parameters
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['user', '-created_at']),
        ]
