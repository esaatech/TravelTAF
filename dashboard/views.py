from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from credits.models import UserCredit, CreditTransaction

# Create your views here.
@login_required
def dashboard(request):
    # Get user's credit balance
    user_credit = UserCredit.objects.filter(user=request.user).first()
    credit_balance = user_credit.balance if user_credit else 0

    # Get recent transactions
    recent_transactions = CreditTransaction.objects.filter(
        user=request.user
    ).order_by('-created_at')[:5]

    # Get user's display name (full name if available, otherwise username)
    display_name = request.user.get_full_name() or request.user.username

    context = {
        'recent_transactions': recent_transactions,
        'unread_notifications': request.user.notifications.unread().exists() if hasattr(request.user, 'notifications') else False,
        'credit_balance': credit_balance,
        'display_name': display_name,
    }
    
    return render(request, 'dashboard/dashboard.html', context)