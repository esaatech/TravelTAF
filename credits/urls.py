from django.urls import path
from . import views

app_name = 'credits'

urlpatterns = [
    path('purchase/', views.purchase_credits, name='purchase'),
    path('balance/', views.credit_balance, name='balance'),
    path('process-payment/', views.process_payment, name='process_payment'),
    path('payment/success/<int:payment_id>/', views.payment_success, name='payment_success'),
]