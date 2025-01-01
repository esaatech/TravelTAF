from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.db.models import Max, Subquery, OuterRef
from flights.models import Flight, FlightBooking, PassengerDetail
from credits.models import UserCredit, CreditTransaction
from subscriptions.models import UserProfile
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import update_session_auth_hash

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        section = self.request.GET.get('section', None)
        
        # Map add_passenger to edit_passenger template
        template_section = 'edit_passenger' if section == 'add_passenger' else section
        
        # Add common context data
        context.update({
            'credit_balance': self.get_credit_balance(),
            'display_name': self.get_display_name(),
            'unread_notifications': self.get_notifications_status(),
            'unread_messages': self.get_messages_status(),
            'current_section': section.title() if section else None,
            'section_template': f'dashboard/sections/{template_section}.html' if template_section else None,
        })

        # Handle section-specific data
        if section:
            method_name = f'get_{section}_data'
            if hasattr(self, method_name):
                context.update(getattr(self, method_name)())
        
        return context

    # Helper methods for common context data
    def get_credit_balance(self):
        user_credit = UserCredit.objects.filter(user=self.request.user).first()
        return user_credit.balance if user_credit else 0

    def get_display_name(self):
        return self.request.user.get_full_name() or self.request.user.username

    def get_notifications_status(self):
        return (self.request.user.notifications.unread().exists() 
                if hasattr(self.request.user, 'notifications') else False)

    def get_messages_status(self):
        return (self.request.user.messages.unread().exists() 
                if hasattr(self.request.user, 'messages') else False)

    def get_recent_transactions(self):
        return CreditTransaction.objects.filter(
            user=self.request.user
        ).order_by('-created_at')[:5]

    # Section-specific data methods
    def get_home_data(self):
        """Data for the default dashboard view"""
        return {
            'recent_transactions': self.get_recent_transactions(),
        }

    # Section-specific data methods
    def get_credits_data(self):
        return {
            'recent_transactions': self.get_recent_transactions(),
            'credit_balance': self.get_credit_balance(),
            # Add any other credits-specific data
        }

    def get_subscriptions_data(self):
        """Data for the subscriptions section"""
        return {
            'current_subscription': None,  # Replace with actual subscription query
            # Add any other subscription-specific data
        }

    def get_profile_data(self):
        """Get user profile data"""
        try:
            profile, created = UserProfile.objects.get_or_create(user=self.request.user)
            return {
                'user': self.request.user,
                'profile': profile
            }
        except Exception as e:
            messages.error(self.request, f'Error loading profile: {str(e)}')
            return {'user': self.request.user}

    def update_profile(self, request):
        """Update user and profile information"""
        user = request.user
        profile = user.profile

        # Update user info
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()

        # Update profile info
        profile.phone = request.POST.get('phone', '')
        profile.address = request.POST.get('address', '')
        profile.email_notifications = request.POST.get('email_notifications') == 'on'
        profile.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('dashboard:dashboard') + '?section=profile'

    def change_password(self, request):
        """Change user password"""
        user = request.user
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not user.check_password(current_password):
            messages.error(request, 'Current password is incorrect.')
        elif new_password != confirm_password:
            messages.error(request, 'New passwords do not match.')
        else:
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # Keep user logged in
            messages.success(request, 'Password changed successfully.')

        return redirect('dashboard:dashboard') + '?section=profile'

    def get_flights_data(self):
        return {
            'current_flights': self.get_current_flights(),
            'recent_flights': self.get_recent_flights(),
            'flight_history': self.get_flight_history()
        }

    def get_current_flights(self):
        """Get upcoming and active flights"""
        return FlightBooking.objects.filter(
            user=self.request.user,
            status='CONFIRMED',
            flight__departure_time__gte=timezone.now()
        ).select_related('flight').order_by('flight__departure_time')

    def get_recent_flights(self):
        """Get recently completed flights"""
        return FlightBooking.objects.filter(
            user=self.request.user,
            status='COMPLETED',
            flight__arrival_time__lte=timezone.now()
        ).select_related('flight').order_by('-flight__arrival_time')[:5]

    def get_flight_history(self):
        """Get all past flights"""
        return FlightBooking.objects.filter(
            user=self.request.user
        ).select_related('flight').order_by('-flight__departure_time')

    def get_flight_detail(self, flight_number):
        """Get detailed flight information"""
        try:
            booking = FlightBooking.objects.select_related(
                'flight'
            ).prefetch_related(
                'passengers'
            ).get(
                flight__flight_number=flight_number,
                user=self.request.user
            )
            return {'booking': booking}
        except FlightBooking.DoesNotExist:
            return None

    def get_passengers_data(self):
        """Get all saved passenger details for the user"""
        saved_passengers = PassengerDetail.objects.filter(
            created_by=self.request.user
        ).order_by('first_name', 'last_name')

        return {
            'saved_passengers': saved_passengers,
            'total_passengers': saved_passengers.count()
        }

    def get_edit_passenger_data(self):
        """Get passenger data for editing"""
        passport_number = self.request.GET.get('passport')
        if passport_number:
            try:
                passenger = PassengerDetail.objects.get(
                    passport_number=passport_number,
                    created_by=self.request.user
                )
                return {'passenger': passenger}
            except PassengerDetail.DoesNotExist:
                return {'error': 'Passenger not found'}
        return {}

    def get_add_passenger_data(self):
        """Reuse edit template for adding new passenger"""
        return {'passenger': None}  # Pass None to indicate new passenger

    def get_flight_history_data(self):
        """Get user's flight history with different statuses"""
        bookings = FlightBooking.objects.filter(
            user=self.request.user
        ).select_related(
            'flight'
        ).prefetch_related(
            'passengers'
        ).order_by(
            '-flight__departure_time'
        )

        # Categorize bookings by status
        history_categories = {
            'completed': bookings.filter(status='COMPLETED'),
            'cancelled': bookings.filter(status='CANCELLED'),
            'upcoming': bookings.filter(status='CONFIRMED', flight__departure_time__gt=timezone.now()),
            'past': bookings.filter(status='CONFIRMED', flight__departure_time__lte=timezone.now())
        }

        return {
            'history_categories': history_categories,
            'total_flights': bookings.count()
        }

    def get_flight_detail_data(self):
        booking_reference = self.request.GET.get('flight')
        if booking_reference:
            try:
                booking = FlightBooking.objects.select_related(
                    'flight'
                ).prefetch_related(
                    'bookingpassenger_set__passenger'
                ).get(
                    booking_reference=booking_reference,
                    user=self.request.user
                )
                return {'booking': booking}
            except FlightBooking.DoesNotExist:
                return {'error': 'Booking not found'}
        return {}

class SavePassengerView(LoginRequiredMixin, View):
    def post(self, request):
        passport_number = request.POST.get('passport_number')
        
        # Get form data
        passenger_data = {
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
            'date_of_birth': request.POST.get('date_of_birth'),
            'passenger_type': request.POST.get('passenger_type'),
            'passport_number': passport_number,
            'passport_expiry': request.POST.get('passport_expiry'),
            'nationality': request.POST.get('nationality'),
            'email': request.POST.get('email', ''),
            'phone': request.POST.get('phone', ''),
            'special_requirements': request.POST.get('special_requirements', '')
        }

        try:
            # Try to get existing passenger
            passenger = PassengerDetail.objects.filter(
                passport_number=passport_number,
                created_by=request.user
            ).first()

            if passenger:
                # Update existing passenger
                for key, value in passenger_data.items():
                    setattr(passenger, key, value)
                passenger.save()
                messages.success(request, 'Passenger details updated successfully.')
            else:
                # Create new passenger
                passenger_data['created_by'] = request.user
                PassengerDetail.objects.create(**passenger_data)
                messages.success(request, 'Passenger details saved successfully.')

        except Exception as e:
            messages.error(request, f'Error saving passenger details: {str(e)}')

        return redirect(reverse('dashboard:dashboard') + '?section=passengers')

class UpdateProfileView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = request.user
        try:
            # Get or create profile
            profile, created = UserProfile.objects.get_or_create(user=user)

            # Update user info
            user.first_name = request.POST.get('first_name', '')
            user.last_name = request.POST.get('last_name', '')
            user.email = request.POST.get('email', '')
            user.save()

            # Update profile info
            profile.phone = request.POST.get('phone', '')
            profile.address = request.POST.get('address', '')
            profile.email_notifications = request.POST.get('email_notifications') == 'on'
            profile.save()

            messages.success(request, 'Profile updated successfully.')
        except Exception as e:
            messages.error(request, f'Error updating profile: {str(e)}')

        return redirect(reverse('dashboard:dashboard') + '?section=profile')

class ChangePasswordView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = request.user
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not user.check_password(current_password):
            messages.error(request, 'Current password is incorrect.')
        elif new_password != confirm_password:
            messages.error(request, 'New passwords do not match.')
        else:
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # Keep user logged in
            messages.success(request, 'Password changed successfully.')

        return redirect(reverse('dashboard:dashboard') + '?section=profile')
