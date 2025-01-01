from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('passenger/save/', views.SavePassengerView.as_view(), name='save_passenger'),
]