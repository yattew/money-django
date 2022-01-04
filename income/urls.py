from django.urls import path
from .views import *
urlpatterns = [
    path("index/",index,name="income"),
    path("add_income/",add_income,name="add_income")
]