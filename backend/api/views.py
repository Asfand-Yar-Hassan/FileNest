from django.http import JsonResponse
from django.shortcuts import render
from .mongo_queries import *
from .storage import *
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.contrib.auth import logout


@csrf_exempt
def signup(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')

            # validate input data
            if not username or not email or not password:
                return JsonResponse({"error": "All fields are required"}, status=400)

            # check if the username already exists
            if get_user(username):
                return JsonResponse({'message': "Username already exists"}, status=400)

            # create user
            user_id = create_user(username, email, password)
            return JsonResponse({"message": f"User successfully created {user_id}"}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def login(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")

            if not username or not password:
                return JsonResponse({"message": "Username and Password required"}, status=400)
            user = verify_user(username, password)
            if user:
                response = JsonResponse(
                    {"message": "user logged in successfully"})
                response.set_cookie("user_id", str(user["_id"]), httponly=True)
                return response
            else:
                return JsonResponse({"error": "Invalid username or password"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def home_page(request):
    """List all files for the user on the home page"""
    if request.method == "GET":
        try:
            user_id = request.user.id
            if user_id:
                files = get_files_by_user(user_id)
                return JsonResponse({"files": files}, status=200, safe=False)
            else:
                return JsonResponse({"message": "please login"})
        except Exception as e:
            return JsonResponse({"error": str(e)})
    else:
        return JsonResponse({"error": "Invalid method"}, status=405)
