from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import CreateUserForm
from django.contrib.auth.models import User
from django.http import JsonResponse
import base64

# Create your views here.

def index(request):
    return render(request, "users/login.html")

def user_login(request):
    """
    this function is used to check if user inputted username and password is corect and redirect to dashboard page if the user is exists in DB
    """    
    if request.method == "POST":
        context = {}
        print(f"here is the request: {request}")
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        print(user)

        
        if user:
            context['user'] = request.user
            print(request.user)
            login(request, user)
            return redirect(f"dashboard/", context)
        else:
            messages.info(request, 'Username or password is incorrect. Please try again!')
    
    
    return redirect("login")

def register(request):
    return render(request, "users/register.html")

def user_register(request):
    """
    this function is used to register the user
    """
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
    """
    this function will get the username from request and check if the username exists in database
    """
    if request.method == "POST":
        username = request.POST.get("username")
        if User.objects.filter(username=username).exists():
            return JsonResponse({"check_status": "Failed"})
            #print("Username is taken")
            #return render(request, "users/register.html", {"check_status": "Failed"})
        else:
            #print("Username is available")
            return JsonResponse({"check_status": "Success"})
            #return render(request, "users/register.html", {"check_status": "Success"})
        
def user_logout(request):
    if request.method == "POST":
        logout(request)
        return redirect("login")
