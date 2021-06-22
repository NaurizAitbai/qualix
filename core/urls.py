from django.urls import path
from core import views


urlpatterns = [
    path('', views.auth_check, name='auth_check')
]