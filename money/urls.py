from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('expenses.urls')),
    path('preferences/',include('user_preferences.urls')),
    path('auth/',include('authentication.urls')),
    path('income/',include("income.urls")),
]
