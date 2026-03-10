from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
import json
from django.contrib.auth.hashers import check_password
from ..models import User 
from rest_framework_simplejwt.tokens import RefreshToken
# live
def login_panel(request):
    return render(request,'login.html')


def registration(request):
    return render(request,'register.html')


@csrf_exempt
def create_login_api(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.filter(email=email).first()
        if user:
            if user.shadow_pass == password:
                login(request, user)
                User.objects.filter(username=user.username).update(is_loggedin=True)
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                if user.user_level == 1:
                    return JsonResponse({"status": 200, "message": "User login successful", "user_id": user.id,"token": access_token})
                elif user.user_level == 9:
                    return JsonResponse({"status": 201, "message": "Admin login successful", "user_id": user.id,"token": access_token})
                else:
                    return JsonResponse({"status": 'success', "message": "Login successful, but no specific redirect."})
            else:
                return JsonResponse({'status':400,'message': 'Incorrect password!'})
        else:
            return JsonResponse({'status':404,'message': 'email does not exist!'})

    return JsonResponse({'message': 'Invalid request method'}, status=400)



@csrf_exempt
def logout_user(request):
    # if request.method == 'POST':
    if request.method in ['POST', 'GET']:
        if request.user.is_authenticated:
            logout(request)
            return JsonResponse({'message': 'Successfully logged out.'}, status=200)
        else:
            return JsonResponse({'error': 'User is not authenticated.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)
    


@csrf_exempt
def change_password(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            old_password = data.get('old_password')
            new_password = data.get('new_password')
            confirm_password = data.get('confirm_password')
            if not request.user.is_authenticated:
                return JsonResponse({'status':401,'message': 'User is not authenticated.'})
            if not old_password or not new_password or not confirm_password:
                return JsonResponse({'status':406,'message': 'Please provide old password, new password, and confirm password.'})

            if new_password != confirm_password:
                return JsonResponse({'status':400,'message': 'New password and confirm password do not match.'})
            user = request.user
            if not user.check_password(old_password):
                return JsonResponse({'status':402,'message': 'Old password is incorrect.'})
            if old_password == new_password:
                return JsonResponse({'status':301,'message': 'New password cannot be the same as the old password.'})
            user.shadow_pass = new_password
            user.set_password(new_password)
            user.save()
            return JsonResponse({'status':200,'message': 'Password changed successfully.'})
        except json.JSONDecodeError:
            return JsonResponse({'status':422,'message': 'Invalid JSON. Please provide a valid JSON request body.'})
        except Exception as e:
            return JsonResponse({'status':500,'message': f'An unexpected error occurred: {str(e)}'})

    return JsonResponse({'status':405,'message': 'Method not allowed. Please use POST.'})

@csrf_exempt
def check_user_logged_in(request):
    if request.user.is_authenticated:
        return JsonResponse({"logged_in": True, "username": request.user.username})
    else:
        return JsonResponse({"logged_in": False})