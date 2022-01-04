from django.contrib.auth.models import User
from django.core import paginator
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages
from django.shortcuts import redirect
from django.core.paginator import Paginator
import json
from django.db.models import Q
from django.http import JsonResponse
from user_preferences.models import UserPreference
# Create your views here.


@login_required(login_url='/auth/login')
def index(request):
    currency = UserPreference.objects.get(user=request.user).currency
    context = {
        "currency":currency
    }
    return render(request, 'expenses/index.html', context)


@login_required(login_url='/auth/login')
def add_expense(request):
    categories = Category.objects.all()
    context = {
        "categories": categories,
        "values": request.POST
    }
    if request.method == "POST":
        ammount = request.POST["ammount"]
        description = request.POST["description"]
        category = request.POST["category"]
        date = request.POST["date"]
        error_str = ""
        if not ammount:
            error_str += "Ammount is required "
        if not description:
            error_str += "description is required "
        if not category:
            error_str += "category is required"
        if not error_str:
            Expense.objects.create(
                owner=request.user,
                ammount=ammount,
                date=date,
                category=category,
                description=description)
            messages.success(request, "expense added successfully")
            return redirect('expenses')
        else:
            messages.error(request, error_str)
    else:
        pass
    return render(request, 'expenses/add_expense.html', context)


@login_required(login_url='/auth/login')
def edit_expense(request, id):
    categories = Category.objects.all()
    expense = Expense.objects.get(pk=id)
    context = {
        "categories": categories,
        "values": request.POST,
        "expense": expense
    }
    if request.method == "GET":
        context["values"] = expense
    else:
        data = request.POST
        expense.ammount = data["ammount"]
        expense.description = data["description"]
        expense.category = data["category"]
        if data["date"]:
            expense.date = data["date"]
        expense.save()
        messages.success(request, "expense updated successfully")
        return redirect("expenses")
    return render(request, 'expenses/edit_expense.html', context)


@login_required(login_url='/auth/login')
def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, "expense deleted successfully")
    return redirect("expenses")


@login_required(login_url='/auth/login')
def expense_search(request,page_num=1):
    if request.method == "POST":
        search_querry = json.loads(
            request.body.decode()).get("search_querry", "")
        expenses = None
        if len(search_querry) <= 0:
            expenses = Expense.objects.filter(owner=request.user)
        else:
            expenses = Expense.objects.filter(
                Q(ammount__startswith=search_querry) |
                Q(date__startswith=search_querry) |
                Q(description__icontains=search_querry) |
                Q(category__icontains=search_querry),
                owner=request.user
            )
    paginator = Paginator(expenses, 4)
    page_obj = paginator.get_page(page_num)
    expenses = list(page_obj.object_list.values())
    for i in range(0,len(expenses)):
        del expenses[i]["owner_id"]
        expenses[i]["date"] = str(expenses[i]["date"])
    data = {
        "expenses":expenses,
        "curr_page":page_num,
        "tot_pages":page_obj.paginator.num_pages,
        }
    return JsonResponse(data, safe=False)
