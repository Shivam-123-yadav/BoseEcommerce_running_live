import random
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils.timezone import now
from django.contrib.auth import update_session_auth_hash
from ..models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import make_password
# live
User = get_user_model()

@csrf_exempt
def send_otp(request):
    """
    API to send OTP to the email with an HTML message.
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')

        try:
            user = User.objects.get(email=email)
            otp = f"{random.randint(1000, 9999)}"
            user.otp = otp
            user.otp_created_at = datetime.now()
            user.save()
            from_email = 'sales@boseservicecenter.co.in'
            subject = 'Your OTP for Password Reset'
            recipient_list = [email]
            message_html = f"""
            <html>
                <body>
                    <p>Dear {user.username},</p>
                    <p>Your OTP for password reset is:</p>
                    <h2>{otp}</h2>
                    <p>This OTP is valid for 10 minutes.</p>
                    <p>If you didn't request this, please ignore this email.</p>
                </body>
            </html>
            """
            send_mail(
                subject=subject,
                message='', 
                from_email=from_email,
                recipient_list=recipient_list,
                html_message=message_html 
            )
            return JsonResponse({'message': 'OTP sent to your email.'}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User with this email does not exist.'}, status=404)


@csrf_exempt
def verify_otp(request):
    """
    API to verify OTP with a 1-minute expiration time, only checking expiration.
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        otp = data.get('otp')

        try:
            user = User.objects.get(email=email)
            if user.otp != otp:
                return JsonResponse({'error': 'Invalid OTP.'}, status=400)
            time_diff = now() - user.otp_created_at
            if time_diff.total_seconds() > 60:
                return JsonResponse({'error': 'OTP has expired.'}, status=400)
            return JsonResponse({'message': 'OTP verified successfully.'}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User with this email does not exist.'}, status=404)



@csrf_exempt
def reset_password(request):
    """
    API to reset the password if OTP is verified.
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        if new_password != confirm_password:
            return JsonResponse({'error': 'Passwords do not match.'}, status=400)
        if not isinstance(new_password, str):
            return JsonResponse({'error': 'Password must be a string.'}, status=400)
        try:
            user = User.objects.get(email=email)
            if user.otp_created_at and now() - user.otp_created_at > timedelta(minutes=10):
                return JsonResponse({'error': 'OTP expired.'}, status=400)
            user.set_password(new_password) 
            user.shadow_pass = new_password
            user.otp = None 
            user.otp_created_at = None
            user.save()
            update_session_auth_hash(request, user)
            return JsonResponse({'message': 'Password reset successfully.'}, status=200)

        except User.DoesNotExist:
            return JsonResponse({'error': 'Invalid email.'}, status=400)


