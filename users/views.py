from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.http import JsonResponse
from .services import register_user, login_user

def user_login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        response = login_user(email, password)
        if response["success"]:
            return JsonResponse({"message": "Login successful"})
        return JsonResponse({"message": response["message"]}, status=400)

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("login_page")
