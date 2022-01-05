from django.shortcuts import redirect, render
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages,auth
import json

# Create your views here.


class RegisterView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')
    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if not User.objects.filter(username = username).exists():
            if not User.objects.filter(email = email).exists():
                if len(password)<=6:
                    messages.error(request,"password must be greater than 6 characters")
                    return render(request, 'authentication/register.html')

                user = User.objects.create_user(username = username,email=email)
                user.set_password(password)
                user.save()
                messages.success(request,"account successfully created")
                return render(request, 'authentication/register.html')
        return render(request, 'authentication/register.html')

class LoginView(View):
    def get(self,request):
        return render(request, 'authentication/login.html')

    def post(self,request):
        data = request.POST
        username = data['username']
        password = data['password']
        if username and password:
            user = auth.authenticate(username = username, password = password)
            if user:
                auth.login(request,user)
                messages.success(request,f"welcome {user.username}, you are now logged in")
                return redirect('expenses')
            else:
                messages.error(request,"invalid credentials")
        else:
            messages.error(request, "please enter the username and password")
        return render(request,'authentication/login.html')

class LogoutView(View):
    def get(self, request):
        auth.logout(request)
        messages.success(request, "you have been logged out")
        return redirect('login')

class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = str(data['username'])
        if not username.isalnum():
            return JsonResponse({'username_error': 'username should only contain alpha numeric characters'}, status=400)
        elif User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'username is already taken'}, status=409)
        else:
            return JsonResponse({'username_valid': True})


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = str(data['email'])
        if not validate_email(email):
            return JsonResponse({'email_error': 'email is not valid'}, status=400)
        elif User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'email is already taken'}, status=409)
        else:
            return JsonResponse({'email_valid': True})
