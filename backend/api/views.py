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
def test(request) -> JsonResponse:
    if request.method == "GET":
        return JsonResponse({"message": "Backend is working!"}, status=200)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


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

            # Return token in response
            return JsonResponse({
                "message": "User successfully created",
                "token": str(user_id)
            }, status=201)
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
                return JsonResponse({
                    "message": "User logged in successfully",
                    "token": str(user["_id"])
                })
            else:
                return JsonResponse({"error": "Invalid username or password"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def dashboard(request):
    """List all files for the user on the home page"""
    if request.method == "GET":
        try:
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return JsonResponse({"message": "Invalid authorization header"}, status=401)

            token = auth_header.split(' ')[1]
            if token:
                files = get_files_by_user(token)
                return JsonResponse({"files": files}, status=200, safe=False)
            else:
                return JsonResponse({"message": "Please login"}, status=401)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=401)
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
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return JsonResponse({"message": "Invalid authorization header"}, status=401)

            token = auth_header.split(' ')[1]
            if not token:
                return JsonResponse({"message": "User needs to be logged in"}, status=401)

            # Validate uploaded file
            uploaded_file = request.FILES.get("file")
            if not uploaded_file:
                return JsonResponse({"message": "File is required"}, status=400)

            # Read the file as bytes (no need to save it to disk)
            file_data = uploaded_file.read()

            # Upload file directly to MinIO
            file_url = upload_file(token, uploaded_file.name, file_data)
            if file_url:
                return JsonResponse({"message": "File uploaded successfully"}, status=201)
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
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return JsonResponse({"message": "Invalid authorization header"}, status=401)

            token = auth_header.split(' ')[1]
            if not token:
                return JsonResponse({"message": "User needs to be logged in"}, status=401)

            data = json.loads(request.body)
            file_id = data.get('file_id')
            if not file_id:
                return JsonResponse({"message": "Please specify the file ID"}, status=400)

            delete_file(token, file_id)
            return JsonResponse({"message": "File successfully deleted"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
