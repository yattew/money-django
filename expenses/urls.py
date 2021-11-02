from django.urls import path
from .views import *


urlpatterns = [
    path('',index,name="index"),
    path('add_expenses/',add_expense,name="add_expenses")
]