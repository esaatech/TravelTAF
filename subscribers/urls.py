from django.urls import path
from . import views

app_name = 'subscribers'

urlpatterns = [
    path('subscribe/', views.subscribe, name='subscribe'),
]
