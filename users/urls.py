from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import *

app_name = 'users'

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('sign_up/', SignupView.as_view(), name='signup')
]