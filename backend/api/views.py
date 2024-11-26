from django.http import JsonResponse
from django.shortcuts import render
from .mongo_queries import *
from .storage import *
import json
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


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
