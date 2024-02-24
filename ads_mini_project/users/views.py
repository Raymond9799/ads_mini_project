from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import CreateUserForm
from django.contrib.auth.models import User
from django.http import JsonResponse

# Create your views here.

def index(request):
    return render(request, "users/login.html")

def user_login(request):    
    if request.method == "POST":
        
        print(f"here is the request: {request}")
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(f"here is the username: {username} and password: {password}")
        user = authenticate(request, username=username, password=password)
        print(user)
        if user:
            login(request, user)
            return redirect("dashboard/")
        else:
            messages.info(request, 'Username or password is incorrect. Please try again!')
    
    context = {}
    return redirect("login")


    #if user not found
    #show user not found

def register(request):
    return render(request, "users/register.html")

def user_register(request):
    form = CreateUserForm(request.POST)
    if request.method == "Get":
        return render(request, "users/register.html")
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            
            form.save()
            context = {"registration_message": "User registered successfully"}
            return render(request, "users/login.html", context)
        else:
            messages.info(request, "Username or password is incorrect. Please try again!")
            return render(request, "users/register.html", {"form": form})


def username_validation(request):
    if request.method == "POST":
        username = request.POST.get("username")
        print(f"here is the username: {username}")
        if User.objects.filter(username=username).exists():
            return JsonResponse({"check_status": "Failed"})
            #print("Username is taken")
            #return render(request, "users/register.html", {"check_status": "Failed"})
        else:
            #print("Username is available")
            return JsonResponse({"check_status": "Success"})
            #return render(request, "users/register.html", {"check_status": "Success"})
