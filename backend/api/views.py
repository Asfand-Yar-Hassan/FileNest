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
            if request.COOKIES.get("user_id"):
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


# @csrf_exempt
# def file_upload_view(request):
#     if request.method == "POST":
#         try:
#             # Validate user session
#             user_id = request.COOKIES.get("user_id")
#             if not user_id:
#                 return JsonResponse({"message": "User needs to be logged in"}, status=401)

#             username = request.POST.get("username")
#             if not username:
#                 return JsonResponse({"message": "Username is required"}, status=400)

#             # Validate uploaded file
#             uploaded_file = request.FILES.get("file")
#             if not uploaded_file:
#                 return JsonResponse({"message": "File is required"}, status=400)

#             # Optional: Check file size (example: 10 MB max)
#             max_file_size = 10 * 1024 * 1024  # 10 MB
#             if uploaded_file.size > max_file_size:
#                 return JsonResponse({"message": "File size exceeds the maximum limit (10 MB)"}, status=413)

#             # Ensure temporary directory exists
#             temp_dir = Path(settings.BASE_DIR) / 'temp'
#             temp_dir.mkdir(parents=True, exist_ok=True)

#             # Save file to the temporary location
#             temp_file_path = temp_dir / uploaded_file.name
#             with temp_file_path.open('wb') as temp_file:
#                 for chunk in uploaded_file.chunks():
#                     temp_file.write(chunk)

#             # Upload file to MinIO
#             file_url = upload_file(username, str(temp_file_path))
#             if file_url:
#                 # Remove the temporary file after upload
#                 temp_file_path.unlink()
#                 return JsonResponse({"message": f"File uploaded successfully: {file_url}"}, status=201)
#             else:
#                 # Log the failure and return a generic error message
#                 logger.error(f"Failed to upload file for user {username}.")
#                 return JsonResponse({"message": "Failed to upload file"}, status=500)

#         except Exception as e:
#             logger.error(f"Error during file upload: {str(e)}")
#             return JsonResponse({"error": str(e)}, status=500)

#         finally:
#             # Ensure temporary file is deleted even in case of an error
#             if temp_file_path.exists():
#                 temp_file_path.unlink()

#     else:
#         return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def file_upload_view(request):
    if request.method == "POST":
        try:
            # Validate user session
            user_id = request.COOKIES.get("user_id")
            if not user_id:
                return JsonResponse({"message": "User needs to be logged in"}, status=401)

            username = request.POST.get("username")
            if not username:
                return JsonResponse({"message": "Username is required"}, status=400)

            # Validate uploaded file
            uploaded_file = request.FILES.get("file")
            if not uploaded_file:
                return JsonResponse({"message": "File is required"}, status=400)

            # Read the file as bytes (no need to save it to disk)
            file_data = uploaded_file.read()

            # Upload file directly to MinIO
            file_url = upload_file(username, uploaded_file.name, file_data)
            if file_url:
                return JsonResponse({"message": f"File uploaded successfully"}, status=201)
            else:
                return JsonResponse({"message": "Failed to upload file"}, status=500)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
