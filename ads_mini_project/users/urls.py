from django.urls import path
from . import views
from django.urls import include

urlpatterns = [
    path("", views.index, name="login"),
    path("login", views.index, name="login"),
    path("user_login", views.user_login, name="user_login"),
    path("register", views.register, name="register"),
    path("user_register", views.user_register, name="user_register"),
    path("username_validation", views.username_validation, name="username_validation"),
    
    #include the dashboard urls from dashboard app
    path("dashboard", include("dashboard.urls")),
    
]
