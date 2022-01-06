from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Source, Income
from django.contrib import messages
from django.shortcuts import redirect
import json
from django.db.models import Q
from django.core.paginator import Paginator
from user_preferences.models import UserPreference
import datetime
# Create your views here.


@login_required(login_url='/auth/login')
def index(request):
    currency = UserPreference.objects.get(user=request.user).currency
    context = {
        "currency": currency
    }
    return render(request, "income/index.html", context=context)


@login_required(login_url='/auth/login')
def add_income(request):
    sources = Source.objects.all()
    context = {
        "sources": sources,
        "values": request.POST
    }
    if request.method == "POST":
        ammount = request.POST["ammount"]
        description = request.POST["description"]
        source = request.POST["source"]
        date = request.POST["date"]
        error_str = ""
        if not ammount:
            error_str += "Ammount is required "
        if not description:
            error_str += "description is required "
        if not source:
            error_str += "source is required"
        if not error_str:
            Income.objects.create(
                owner=request.user,
                ammount=ammount,
                date=date,
                source=source,
                description=description,
            )
            messages.success(request, "Income was added successfully")
            return redirect("income")
        else:
            messages.error(request, error_str)
    return render(request, "income/add_income.html", context=context)


@login_required(login_url='/auth/login')
def edit_income(request, id):
    sources = Source.objects.all()
    income = Income.objects.get(pk=id)
    context = {
        "sources": sources,
        "values": request.POST,
        "income": income
    }
    if request.method == "GET":
        context["values"] = income
    else:
        data = request.POST
        income.ammount = data["ammount"]
        income.description = data["description"]
        income.source = data["source"]
        if data["date"]:
            income.date = data["date"]
        income.save()
        messages.success(request, "income updated successfully")
        return redirect("income")
    return render(request, 'income/edit_income.html', context)

@login_required(login_url='/auth/login')
def delete_income(request, id):
    income = Income.objects.get(pk=id)
    income.delete()
    messages.success(request, "income deleted successfully")
    return redirect("income")

def income_search(request, page_num=1):
    if request.method == "POST":
        search_querry = json.loads(
            request.body.decode()).get("search_querry", "")
        incomes = None
        if len(search_querry) <= 0:
            incomes = Income.objects.filter(owner=request.user)
        else:
            incomes = Income.objects.filter(
                Q(ammount__startswith=search_querry) |
                Q(date__startswith=search_querry) |
                Q(description__icontains=search_querry) |
                Q(source__icontains=search_querry),
                owner=request.user
            )
    paginator = Paginator(incomes, 4)
    page_obj = paginator.get_page(page_num)
    incomes = list(page_obj.object_list.values())
    for i in range(0, len(incomes)):
        del incomes[i]["owner_id"]
        incomes[i]["date"] = str(incomes[i]["date"])
    data = {
        "incomes": incomes,
        "curr_page": page_num,
        "tot_pages": page_obj.paginator.num_pages,
    }
    return JsonResponse(data, safe=False)

def income_summary(request):
    curr_date = datetime.date.today()
    date_30_day_before = curr_date-datetime.timedelta(days=30)
    incomes = Income.objects.filter(owner = request.user,date__gte=date_30_day_before).order_by("date")
    pie_data = {}
    line_data = {}
    data = {}
    for income in incomes:
        if income.source not in pie_data:
            pie_data[income.source] = income.ammount
        else:
            pie_data[income.source]+=income.ammount
    for income in incomes:
        date = str(income.date)
        if date not in line_data:
            line_data[date] = income.ammount
        else:
            line_data[date]+=income.ammount
    # for i in incomes:
    data = {
        "pie_data":pie_data,
        "line_data":line_data
    }
    return JsonResponse(data) 