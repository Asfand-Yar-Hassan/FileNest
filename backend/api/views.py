from django.http import JsonResponse
from django.shortcuts import render
from .mongo_queries import *
from .storage import *
import json
from django.views.decorators.csrf import csrf_exempt
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


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
            if get_user_by_username(username):
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
            user_id = request.COOKIES.get("user_id")
            if user_id:
                files = get_files_by_user(user_id)
                return JsonResponse({"files": files}, status=200, safe=False)
            else:
                return JsonResponse({"message": "please login"})
        except Exception as e:
            return JsonResponse({"error": str(e)})
    else:
        return JsonResponse({"error": "Invalid method"}, status=405)


@csrf_exempt
def logout_view(request):
    if request.method == "POST":
        try:
            if request.COOKIES.get("user_id"):
                response = JsonResponse({"message": "User logged out"})
                response.delete_cookie("user_id")
                return response
            else:
                return JsonResponse({"message": "User not logged in"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def file_upload_view(request):
    if request.method == "POST":
        try:
            # Validate user session
            user_id = request.COOKIES.get("user_id")
            if not user_id:
                return JsonResponse({"message": "User needs to be logged in"}, status=401)

            # Validate uploaded file
            uploaded_file = request.FILES.get("file")
            if not uploaded_file:
                return JsonResponse({"message": "File is required"}, status=400)

            # Read the file as bytes (no need to save it to disk)
            file_data = uploaded_file.read()

            # Upload file directly to MinIO
            file_url = upload_file(user_id, uploaded_file.name, file_data)
            if file_url:
                return JsonResponse({"message": f"File uploaded successfully"}, status=201)
            else:
                return JsonResponse({"message": "Failed to upload file"}, status=500)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def delete_file_view(request):
    if request.method == "DELETE":
        try:
            user_id = request.COOKIES.get("user_id")
            if not user_id:
                return JsonResponse({"message": "User needs to be logged in"}, status=401)
            file_name = request.GET.get("filename")
            if not file_name:
                return JsonResponse({"message": "Please specify the file name"}, status=401)
            delete_file(user_id, file_name)
            return JsonResponse({"message": "File successfully deleted"}, status=200)
        except Exception as e:
            return JsonResponse({"message": str(e)})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
