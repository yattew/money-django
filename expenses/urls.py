from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('',index,name="expenses"),
    path('add_expense/',add_expense,name="add_expense"),
    path('edit_expense/<int:id>',edit_expense,name="edit_expense"),
    path('delete_expense/<int:id>',delete_expense,name="delete_expense"),
    path('expense_search/<int:page_num>',csrf_exempt(expense_search),name="expense_search")
]