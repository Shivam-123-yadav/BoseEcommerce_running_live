
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.html import format_html
from ..models import *

# live

@csrf_exempt
def create_registration(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        username=request.POST.get('username')
        lastname = request.POST.get('last_name')
        email = request.POST.get('email')
        password=request.POST.get('password')
        shadow_pass=password
        if not first_name or not lastname or not email or not password:
            return JsonResponse({'status':404,'message':'all field is required'})
        
        User = get_user_model()
        if User.objects.filter(email=email).exists():
            return JsonResponse({'status': 409, 'message': 'Email already exists'}, status=409)
        
        try:
            user=User.objects.create(username=username,first_name=first_name,user_level=1,
                                     last_name=lastname,email=email,
                                     password=make_password(password),shadow_pass=shadow_pass)
            user.save()

            main_url = 'https://www.boseservicecenter.co.in/login'

            subject = 'Welcome to Our Platform'
            message_html = format_html(
                f"""
                <p>Hi {first_name},</p>
                <p>Thank you for registering with us!</p>
                <p>Please click <a href="{main_url}" target="_blank">https://www.boseservicecenter.co.in/login</a> to login to our website.</p>
                <p>If you didn't request this registration, please ignore this email.</p>
                """
            )
            from_email = 'sales@boseservicecenter.co.in'
            recipient_list = [email]

            send_mail(
                subject,
                '', 
                from_email,
                recipient_list,
                html_message=message_html
            )
            return JsonResponse({'status':200,'message': 'Registration created successfully'})
        except Exception as e:
            return JsonResponse({'status': 500, 'message': 'Failed to create user'}, status=500)
        
    return JsonResponse({'status': 405, 'message': 'Method not allowed'}, status=405)



@csrf_exempt
def check_email(request):
    if request.method == 'POST':
        email = request.POST.get('email', None)
        if email:
            if User.objects.filter(email=email).exists():
                return JsonResponse({'status': 200, 'message': 'Email is Already Exists'})
            else:
                return JsonResponse({'status': 201, 'message': 'Email is available'})
        return JsonResponse({'message': 'Please provide an email'}, status=400)
    
@csrf_exempt
def check_username(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        if username:
            if User.objects.filter(username=username).exists():
                return JsonResponse({'status': 200, 'message': 'Username is Already Exists'})
            else:
                return JsonResponse({'status': 201, 'message': 'Username is Available'})
        return JsonResponse({'message': 'Please provide a username'}, status=400)