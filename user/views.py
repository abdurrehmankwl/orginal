from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import json

User = get_user_model()

@csrf_exempt  
def signup_users(request):
    if request.method == "GET":
        return render(request , "signup.html")

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            username = data.get("username")
            password = data.get("password")

            if not email or not username or not password:
                return JsonResponse({"error": "Email, username, and password are required"}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({"error": "Email already exists"}, status=400)

            if User.objects.filter(username=username).exists():
                return JsonResponse({"error": "Username already exists"}, status=400)

            user = User(email=email, username=username)
            user.set_password(password) 
            user.save()

            return JsonResponse({
                    "message": "user created successfully",
                    "user": {
                        "username": user.username,
                        "email": user.email,
                        "id": user.id
                    }
                }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def login_users(request):
    if request.method == "GET":
        return JsonResponse({"user": "123"}, status=200)

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")  
            password = data.get("password")

            if not username or not password:
                return JsonResponse({"error": "Username and password are required"}, status=400)

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                request.session.set_expiry(86400)  # 24 hours
                return JsonResponse({
                    "message": "Login successful",
                    "user": {
                        "username": user.username,
                        "email": user.email,
                        "id": user.id,
                        "is_authenticated": True
                    }
                }, status=200)
            else:
                return JsonResponse({"error": "Invalid username or password"}, status=401)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
@login_required 
def curr_user(request):
    try:
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({"error": "User not authenticated"}, status=401)
            
        user_data = {
            "email": user.email,
            "username": user.username,
            "id": user.id,
            "is_authenticated": user.is_authenticated
        }
        return JsonResponse({"user": user_data}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
def logout_users(request):
    if request.user.is_authenticated:
        logout(request)
        return JsonResponse({"message": "Successfully logged out"}, status=200)
    return JsonResponse({"message": "Not logged in"}, status=200)

@csrf_exempt
@login_required
def change_password(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            old_password = data.get("oldPassword")
            new_password = data.get("newPassword")

            if not old_password or not new_password:
                return JsonResponse({"error": "Old password and new password are required"}, status=400)

            user = request.user
            
            
            if not user.check_password(old_password):
                return JsonResponse({"error": "Current password is incorrect"}, status=400)

            
            if len(new_password) < 8:
                return JsonResponse({"error": "New password must be at least 8 characters long"}, status=400)

            # Set new password
            user.set_password(new_password)
            user.save()

            return JsonResponse({"message": "Password changed successfully"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)