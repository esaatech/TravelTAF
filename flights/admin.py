from django.contrib import admin
from .models import Flight, FlightBooking, PassengerDetail, BookingPassenger

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('flight_number', 'origin', 'destination', 'departure_time', 'status')
    list_filter = ('status', 'origin', 'destination')
    search_fields = ('flight_number', 'origin', 'destination')
    date_hierarchy = 'departure_time'

@admin.register(PassengerDetail)
class PassengerDetailAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'passport_number', 'passenger_type', 'nationality', 'created_by')
    list_filter = ('passenger_type', 'nationality', 'created_by')
    search_fields = ('first_name', 'last_name', 'passport_number', 'email')
    date_hierarchy = 'created_at'

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    get_full_name.short_description = 'Full Name'

class BookingPassengerInline(admin.TabularInline):
    model = BookingPassenger
    extra = 0
    readonly_fields = ('checked_in', 'boarding_pass_issued')

@admin.register(FlightBooking)
class FlightBookingAdmin(admin.ModelAdmin):
    list_display = ('booking_reference', 'user', 'flight', 'status', 'booking_date', 'total_price')
    list_filter = ('status', 'currency', 'is_active')
    search_fields = ('booking_reference', 'user__username', 'flight__flight_number')
    date_hierarchy = 'booking_date'
    inlines = [BookingPassengerInline]

@admin.register(BookingPassenger)
class BookingPassengerAdmin(admin.ModelAdmin):
    list_display = ('booking', 'passenger', 'seat_number', 'checked_in', 'boarding_pass_issued')
    list_filter = ('checked_in', 'boarding_pass_issued')
    search_fields = ('booking__booking_reference', 'passenger__passport_number', 'seat_number')
