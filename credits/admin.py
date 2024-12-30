from django.contrib import admin
from django.utils.html import format_html
from decimal import Decimal
from .models import UserCredit, CreditTransaction, CreditPayment

@admin.register(UserCredit)
class UserCreditAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'balance', 'last_updated')
    search_fields = ('user__email', 'user__username')
    readonly_fields = ('last_updated',)

    def user_email(self, obj):
        return obj.user.email

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields + ('user',)
        return self.readonly_fields

    # Add action to give bonus credits
    actions = ['give_bonus_credits']

    @admin.action(description='Give bonus credits to selected users')
    def give_bonus_credits(self, request, queryset):
        from django.contrib import messages
        from django.shortcuts import render
        from django import forms

        class BonusCreditForm(forms.Form):
            _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
            credits = forms.DecimalField(
                min_value=Decimal('0.01'),
                decimal_places=2,
                label='Credits to add'
            )
            reason = forms.CharField(
                max_length=255,
                required=True,
                label='Reason for bonus'
            )

        if 'apply' in request.POST:
            form = BonusCreditForm(request.POST)
            if form.is_valid():
                credits = form.cleaned_data['credits']
                reason = form.cleaned_data['reason']
                updated = 0

                for user_credit in queryset:
                    user_credit.balance += credits
                    user_credit.save()

                    # Create transaction record
                    CreditTransaction.objects.create(
                        user=user_credit.user,
                        amount=credits,
                        transaction_type='BONUS',
                        description=f'Admin bonus: {reason}'
                    )
                    updated += 1

                self.message_user(
                    request,
                    f'Successfully added {credits} credits to {updated} users.',
                    messages.SUCCESS
                )
                return None

        form = BonusCreditForm(initial={
            '_selected_action': request.POST.getlist('_selected_action')
        })

        return render(
            request,
            'admin/give_bonus_credits.html',
            {
                'title': 'Give Bonus Credits',
                'users': queryset,
                'form': form,
            }
        )

@admin.register(CreditTransaction)
class CreditTransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'transaction_type', 'currency', 'created_at']
    list_filter = ['transaction_type', 'currency', 'created_at']
    search_fields = ['user__username', 'payment_intent_id', 'description']
    readonly_fields = ['payment_intent_id', 'created_at']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

    def user_email(self, obj):
        return obj.user.email

@admin.register(CreditPayment)
class CreditPaymentAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'total', 'status', 'created')
    list_filter = ('status', 'created')
    search_fields = ('user__email',)
    readonly_fields = ('created',)

    def user_email(self, obj):
        return obj.user.email
