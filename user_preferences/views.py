from django.core.checks import messages
from django.shortcuts import render
import os
import json
from django.conf import settings
from django.contrib import messages
from django.views import View
from .models import UserPreference
# Create your views here.


class IndexView(View):
    def get(self, request):
        context = {}
        context["currencies"] = self.get_currencies()
        pref_exist = UserPreference.objects.filter(
            user=request.user).exists()
        if pref_exist:
            context["preference"] = UserPreference.objects.get(
                user=request.user)
        return render(request, 'user_preferences/index.html', context=context)

    def post(self, request):
        context = {}
        context["currencies"] = self.get_currencies()
        pref_exist = UserPreference.objects.filter(
            user=request.user).exists()
        currency = request.POST['currency']
        user_preference = None
        if pref_exist:
            user_preference = UserPreference.objects.get(user=request.user)
            user_preference.currency = currency
            user_preference.save()
        else:
            user_preference = UserPreference.objects.create(user=request.user, currency=currency)
        messages.success(request, "changes saved")
        context["preference"] = user_preference
        return render(request, 'user_preferences/index.html', context=context)

    def get_currencies(self) -> list:
        currencies = []
        file_path = os.path.join(settings.BASE_DIR, 'currencies.json')
        with open(file_path, 'r') as file:
            data = json.load(file)
            for k, v in data.items():
                currencies.append({"name": k, "value": v})
        return currencies