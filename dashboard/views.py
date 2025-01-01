from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from credits.models import UserCredit, CreditTransaction

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        section = self.request.GET.get('section', None)
        
        # Add common context data
        context.update({
            'credit_balance': self.get_credit_balance(),
            'display_name': self.get_display_name(),
            'unread_notifications': self.get_notifications_status(),
            'unread_messages': self.get_messages_status(),
            'current_section': section.title() if section else None,
            'section_template': f'dashboard/sections/{section}.html' if section else None,
        })

        # Add section-specific data
        if section:
            method_name = f'get_{section}_data'
            if hasattr(self, method_name):
                context.update(getattr(self, method_name)())
        else:
            # Default dashboard data
            context.update(self.get_home_data())

        return context

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

    def get_credits_data(self):
        """Data for the credits section"""
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
        """Data for the profile section"""
        return {
            'user': self.request.user,
            # Add any other profile-specific data
        }