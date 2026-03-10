import json
import logging
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..models import UserDetails
from django.views.decorators.csrf import csrf_exempt
from ..models import *
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.shortcuts import redirect
import requests
from django.conf import settings
import uuid
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from weasyprint import HTML
from io import BytesIO
from django.core.files.storage import FileSystemStorage
from datetime import datetime
from django.utils import timezone 
from django.core.mail import send_mail

# live
#==================>  customer details create code  <=============================


logger = logging.getLogger(__name__)

        
@csrf_exempt
def UserDetailsView(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')

        if not all([first_name,email, phone_number, address, city, state, postal_code]):
            return JsonResponse({"error": "All fields are mandatory"}, status=400)
        
        user_details=UserDetails.objects.create(
            user=request.user,  
            first_name=first_name,
            email=email,
            phone_number=phone_number,
            address=address,
            city=city,
            state=state,
            postal_code=postal_code,
        )
        response_data = {
            "user": user_details.user.username,
            "first_name": user_details.first_name,
            "email": user_details.email,
            "phone_number": user_details.phone_number,
            "address": user_details.address,
            "city": user_details.city,
            "state": user_details.state,
            "postal_code": user_details.postal_code
        }
        return JsonResponse({"message": "User details saved successfully","response_data":response_data}, status=201)
    elif request.method == 'GET':
        try:
            user_details = UserDetails.objects.get(user=request.user)
            response_data = {
                "user": user_details.user.username,
                "first_name": user_details.first_name,
                "email": user_details.email,
                "phone_number": user_details.phone_number,
                "address": user_details.address,
                "city": user_details.city,
                "state": user_details.state,
                "postal_code": user_details.postal_code
            }
            return JsonResponse({"status":200,"response_data": response_data})
        except UserDetails.DoesNotExist:
            return JsonResponse({"error": "User details not found"}, status=404)
    return JsonResponse({'status':404,'message':'not found'})
        
#==================>  customer details update code  <=============================

@csrf_exempt
def userscreations_data(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            try:
                print('Fetching user details...')
                fetchuser_details = get_object_or_404(UserDetails, user=request.user)

                user_details_data = {
                    'first_name': fetchuser_details.first_name,
                    'last_name': fetchuser_details.last_name,
                    'email': fetchuser_details.email,
                    'phone_number': fetchuser_details.phone_number,
                    'address': fetchuser_details.address,
                    'city': fetchuser_details.city,
                    'state': fetchuser_details.state,
                    'postal_code': fetchuser_details.postal_code,
                    'country': fetchuser_details.country,
                }
                
                return JsonResponse({'status': 'success', 'details': user_details_data})
            except Exception as e:
                return JsonResponse({'error': 'Failed to fetch user details'}, status=500)
        
        elif request.method == 'POST':
            try:
                first_name = request.POST.get('first_name')
                email = request.POST.get('email')
                phone_number = request.POST.get('phone_number')
                address = request.POST.get('address')
                city = request.POST.get('city')
                state = request.POST.get('state')
                postal_code = request.POST.get('postal_code')
                fetchuser_details = get_object_or_404(UserDetails, user=request.user)

                fetchuser_details.first_name = first_name
                fetchuser_details.email = email
                fetchuser_details.phone_number = phone_number
                fetchuser_details.address = address
                fetchuser_details.city = city
                fetchuser_details.state = state
                fetchuser_details.postal_code = postal_code
                fetchuser_details.save()
                
                updated_user_details = {
                    'first_name': fetchuser_details.first_name,
                    'last_name': fetchuser_details.last_name,
                    'email': fetchuser_details.email,
                    'phone_number': fetchuser_details.phone_number,
                    'address': fetchuser_details.address,
                    'city': fetchuser_details.city,
                    'state': fetchuser_details.state,
                    'postal_code': fetchuser_details.postal_code,
                    'country': fetchuser_details.country,
                }
                
                return JsonResponse({'status': 'success', 'message': 'User details updated successfully','updated_details': updated_user_details})
            except Exception as e:
                return JsonResponse({'error': 'Failed to update user details'}, status=500)
        else:
            return JsonResponse({'error': 'Invalid request method'}, status=400)
    else:
        return JsonResponse({'error': 'User not authenticated'}, status=401)
    


#==================>Generate payment gatway link <=============================


import uuid
import logging
import re
import requests
import traceback
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from ..models import Cart, Order, OrderItem

logger = logging.getLogger(__name__)

cashfree_url = 'https://api.cashfree.com/api/v1/order/create'


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(login_required, name='dispatch')
class BuyProductsView(View):
    def post(self, request, *args, **kwargs):
        try:
            # Delete existing pending order
            existing_order = Order.objects.filter(user=request.user, payment_status='pending').first()
            if existing_order:
                existing_order.delete()

            cart = Cart.objects.filter(user=request.user).first()
            if not cart or not cart.cart_items.exists():
                return JsonResponse({'status': 'error', 'message': 'Your cart is empty. Please add items before placing an order.'}, status=400)

            # Calculate total amount
            total_subtotal = 0
            total_discount = 0
            total_shipping_charge = 0
            for ci in cart.cart_items.all():
                item = ci.item
                total_subtotal += item.mrp_price * ci.quantity
                total_discount += item.discount_amount * ci.quantity
                total_shipping_charge += item.shipping_charges if item.shipping_charges else 0

            total_amount = total_subtotal - total_discount + total_shipping_charge

            # Safe order note using title
            order_note = ", ".join([getattr(ci.item, 'title', str(ci.item.id)) for ci in cart.cart_items.all()])[:100]

            order_id = f"order_{uuid.uuid4()}"
            order = Order.objects.create(
                order_id=order_id,
                user=request.user,
                total_amount=total_amount,
                payment_status='pending',
                order_note=order_note,
                payment_link='',
            )

            for ci in cart.cart_items.all():
                OrderItem.objects.create(
                    order=order,
                    item=ci.item,
                    quantity=ci.quantity,
                    total_price=(ci.item.final_price or 0) * ci.quantity,
                    type_color_name=getattr(ci, 'type_color_name', ''),
                    type_color_image_url=getattr(ci, 'type_color_image_url', ''),
                )

            user_details = getattr(request.user, 'user_details', None)
            if not user_details:
                return JsonResponse({'status': 'error', 'message': 'Please add billing details'}, status=400)

            payment_data = {
                "appId": settings.CASHFREE_CLIENT_ID,
                "secretKey": settings.CASHFREE_SECRET_KEY,
                "orderId": order_id,
                "orderAmount": str(total_amount),
                "orderCurrency": "INR",
                "customerName": getattr(user_details, 'first_name', request.user.username),
                "customerEmail": getattr(user_details, 'email', request.user.email),
                "customerPhone": getattr(user_details, 'phone_number', ''),
                "orderNote": order_note,
                "returnUrl": "https://www.boseservicecenter.co.in/order_confirmation_response",
                "notifyUrl": ""
            }

            response = requests.post(
                cashfree_url,
                data=payment_data,
                headers={
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'x-client-id': settings.CASHFREE_CLIENT_ID,
                    'x-client-secret': settings.CASHFREE_SECRET_KEY,
                }
            )

            try:
                response_data = response.json()
            except Exception:
                logger.error("Invalid JSON from Cashfree: %s", response.text)
                return JsonResponse({'status': 'error', 'message': 'Invalid JSON from Cashfree'}, status=500)

            if response.status_code == 200 and response_data.get('paymentLink'):
                order.payment_link = response_data['paymentLink']
                order.save()
                return JsonResponse({'status': 'success', 'payment_link': response_data['paymentLink']}, status=200)
            else:
                logger.error("Failed to create payment link: %s", response_data)
                return JsonResponse({'status': 'error', 'message': 'Failed to create payment link.'}, status=500)

        except Exception:
            logger.error("Error in BuyProductsView:\n%s", traceback.format_exc())
            return JsonResponse({'status': 'error', 'message': 'An error occurred while processing your order. Please try again later.'}, status=500)


#==================>Fetch cashfree details <=============================


# def get_request_data(request, key):
#     return request.GET.get(key) or request.POST.get(key)


# @csrf_exempt
# def payment_returns(request):
#     print(request.POST,'========POSTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT')
#     if request.method not in ["POST", "GET"]:
#         return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)
    
#             # 🔍 Debug prints
#     print("==== CASHFREE PAYMENT CALLBACK ====")
#     print("Request Method:", request.method)
#     print("GET Data:", dict(request.GET))
#     print("POST Data:", dict(request.POST))
#     print("Raw Body:", request.body.decode("utf-8"))
#     print("===================================")

    
#     try:
#         order_id = get_request_data(request, 'orderId')
#         tx_status = get_request_data(request, 'txStatus')
#         payment_mode = get_request_data(request, 'paymentMode')
#         reference_id = get_request_data(request, 'referenceId')
#         signature = get_request_data(request, 'signature')
#         transaction_time = get_request_data(request, 'txTime')

#         if not order_id or not tx_status:
#             return JsonResponse({'status': 'error', 'message': 'Missing required parameters.'}, status=400)
        
#         # if tx_status == 'USER_DROPPED' or tx_status== 'INCOMPLETE':
#         #     return redirect('https://www.boseservicecenter.co.in/chekout_now')

#         if tx_status in ['USER_DROPPED', 'INCOMPLETE', 'FAILED']:
#             try:
#                 order = Order.objects.get(order_id=order_id)
#                 if tx_status == 'USER_DROPPED':
#                     order.status = Order.OrderStatus.USER_DROPPED
#                 elif tx_status == 'INCOMPLETE':
#                     order.status = Order.OrderStatus.INCOMPLETE
#                 elif tx_status == 'FAILED':
#                     order.status = Order.OrderStatus.CANCELLED 
#                     order.payment_status = 'failed' 
#                     if order.user.email:
#                         subject = "Transaction Failed"
#                         message = f"Dear {order.user.username},\n\nYour transaction has failed. Please try again."
#                         from_email = settings.DEFAULT_FROM_EMAIL
#                         recipient_list = [order.user.email]
#                         send_mail(subject, message, from_email, recipient_list)
#                 order.save()
#             except Order.DoesNotExist:
#                 logger.warning(f"Order not found: {order_id}")
#                 return JsonResponse({'status': 'error', 'message': 'Order not found.'}, status=404)
#             return redirect('https://www.boseservicecenter.co.in/chekout_now')
        
        
#         # verify_url = f"https://sandbox.cashfree.com/pg/orders/{order_id}?version=2022-09-01"
#         verify_url = f"https://api.cashfree.com/pg/orders/{order_id}?version=2022-09-01"
#         headers = {
#             "x-client-id": settings.CASHFREE_CLIENT_ID,
#             "x-client-secret": settings.CASHFREE_SECRET_KEY,
#             "x-api-version": "2022-09-01",
#         }

#         try:
#             response = requests.get(verify_url, headers=headers)
#             response_data = response.json()
#         except requests.RequestException as e:
#             logger.error(f"Cashfree API error: {str(e)}")
#             return JsonResponse({'status': 'error', 'message': 'Failed to connect to Cashfree API.'}, status=500)

#         if response.status_code != 200:
#             return JsonResponse({'status': 'error', 'message': 'Failed to verify payment.'}, status=500)
#         try:
#             order = Order.objects.get(order_id=order_id)
#         except Order.DoesNotExist:
#             logger.warning(f"Order not found: {order_id}")
#             return JsonResponse({'status': 'error', 'message': 'Order not found.'}, status=404)

#         cashfree_status = response_data.get('order_status')
#         order.payment_mode = payment_mode
#         order.reference_id = reference_id
#         order.signature = signature
#         order.transaction_time = transaction_time
#         order.payment_status = 'success' if tx_status == 'SUCCESS' and cashfree_status == 'PAID' else 'failed'
#         if tx_status == 'SUCCESS' and cashfree_status == 'PAID':
#             order.status = Order.OrderStatus.PAID
#         order.save()

#         Cart.objects.filter(user=order.user).delete()
#         order_item_instances = order.order_items.all()
#         item_details = [
#             {
#                 'title': order_item.item.title,
#                 'quantity': order_item.quantity,
#                 'final_price': order_item.item.final_price,  
#                 # 'color_name': order_item.type_color_name,  # Add color name
#                 # 'color_name': order_item.type_color_name.replace("-", " ").title(),  # Add color name
#                 'color_name': (order_item.type_color_name.replace("-", " ").title() if order_item.type_color_name else "N/A"),

#                 'color_image_url': order_item.type_color_image_url,  # Add color image URL
#             }
#             for order_item in order_item_instances
#         ]

#         order_item_instance = None
#         if order.order_items.exists():
#             order_item_instance = order.order_items.first()

#         payment_status, created = paymentStatus.objects.update_or_create(
#             order=order,
#             order_item=order_item_instance,
#             defaults={
#                 'user': order.user,
#                 'amount': order.total_amount,
#                 'status': order.payment_status,
#                 'transaction_id': reference_id, 
#                 'customer_name': order.user.user_details.first_name,
#                 'customer_email': order.user.user_details.email,
#                 'customer_phone': order.user.user_details.phone_number,
#                 'customer_address': order.user.user_details.address,
#                 'gateway_response': response_data,
#             }
#         )

#         if isinstance(order.transaction_time, str):
#             try:
#                 timestamp = datetime.strptime(order.transaction_time, "%Y-%m-%d %H:%M:%S")
#                 print(timestamp,'timestamp===============================================')
#             except ValueError:
#                 logger.error(f"Failed to parse transaction_time: {order.transaction_time}")
#                 return JsonResponse({'status': 'error', 'message': 'Invalid transaction time format'}, status=400)
#         else:
#             timestamp = order.transaction_time
#         if timestamp.tzinfo is None:
#             timestamp = timezone.make_aware(timestamp)

#         date_only = timestamp
#         pdf_context = {
#             'user': order.user,
#             'amount': order.total_amount,
#             'status': order.payment_status,
#             'transaction_id': reference_id,
#             'customer_name': order.user.user_details.first_name,
#             'customer_email': order.user.user_details.email,
#             'customer_phone': order.user.user_details.phone_number,
#             'customer_address': order.user.user_details.address,
#             'customer_state': order.user.user_details.state,
#             'customer_city': order.user.user_details.city,
#             'customer_zipcode': order.user.user_details.postal_code,
#             'gateway_response': response_data,
#             "payment_mode":order.payment_mode,
#             "transaction_date": date_only,
#             "item_details":item_details,
#         }



def get_request_data(request, key):
    return request.GET.get(key) or request.POST.get(key)

@csrf_exempt
def payment_returns(request):
    if request.method not in ["POST", "GET"]:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)
    
    print("==== CASHFREE PAYMENT CALLBACK ====")
    print("Request Method:", request.method)
    print("GET Data:", dict(request.GET))
    print("POST Data:", dict(request.POST))
    print("Raw Body:", request.body.decode("utf-8"))
    print("===================================")

    try:
        order_id = get_request_data(request, 'orderId')
        tx_status = get_request_data(request, 'txStatus')
        payment_mode = get_request_data(request, 'paymentMode')
        reference_id = get_request_data(request, 'referenceId')
        signature = get_request_data(request, 'signature')
        transaction_time = get_request_data(request, 'txTime')

        if not order_id or not tx_status:
            return JsonResponse({'status': 'error', 'message': 'Missing required parameters.'}, status=400)

        if tx_status in ['USER_DROPPED', 'INCOMPLETE', 'FAILED']:
            try:
                order = Order.objects.get(order_id=order_id)
                if tx_status == 'USER_DROPPED':
                    order.status = Order.OrderStatus.USER_DROPPED
                elif tx_status == 'INCOMPLETE':
                    order.status = Order.OrderStatus.INCOMPLETE
                elif tx_status == 'FAILED':
                    order.status = Order.OrderStatus.CANCELLED 
                    order.payment_status = 'failed'
                    if order.user.email:
                        subject = "Transaction Failed"
                        message = f"Dear {order.user.username},\n\nYour transaction has failed. Please try again."
                        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [order.user.email])
                order.save()
            except Order.DoesNotExist:
                logger.warning(f"Order not found: {order_id}")
                return JsonResponse({'status': 'error', 'message': 'Order not found.'}, status=404)
            return redirect('https://www.boseservicecenter.co.in/chekout_now')

        # VERIFY WITH CASHFREE
        verify_url = f"https://api.cashfree.com/pg/orders/{order_id}?version=2022-09-01"
        headers = {
            "x-client-id": settings.CASHFREE_CLIENT_ID,
            "x-client-secret": settings.CASHFREE_SECRET_KEY,
            "x-api-version": "2022-09-01",
        }

        try:
            response = requests.get(verify_url, headers=headers)
            response_data = response.json()
        except requests.RequestException as e:
            logger.error(f"Cashfree API error: {str(e)}")
            return JsonResponse({'status': 'error', 'message': 'Failed to connect to Cashfree API.'}, status=500)

        if response.status_code != 200:
            return JsonResponse({'status': 'error', 'message': 'Failed to verify payment.'}, status=500)

        try:
            order = Order.objects.get(order_id=order_id)
        except Order.DoesNotExist:
            logger.warning(f"Order not found: {order_id}")
            return JsonResponse({'status': 'error', 'message': 'Order not found.'}, status=404)

        cashfree_status = response_data.get('order_status')
        order.payment_mode = payment_mode
        order.reference_id = reference_id
        order.signature = signature
        order.transaction_time = transaction_time
        order.payment_status = 'success' if tx_status == 'SUCCESS' and cashfree_status == 'PAID' else 'failed'
        if tx_status == 'SUCCESS' and cashfree_status == 'PAID':
            order.status = Order.OrderStatus.PAID
        order.save()

        Cart.objects.filter(user=order.user).delete()
        order_items = order.order_items.all()
        item_details = [
            {
                'title': item.item.title,
                'quantity': item.quantity,
                'final_price': item.item.final_price,
                'color_name': item.type_color_name.replace("-", " ").title() if item.type_color_name else "N/A",
                'color_image_url': item.type_color_image_url,
            } for item in order_items
        ]

        order_item_instance = order_items.first() if order_items.exists() else None
        user_details = getattr(order.user, 'user_details', None)

        paymentStatus.objects.update_or_create(
            order=order,
            order_item=order_item_instance,
            defaults={
                'user': order.user,
                'amount': order.total_amount,
                'status': order.payment_status,
                'transaction_id': reference_id,
                'customer_name': getattr(user_details, 'first_name', 'N/A'),
                'customer_email': getattr(user_details, 'email', 'N/A'),
                'customer_phone': getattr(user_details, 'phone_number', 'N/A'),
                'customer_address': getattr(user_details, 'address', 'N/A'),
                'gateway_response': response_data,
            }
        )

        # Format time
        if isinstance(order.transaction_time, str):
            try:
                timestamp = datetime.strptime(order.transaction_time, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                logger.error(f"Invalid transaction time format: {order.transaction_time}")
                return JsonResponse({'status': 'error', 'message': 'Invalid transaction time format'}, status=400)
        else:
            timestamp = order.transaction_time

        if timestamp.tzinfo is None:
            timestamp = timezone.make_aware(timestamp)

        date_only = timestamp

        # PDF Context
        pdf_context = {
            'user': order.user,
            'amount': order.total_amount,
            'status': order.payment_status,
            'transaction_id': reference_id,
            'customer_name': getattr(user_details, 'first_name', 'N/A'),
            'customer_email': getattr(user_details, 'email', 'N/A'),
            'customer_phone': getattr(user_details, 'phone_number', 'N/A'),
            'customer_address': getattr(user_details, 'address', 'N/A'),
            'customer_state': getattr(user_details, 'state', ''),
            'customer_city': getattr(user_details, 'city', ''),
            'customer_zipcode': getattr(user_details, 'postal_code', ''),
            "payment_mode": order.payment_mode,
            "transaction_date": date_only,
            "item_details": item_details,
        }


        pdf_html = render_to_string('bill-pdf.html', pdf_context)
        pdf_file = HTML(string=pdf_html).write_pdf()

        try:
            email_subject = "Payment Success - Order Confirmation"
            # email_body = f"Dear {order.user.user_details.first_name},\n\nYour payment was successful. Please find the order confirmation attached."
            email_body = f"""
<html>
<body style="margin: 0px; padding: 0px; box-sizing: border-box; font-family: Arial, sans-serif;  color: #000;">

<div style="padding: 20px; max-width: 600px; margin: 0; background-color: #e3e3e3; color: #000; border: 1px solid #444; border-radius: 8px;">
    <a href="https://www.boseservicecenter.co.in/products-category?filter=portablebluetooth"><img src="https://www.boseservicecenter.co.in/static/images/mail-banner-buynow.jpg" style="width: 100%; height: auto; margin-bottom: 20px;"></a>
    <p style="font-size: 16px; color: #000;">Dear {order.user.user_details.first_name},</p>
    <p style="font-size: 14px; color: #000;">Your payment has been successfully processed. We are now preparing your order. You will receive a confirmation email shortly.</p>

    <!-- Billing Address Section -->
    <table cellpadding="3" cellspacing="5" style="width: 100%; background-color:#f2f2f2; margin-bottom: 10px; padding: 10px; border-radius: 8px; border-collapse: collapse;">
        <tr>
            <td colspan="2" style="color: #ffffff;font-weight: bold;border-bottom: 1px solid #444;padding: 10px;background: #5a5a68;border-radius: 10px 10px 0px 0px;">Billing Address</td>
        </tr>
        <tr>
            <td style="color: #000; padding: 10px;">Name:</td>
            <td style="color: #000; padding: 10px;">{order.user.user_details.first_name or "-"}</td>
        </tr>
        <tr>
            <td style="color: #000; padding: 10px;">Address:</td>
            <td style="color: #000; padding: 10px;">{order.user.user_details.address or "-"}</td>
        </tr>
        <tr>
            <td style="color: #000; padding: 10px;">State:</td>
            <td style="color: #000; padding: 10px;">{order.user.user_details.state or "-"}</td>
        </tr>
        <tr>
            <td style="color: #000; padding: 10px;">City:</td>
            <td style="color: #000; padding: 10px;">{order.user.user_details.city or "-"}</td>
        </tr>
        <tr>
            <td style="color: #000; padding: 10px;">Zip Code:</td>
            <td style="color: #000; padding: 10px;">{order.user.user_details.postal_code or "-"}</td>
        </tr>
    </table>

    <!-- Customer Information Section -->
    <table cellpadding="3" cellspacing="0" style="width: 100%; background-color: #f2f2f2; margin-bottom: 10px; padding: 10px; border-radius: 8px; border-collapse: collapse;">
        <tr>
            <td colspan="2" style="color: #ffffff;font-weight: bold;border-bottom: 1px solid #444;padding: 10px;background: #5a5a68;border-radius: 10px 10px 0px 0px;">Customer Information</td>
        </tr>
        <tr>
            <td style="color: #000; padding: 10px;">Email:</td>
            <td style="color: #000; padding: 10px;">{order.user.user_details.email or "-"}</td>
        </tr>
        <tr>
            <td style="color: #000; padding: 10px;">Mobile Number:</td>
            <td style="color: #000; padding: 10px;">{order.user.user_details.phone_number or "-"}</td>
        </tr>
    </table>

    <!-- Transaction Details Section -->
    <table cellpadding="3" cellspacing="0" style="width: 100%; background-color: #f2f2f2; margin-bottom: 10px; padding: 10px; border-radius: 8px; border-collapse: collapse;">
        <tr>
            <td colspan="2" style="color: #ffffff;font-weight: bold;border-bottom: 1px solid #444;padding: 10px;background: #5a5a68;border-radius: 10px 10px 0px 0px;">Transaction Details</td>
        </tr>
        <tr>
            <td style="color: #000; padding: 10px;">Transaction ID:</td>
            <td style="color: #000; padding: 10px;">{reference_id or "-"}</td>
        </tr>
        <tr>
            <td style="color: #000; padding: 10px;">Transaction Date:</td>
            <td style="color: #000; padding: 10px;">{date_only or "-"}</td>
        </tr>
        <tr>
            <td style="color: #000; padding: 10px;">Payment Method:</td>
            <td style="color: #000; padding: 10px;">{order.payment_mode or "-"}</td>
        </tr>
    </table>

    <!-- Product Details Section -->
    <table cellpadding="3" cellspacing="0" style="width: 100%; background-color: #f2f2f2; margin-bottom: 10px; padding: 10px; border-radius: 8px; border-collapse: collapse;">
        <tr>
            <td colspan="5" style="color: #ffffff;font-weight: bold;border-bottom: 1px solid #444;padding: 10px;background: #5a5a68;border-radius: 10px 10px 0px 0px;">Product Details</td>
        </tr>
        <tr>
            <th style="color: #000; text-align: left; padding: 10px;">Product Name</th>
            <th style="color: #000; text-align: left; padding: 10px;">Color</th>
            <th style="color: #000; text-align: left; padding: 10px;">Quantity</th>
            <th style="color: #000; text-align: left; padding: 10px;">Price</th>
            <th style="color: #000; text-align: left; padding: 10px;">Total</th>
        </tr>
"""

            for item in item_details:
                email_body += f"""
        <tr>
            <td style="color: #000; padding: 10px;">{item['title'] or "-"}</td>
            <td style="color: #000; padding: 10px;">{item['color_name'] or "-"}</td>
            <td style="color: #000; padding: 10px;">{item['quantity'] or "-"}</td>
            <td style="color: #000; padding: 10px;">₹{item['final_price'] or "-"}</td>
            <td style="color: #000; padding: 10px;">₹{item['quantity'] * item['final_price'] if item['final_price'] else "-"}</td>
        </tr>
    """

            email_body += f"""
        <tr>
            <td colspan="4" style="color: #000; text-align: right; padding: 10px; font-weight: bold;">Grand Total:</td>
            <td style="color: #000; padding: 10px;">₹{order.total_amount or "-"}</td>
        </tr>
    </table>

    <p style="font-size: 14px; color: #000;">If you have any questions or need assistance, please contact us at:</p>
    <p style="font-size: 14px; color: #000;">
        <a href="mailto:sales@boseservicecenter.co.in" style="color: #000;">sales@boseservicecenter.co.in</a> |
        Whatsapp: <a href="https://wa.me/919987223322?text=Hello%2C%20Required%20Assistance%20for%20Bose%20Products" target="_blank" style="color: #000;">9987223322</a>
    </p>

    <p style="font-size: 14px; color: #000;">Best regards,<br>
Bose Service Center. (3rd Party Sales & Services).</p>

</div>
</body>
</html>
"""

            to_email = [order.user.user_details.email]
            email = EmailMessage(
                email_subject, email_body, settings.DEFAULT_FROM_EMAIL, to=to_email, 
                # bcc=['klickinfosys@gmail.com','sales@boseservicecenter.co.in'],
                bcc=[
                    # '"Bose Support" <klickinfosys@gmail.com>', 
                    '"Bose Support" <sales@boseservicecenter.co.in>',
                    '"Bose Support" <bapu44@gmail.com>'
                ], 
            )
            email.attach('payment_confirmation.pdf', pdf_file, 'application/pdf')
            email.content_subtype = "html"
            email.send()
        except Exception as email_error:
            logger.error(f"Failed to send email: {str(email_error)}")
            return JsonResponse({'status': 'error', 'message': 'Payment successful but failed to send email.'}, status=500)

        return render(request, "payment_success.html", {"order": order, "response": response_data})

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)




# get user details
@login_required
def get_profile(request):
    user = request.user
    profile_data = {
        "userid":user.id,
        'username':user.username,
        'full_name': f"{user.first_name}",
        'address': user.address,
        'mobile': user.mobile,
        'email': user.email,
        'state': user.state,
        'city': user.city,
        'postal_code': user.postal_code,
    }
    return JsonResponse(profile_data)


@csrf_exempt
def update_profile(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'message': 'You must be logged in to update your profile.'}, status=401)

        user = request.user 
        full_name = request.POST.get('full_name', None)
        address = request.POST.get('address', None)
        mobile = request.POST.get('mobile', None)
        email = request.POST.get('email', None)
        state = request.POST.get('state', None)
        city = request.POST.get('city', None)
        postal_code = request.POST.get('postal_code', None)

        try:
            if full_name is not None:
                user.first_name = full_name
            if address is not None:
                user.address = address
            if mobile is not None:
                user.mobile = mobile
            if email is not None:
                user.email = email
            if state is not None:
                user.state = state
            if city is not None:
                user.city = city
            if postal_code is not None:
                user.postal_code = postal_code
            user.save()

            return JsonResponse({
                'status': 200,
                'message': 'Profile updated successfully',
                'id': user.id,
                'full_name': user.first_name,
                'address': user.address,
                'mobile': user.mobile,
                'email': user.email,
                'state': user.state,
                'city': user.city,
                'postal_code': user.postal_code
            })

        except ValidationError as e:
            return JsonResponse({'message': str(e), 'status': 'failed'}, status=400)
        except Exception as e:
            return JsonResponse({'message': f"An error occurred: {str(e)}", 'status': 'failed'}, status=500)

    elif request.method == 'GET':
        if not request.user.is_authenticated:
            return JsonResponse({'message': 'You must be logged in to view your profile.'}, status=401)

        user = request.user
        return JsonResponse({
            'status': 200,
            'full_name': user.first_name,
            "id": user.id,
            'address': user.address,
            'mobile': user.mobile,
            'email': user.email,
            'state': user.state,
            'city': user.city,
            'postal_code': user.postal_code
        })

    return JsonResponse({'message': 'Invalid request method. Please use GET or POST.', 'status': 'failed'}, status=405)


@csrf_exempt
def userAccountDelete(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'message': 'You must be logged in to delete your account.'}, status=401)
    
        if request.user.user_level == 9:
            return JsonResponse({'message': 'You cannot delete your account with user level 9.'}, status=403)
        try:
            user = request.user
            user.delete()
            return JsonResponse({'message': 'Your account has been successfully deleted.'}, status=200)
        
        except Exception as e:
            return JsonResponse({'message': f'Error deleting account: {str(e)}'}, status=500)

    return JsonResponse({'message': 'Invalid request method. Only POST is allowed.'}, status=405)

@csrf_exempt
def check_login(request):
    """
    Check if the user is logged in and return the user information in JSON format.
    If not logged in, return an error message.
    """
    if request.user.is_authenticated:
        return JsonResponse({
            'status': 'success',
            'message': 'User is logged in',
            'user': {
                'id': request.user.id,
                'username': request.user.username,
                'email': request.user.email
            }
        }, status=200)
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'User is not logged in'
        }, status=401)
    

@csrf_exempt
def check_user_login(request):
    if request.user.is_authenticated:
        user_data = {
            'user_id': request.user.id,
            'username': request.user.username,
            'email': request.user.email,
            'is_logged_in': True
        }
        return JsonResponse({'status': 'success', 'user_data': user_data})
    else:
        return JsonResponse({'status': 'failure', 'message': 'User not logged in'})