from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import *


# app_name = 'authentication'

urlpatterns = [
    path('register/', RegisterView.as_view(),name="register"),
    path('login/', LoginView.as_view(),name="login"),
    path('logout/', LogoutView.as_view(),name="logout"),
    path('username_validation/', csrf_exempt(UsernameValidationView.as_view()),name="username-validation"),
    path('email_validation/', csrf_exempt(EmailValidationView.as_view()),name="email-validation"),
]
