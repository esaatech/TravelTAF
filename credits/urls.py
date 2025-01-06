from django.urls import path
from . import views

app_name = 'credits'

urlpatterns = [
    path('purchase/', views.purchase_credits, name='purchase'),
    path('balance/', views.credit_balance, name='balance'),
    path('process-payment/', views.process_payment, name='process_payment'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/success/<int:transaction_id>/', views.payment_success, name='payment_success_with_id'),
    path('transaction-history/', views.transaction_history, name='transaction_history'),
]