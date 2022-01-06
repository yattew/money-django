from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    path("",index,name="income"),
    path("add_income/",add_income,name="add_income"),
    path("income_search/<int:page_num>",csrf_exempt(income_search),name="income_search"),
    path("edit_income/<int:id>",edit_income,name="edit_income"),
    path("delete_income/<int:id>",delete_income,name="delete_income"),
    path('income_summary',csrf_exempt(income_summary),name="income_summary")
]