from django.urls import path
from . import views
from .views import DashboardView, UpdateProfileView, ChangePasswordView


app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('passenger/save/', views.SavePassengerView.as_view(), name='save_passenger'),
    path('profile/update/', UpdateProfileView.as_view(), name='update_profile'),
    path('profile/change-password/', ChangePasswordView.as_view(), name='change_password'),
]