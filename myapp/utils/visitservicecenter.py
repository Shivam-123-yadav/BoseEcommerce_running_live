from django.http import JsonResponse
from ..models import *
from weasyprint import HTML
from django.template.loader import render_to_string
# from django.core.mail import EmailMessage
from django.core.mail import EmailMessage, get_connection
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import logging
import uuid
from django.views import View
from django.utils.decorators import method_decorator
import requests
import logging
from django.http import HttpResponse
import json
from django.shortcuts import render
from datetime import datetime
from django.shortcuts import redirect
from django.db.models import Count


logger = logging.getLogger(__name__)
cashfree_url = 'https://api.cashfree.com/api/v1/order/create'

@csrf_exempt
def offsite_visit(request):
    if request.method=='POST':
        try:
            device_name=request.POST.get('device_name')
            issue_description=request.POST.get("issue_description")
            device_serial_number=request.POST.get("device_serial_number")
            service_center_name=request.POST.get("service_center_name")
            customer_name=request.POST.get("customer_name")
            customer_email=request.POST.get("customer_email")
            customer_mobile=request.POST.get("customer_mobile")
            customer_address=request.POST.get("customer_address")
            visit_type=request.POST.get("visit_type")
            visit_date=request.POST.get("visit_date")
            time_slot=request.POST.get("time_slot")

            if not device_name:
                return JsonResponse({'error': 'Device details are required.'}, status=400)
            
            if not customer_name or not customer_email or not customer_mobile or not customer_address:
                return JsonResponse({'error': 'Customer details are required.'}, status=400)
            
            if not visit_date or not time_slot:
                return JsonResponse({'error': 'Visit details are required.'}, status=400)

            if '@' not in customer_email:
                return JsonResponse({'error': 'Invalid email format.'}, status=400)

            if len(customer_mobile) != 10 or not customer_mobile.isdigit():
                return JsonResponse({'error': 'Invalid mobile number.'}, status=400)

            offsite_visit = OffsiteServiceVisit.objects.create(
                device_name=device_name,
                issue_description=issue_description,
                device_serial_number=device_serial_number,
                service_center_name=service_center_name,
                customer_name=customer_name,
                customer_email=customer_email,
                customer_mobile=customer_mobile,
                customer_address=customer_address,
                visit_type=visit_type,
                visit_date=visit_date,
                time_slot=time_slot
                )
    
            pdf_context = {
                'device_name': device_name,
                'issue_description': issue_description,
                'device_serial_number': device_serial_number,
                'service_center_name': service_center_name,
                'customer_name': customer_name,
                'customer_email': customer_email,
                'customer_mobile': customer_mobile,
                'customer_address': customer_address,
                'visit_type': visit_type,
                'visit_date': visit_date,
                'time_slot': time_slot,
            }

            pdf_html = render_to_string('offsite-visit-pdf.html', pdf_context)
            pdf_file = HTML(string=pdf_html).write_pdf()
            email_subject = "Offsite Service Visit Confirmation"

            email_body = f"""
<html>
<body style="margin: 0px; padding: 0px; box-sizing: border-box; font-family: Arial, sans-serif;  color: #000;">

<div style="padding: 20px; max-width: 600px; margin: 0; background-color: #e3e3e3; color: #000; border: 1px solid #444; border-radius: 8px;">
    <a href="https://www.boseservicecenter.co.in/appointment_form"><img src="https://www.boseservicecenter.co.in/static/images/mail-banner-booknow.jpg" style="width: 100%; height: auto; margin-bottom: 20px;"></a>
    <p style="font-size: 16px; color: #000;">Dear {customer_name},</p>
    <p style="font-size: 14px; color: #000;">Your offsite service visit has been scheduled. Please find the visit confirmation attached.</p>

    <!-- Billing Address Section -->
    <table cellpadding="3" cellspacing="5" style="width: 100%; background-color:#f2f2f2; margin-bottom: 10px; padding: 10px; border-radius: 8px; border-collapse: collapse;">
        <tr>
            <td colspan="2" style="color: #ffffff;font-weight: bold;border-bottom: 1px solid #444;padding: 10px;background: #5a5a68;border-radius: 10px 10px 0px 0px;">Customer Details:</td>
        </tr>
        <tr>
            <td style="color: #000; padding: 10px;">Name:</td>
            <td style="color: #000; padding: 10px;">{customer_name or "-"}</td>
        </tr>
        <tr>
            <td style="color: #000; padding: 10px;">Mobile Number:</td>
            <td style="color: #000; padding: 10px;">{customer_mobile or "-"}</td>
        </tr>
        <tr>
            <td style="color: #000; padding: 10px;">Email:</td>
            <td style="color: #000; padding: 10px;">{customer_email or "-"}</td>
        </tr>
        <tr>
            <td style="color: #000; padding: 10px;">Address:</td>
            <td style="color: #000; padding: 10px;">{customer_address or "-"}</td>
        </tr>
    </table>

    <!-- Customer Information Section -->
    <table cellpadding="3" cellspacing="0" style="width: 100%; background-color: #f2f2f2; margin-bottom: 10px; padding: 10px; border-radius: 8px; border-collapse: collapse;">
        <tr>
            <td colspan="2" style="color: #ffffff;font-weight: bold;border-bottom: 1px solid #444;padding: 10px;background: #5a5a68;border-radius: 10px 10px 0px 0px;">Device Details:</td>
        </tr>
        <tr>
            <td style="color: #000; padding: 10px;">Device Name:</td>
            <td style="color: #000; padding: 10px;">{device_name or "-"}</td>
        </tr>
        <tr>
            <td style="color: #000; padding: 10px;">Issue Description:</td>
            <td style="color: #000; padding: 10px;">{issue_description or "-"}</td>
        </tr>
        <tr>
            <td style="color: #000; padding: 10px;">Serial Number:</td>
            <td style="color: #000; padding: 10px;">{device_serial_number or "-"}</td>
        </tr>
    </table>

    <!-- Transaction Details Section -->
    <table cellpadding="3" cellspacing="0" style="width: 100%; background-color: #f2f2f2; margin-bottom: 10px; padding: 10px; border-radius: 8px; border-collapse: collapse;">
        <tr>
            <td colspan="2" style="color: #ffffff;font-weight: bold;border-bottom: 1px solid #444;padding: 10px;background: #5a5a68;border-radius: 10px 10px 0px 0px;">Service Details:</td>
        </tr>
        <tr>
            <td style="color: #000; padding: 10px;">Store......:</td>
            <td style="color: #000; padding: 10px;">{service_center_name or "-"}</td>
        </tr>
        <tr>
            <td style="color: #000; padding: 10px;">Visit Type:</td>
            <td style="color: #000; padding: 10px;">{visit_type or "-"}</td>
        </tr>
        <tr>
            <td style="color: #000; padding: 10px;">Visit Date:</td>
            <td style="color: #000; padding: 10px;">{visit_date or "-"}</td>
        </tr>
        <tr>
            <td style="color: #000; padding: 10px;">Time Slot:</td>
            <td style="color: #000; padding: 10px;">{time_slot or "-"}</td>
        </tr>
    </table>

        <p style="font-size: 14px; color: #000;">If you have any questions or need assistance, please contact us at:</p>
        <p style="font-size: 14px; color: #000;">
        <a href="mailto:support@boseservicecenter.co.in" style="color: #000;">support@boseservicecenter.co.in</a> |
        Whatsapp: <a href="https://wa.me/919987223322?text=Hello%2C%20Required%20Assistance%20for%20Bose%20Products" target="_blank" style="color: #000;">9987223322</a>
    </p>
    <p style="font-size: 14px; color: #000;">Best regards,<br>Bose Service Center. (3rd Party Sales & Services).</p>
</div>
</body>
</html>
"""






   


#             email_body = f"""
# <html>
# <body style="margin: 0px;
# 	  padding: 0px;
# 	  -webkit-box-sizing: border-box;
# 	  -moz-box-sizing: border-box;
# 	  box-sizing: border-box; color:#fff;overflow:hidden;font-family: var(--font-muli);">

# <div style="padding:10px; display:block; width:100%; background:#222; color:#fff;"><p style="color:#fff;">Dear {customer_name},</p>

# <p style="color:#fff;">Your offsite service visit has been scheduled. Please find the visit confirmation attached.</p>

# <div style="background:#333; margin-bottom:5px; border-bottom:5px #333; padding:10px;"><p style="color:#fff;"><b>Customer Details:</b><br>
# <span style="color:#fff;">---------------------------------</span><br>
# <b style="color:#fff;">Name:</b> <span style="color:#fff;">{customer_name or "-"}</span><br>
# <b style="color:#fff;">Mobile Number:</b> <span style="color:#fff;">{customer_mobile or "-"}</span><br>
# <b style="color:#fff;">Email:</b> <span style="color:#fff;">{customer_email or "-"}</span><br>
# <b style="color:#fff;">Address:</b> <span style="color:#fff;">{customer_address or "-"}</span></p></div>

# <div style="background:#333; margin-bottom:5px; border-bottom:5px #333; padding:10px;">
# <p style="color:#fff;"><b style="color:#fff;">Device Details:</b><br>
# <span style="color:#fff;">---------------------------------</span><br>
# <b style="color:#fff;">Device Name:</b> <span style="color:#fff;">{device_name or "-"}</span><br>
# <b style="color:#fff;">Issue Description:</b> <span style="color:#fff;">{issue_description or "-"}</span><br>
# <b style="color:#fff;">Serial Number:</b> <span style="color:#fff;">{device_serial_number or "-"}</span></p></div>

# <div style="background:#333; margin-bottom:5px; border-bottom:5px #333; padding:10px;">
# <p style="color:#fff;"><b style="color:#fff;">Service Details:</b><br>
# <span style="color:#fff;">---------------------------------</span><br>
# <b style="color:#fff;">Service Center Name:</b> <span style="color:#fff;">{service_center_name or "-"}</span><br>
# <b style="color:#fff;">Visit Type:</b> <span style="color:#fff;">{visit_type or "-"}</span><br>
# <b style="color:#fff;">Visit Date:</b> <span style="color:#fff;">{visit_date or "-"}</span><br>
# <b style="color:#fff;">Time Slot:</b> <span style="color:#fff;">{time_slot or "-"}</span></p></div>


# <div style="background:#333; margin-top:5px;  padding:10px;">
# <p style="color:#fff;">If you have any questions or need to reschedule, please contact us at:<br>
# <a href="mailto:support@boseservicecenter.co.in">support@boseservicecenter.co.in</a> | Whatsapp No. <a href="https://wa.me/919987223322?text=Hello%2C%20Required%20Assistance%20for%20Bose%20Products" class="floatbtn" target="_blank">9987223322</a></p>

# <p style="color:#fff;">Best regards,<br>
# Bose Service Center</p>
# </div>
# </div>
# </body>
# </html>
# """

            connection = get_connection(
                backend=settings.EMAIL_BACKEND_SECONDARY,
                host=settings.EMAIL_HOST_SECONDARY,
                port=settings.EMAIL_PORT_SECONDARY,
                username=settings.EMAIL_HOST_USER_SECONDARY,
                password=settings.EMAIL_HOST_PASSWORD_SECONDARY,
                use_ssl=settings.EMAIL_USE_SSL_SECONDARY,
            )

            to_email = [customer_email]
            email = EmailMessage(
                subject=email_subject,
                body=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL_SECONDARY,
                to=to_email,
                # bcc=['klickinfosys@gmail.com', 'support@boseservicecenter.co.in'],
                bcc=[
                    # '"Bose Support" <klickinfosys@gmail.com>', 
                    '"Bose Support" <support@boseservicecenter.co.in>',
                    '"Bose Support" <bapu44@gmail.com>'
                ], 
                connection=connection,
            )
            email.attach('offsite_visit.pdf', pdf_file, 'application/pdf')
            email.content_subtype = "html"
            email.send()

            return JsonResponse({'status': 200, 'message': 'Offsite service visit scheduled successfully and email sent.'})
        except Exception as email_error:
            logger.error(f"Failed to send email: {str(email_error)}")
            return JsonResponse({'status': 'error', 'message': 'Failed to send email.'}, status=500)
        



@method_decorator(csrf_exempt, name='dispatch')
class onside_visit_appointments(View):
    def post(self, request, *args, **kwargs):
        try:
            device_name=request.POST.get('device_name')
            issue_description=request.POST.get("issue_description")
            device_serial_number=request.POST.get("device_serial_number")
            service_center_name=request.POST.get("service_center_name")
            customer_name=request.POST.get("customer_name")
            customer_email=request.POST.get("customer_email")
            customer_mobile=request.POST.get("customer_mobile")
            customer_address=request.POST.get("customer_address")
            visit_type=request.POST.get("visit_type")
            visit_date=request.POST.get("visit_date")
            time_slot=request.POST.get("time_slot")

            print(device_name,issue_description,device_serial_number,service_center_name,customer_name,customer_email,
                  customer_mobile,customer_address,visit_type,visit_date,time_slot,'==================================')
            if not device_name:
                return JsonResponse({'error': 'Device details are required.'}, status=400)
            
            if not customer_name or not customer_email or not customer_mobile or not customer_address:
                return JsonResponse({'error': 'Customer details are required.'}, status=400)
            
            if not visit_date or not time_slot:
                return JsonResponse({'error': 'Visit details are required.'}, status=400)

            if '@' not in customer_email:
                return JsonResponse({'error': 'Invalid email format.'}, status=400)

            if len(customer_mobile) != 10 or not customer_mobile.isdigit():
                return JsonResponse({'error': 'Invalid mobile number.'}, status=400)
    
            total_amount = 2360
            # total_amount = 1180
            # total_amount = 1
            order_uuid = uuid.uuid4()
            order_id = f"order_{order_uuid}"
            onside_service = onsiteVisitServiceCenter.objects.create(
                order_id=order_id,
                device_name=device_name,
                issue_description=issue_description,
                device_serial_number=device_serial_number,
                service_center_name=service_center_name,
                customer_name=customer_name,
                customer_email=customer_email,
                customer_mobile=customer_mobile,
                customer_address=customer_address,
                visit_type=visit_type,
                visit_date=visit_date,
                time_slot=time_slot,
                service_charge=str(total_amount),
                payment_status='pending',
                order_note="Appointment created",
                payment_link='',
            )
            payment_data = {
                "appId": settings.CASHFREE_CLIENT_ID,
                "secretKey": settings.CASHFREE_SECRET_KEY,
                "orderId": order_id,
                "orderAmount": str(total_amount),
                "orderCurrency": "INR",
                "customerName": customer_name,
                "customerEmail": customer_email,
                "customerPhone": customer_mobile,
                "orderNote": f"Appointment scheduled for {visit_date} at {time_slot}.",
                # "returnUrl": "https://boseservicecenter.co.in/payment-return-response",
                "returnUrl": f"https://www.boseservicecenter.co.in/payment-return-response",
                "notifyUrl": "https://www.boseservicecenter.co.in/cashfree/webhook"
            }

            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'x-client-id': settings.CASHFREE_CLIENT_ID,
                'x-client-secret': settings.CASHFREE_SECRET_KEY,
            }

            response = requests.post(cashfree_url, data=payment_data, headers=headers)
            response_data = response.json()

            if response.status_code == 200 and response_data.get('paymentLink'):
                logger.info(f"Payment link created successfully: {response_data['paymentLink']}")
                onside_service.payment_link = response_data['paymentLink']
                onside_service.save()
                return JsonResponse({'status': 'success', 'payment_link': response_data['paymentLink']}, status=200)
            else:
                logger.error(f"Failed to create payment link: {response_data}")
                return JsonResponse({'status': 'error', 'message': 'Failed to create payment link.'}, status=500)
            
        except Exception as e:
            logger.error(f"Error occurred while processing the Buy Now request: {e}")
            return JsonResponse({'status': 'error', 'message': 'An error occurred. Please try again later.'}, status=500)
        



def onside_visit_service(request, key):
    return request.GET.get(key) or request.POST.get(key)


# @csrf_exempt
# def payment_online(request):
    # if request.method not in ["POST", "GET"]:
        # return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)
    # 

    # print("==== CASHFREE PAYMENT CALLBACK ====")
    # print("Request Method:", request.method)
    # print("GET Data:", dict(request.GET))
    # print("POST Data:", dict(request.POST))
    # print("Raw Body:", request.body.decode("utf-8"))
    # print("===================================")
    # 
    # try:
        # order_id = onside_visit_service(request, 'orderId')
        # tx_status = onside_visit_service(request, 'txStatus')
        # payment_mode = onside_visit_service(request, 'paymentMode')
        # reference_id = onside_visit_service(request, 'referenceId')
        # signature = onside_visit_service(request, 'signature')
        # transaction_time = onside_visit_service(request, 'txTime')
        # if not order_id or not tx_status:
            # return JsonResponse({'status': 'error', 'message': 'Missing required parameters.'}, status=400)
        # 
        # if tx_status in ['USER_DROPPED', 'INCOMPLETE', 'FAILED']:
            # try:
                # order = onsiteVisitServiceCenter.objects.get(order_id=order_id)
                # if tx_status == 'USER_DROPPED':
                    # order.payment_status = 'user dropped'
                # elif tx_status == 'INCOMPLETE':
                    # order.payment_status = 'incomplete'
                # elif tx_status == 'FAILED':
                    # order.payment_status = 'failed'
                # order.save()
            # except onsiteVisitServiceCenter.DoesNotExist:
                # logger.warning(f"Order not found: {order_id}")
                # return JsonResponse({'status': 'error', 'message': 'Order not found.'}, status=404)
            # return redirect('https://boseservicecenter.co.in/appointment_form')
        # 
        # verify_url = f"https://api.cashfree.com/pg/orders/{order_id}?version=2022-09-01"
        # headers = {
            # "x-client-id": settings.CASHFREE_CLIENT_ID,
            # "x-client-secret": settings.CASHFREE_SECRET_KEY,
            # "x-api-version": "2022-09-01",
        # }
        # try:
            # response = requests.get(verify_url, headers=headers)
            # response_data = response.json()
        # except requests.RequestException as e:
            # logger.error(f"Cashfree API error: {str(e)}")
            # return JsonResponse({'status': 'error', 'message': 'Failed to connect to Cashfree API.'}, status=500)
# 
        # if response.status_code != 200:
            # return JsonResponse({'status': 'error', 'message': 'Failed to verify payment.'}, status=500)
        # if response.status_code != 200:
            # return JsonResponse({'status': 'error', 'message': 'Failed to verify payment.'}, status=500)
        # try:
            # onside_visit = onsiteVisitServiceCenter.objects.get(order_id=order_id)
        # except onsiteVisitServiceCenter.DoesNotExist:
            # logger.warning(f"Order not found: {order_id}")
            # return JsonResponse({'status': 'error', 'message': 'Order not found.'}, status=404)
        # cashfree_status = response_data.get('order_status')
# 
        # onside_visit.payment_mode = payment_mode
        # onside_visit.reference_id = reference_id
        # onside_visit.signature = signature
        # onside_visit.transaction_time = transaction_time
        # onside_visit.payment_status = 'paid' if tx_status == 'SUCCESS' and cashfree_status == 'PAID' else 'pending'
# 
        # if tx_status == 'SUCCESS' and cashfree_status == 'PAID':
            # onside_visit.payment_status = 'paid' 
        # else:
            # onside_visit.payment_status = 'pending'
        # onside_visit.save()
# 
        # payment_response = paymentResponseOnline.objects.update_or_create(
                # visit_service_id=onside_visit,
                # defaults={
                    # 'transaction_id': reference_id,
                    # 'amount': onside_visit.service_charge, 
                    # 'status': 'success' if tx_status == 'SUCCESS' and cashfree_status == 'PAID' else 'failed',
                    # 'update_status': onside_visit.payment_status,
                    # 'gateway_response': response_data,
                    # 'customer_name': onside_visit.customer_name, 
                    # 'customer_email': onside_visit.customer_email,
                    # 'customer_phone': onside_visit.customer_mobile, 
                    # 'customer_address': onside_visit.customer_address, 
                    # }
                # )   
        # 
        # transaction_time = datetime.strptime(transaction_time, '%Y-%m-%d %H:%M:%S')
        # pdf_context = {
            # 'order_id': onside_visit.order_id,
            # 'device_name': onside_visit.device_name,
            # 'issue_description': onside_visit.issue_description,
            # 'device_serial_number': onside_visit.device_serial_number,
            # 'service_center_name': onside_visit.service_center_name,
            # 'customer_name': onside_visit.customer_name,
            # 'customer_email': onside_visit.customer_email,
            # 'customer_phone': onside_visit.customer_mobile,
            # 'customer_address': onside_visit.customer_address,
            # 'visit_type': onside_visit.visit_type,
            # 'visit_date': onside_visit.visit_date,
            # 'time_slot': onside_visit.time_slot,
            # 'service_charge': onside_visit.service_charge,
            # 'payment_status': onside_visit.payment_status,
            # 'transaction_id': reference_id,
            # 'transaction_date':transaction_time,
            # "payment_mode":onside_visit.payment_mode,
        # }
from datetime import datetime
from django.utils import timezone

@csrf_exempt
def payment_online(request):
    if request.method not in ["POST", "GET"]:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

    print("==== CASHFREE PAYMENT CALLBACK ====")
    print("Request Method:", request.method)
    print("GET Data:", dict(request.GET))
    print("POST Data:", dict(request.POST))
    print("Raw Body:", request.body.decode("utf-8"))
    print("===================================")

    try:
        order_id = onside_visit_service(request, 'orderId')
        tx_status = onside_visit_service(request, 'txStatus')
        payment_mode = onside_visit_service(request, 'paymentMode')
        reference_id = onside_visit_service(request, 'referenceId')
        signature = onside_visit_service(request, 'signature')
        transaction_time_str = onside_visit_service(request, 'txTime')

        if not order_id or not tx_status:
            return JsonResponse({'status': 'error', 'message': 'Missing required parameters.'}, status=400)

        if tx_status in ['USER_DROPPED', 'INCOMPLETE', 'FAILED']:
            try:
                order = onsiteVisitServiceCenter.objects.get(order_id=order_id)
                order.payment_status = {
                    'USER_DROPPED': 'user dropped',
                    'INCOMPLETE': 'incomplete',
                    'FAILED': 'failed'
                }.get(tx_status, 'failed')
                order.save()
            except onsiteVisitServiceCenter.DoesNotExist:
                logger.warning(f"Order not found: {order_id}")
                return JsonResponse({'status': 'error', 'message': 'Order not found.'}, status=404)
            return redirect('https://www.boseservicecenter.co.in/appointment_form')

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
            onside_visit = onsiteVisitServiceCenter.objects.get(order_id=order_id)
        except onsiteVisitServiceCenter.DoesNotExist:
            logger.warning(f"Order not found: {order_id}")
            return JsonResponse({'status': 'error', 'message': 'Order not found.'}, status=404)

        cashfree_status = response_data.get('order_status')
        onside_visit.payment_mode = payment_mode
        onside_visit.reference_id = reference_id
        onside_visit.signature = signature

        # ✅ Parse transaction time safely
        try:
            transaction_time = datetime.strptime(transaction_time_str, '%Y-%m-%d %H:%M:%S')
        except Exception as e:
            logger.warning(f"Invalid transaction_time format: {transaction_time_str}")
            transaction_time = timezone.now()

        onside_visit.transaction_time = transaction_time
        onside_visit.payment_status = 'paid' if tx_status == 'SUCCESS' and cashfree_status == 'PAID' else 'pending'
        onside_visit.save()

        payment_response = paymentResponseOnline.objects.update_or_create(
            visit_service_id=onside_visit,
            defaults={
                'transaction_id': reference_id,
                'amount': onside_visit.service_charge,
                'status': 'success' if tx_status == 'SUCCESS' and cashfree_status == 'PAID' else 'failed',
                'update_status': onside_visit.payment_status,
                'gateway_response': response_data,
                'customer_name': onside_visit.customer_name,
                'customer_email': onside_visit.customer_email,
                'customer_phone': onside_visit.customer_mobile,
                'customer_address': onside_visit.customer_address,
            }
        )

        pdf_context = {
            'order_id': onside_visit.order_id,
            'device_name': onside_visit.device_name,
            'issue_description': onside_visit.issue_description,
            'device_serial_number': onside_visit.device_serial_number,
            'service_center_name': onside_visit.service_center_name,
            'customer_name': onside_visit.customer_name,
            'customer_email': onside_visit.customer_email,
            'customer_phone': onside_visit.customer_mobile,
            'customer_address': onside_visit.customer_address,
            'visit_type': onside_visit.visit_type,
            'visit_date': onside_visit.visit_date,
            'time_slot': onside_visit.time_slot,
            'service_charge': onside_visit.service_charge,
            'payment_status': onside_visit.payment_status,
            'transaction_id': reference_id,
            'transaction_date': transaction_time,
            "payment_mode": onside_visit.payment_mode,
        }
        
        
        pdf_html = render_to_string('onsite-visit-pdf.html', pdf_context)
        pdf_file = HTML(string=pdf_html).write_pdf()
        email_subject = "Payment Success - Appointment Confirmation"
        email_subject = "Onsite Service Visit Confirmation" 

        email_body = f"""
<html>
<body style="margin: 0px; padding: 0px; box-sizing: border-box; font-family: Arial, sans-serif;  color: #000;">

<div style="padding: 20px; max-width: 600px; margin: 0; background-color: #e3e3e3; color: #000; border: 1px solid #444; border-radius: 8px;">
    <a href="https://www.boseservicecenter.co.in/appointment_form"><img src="https://www.boseservicecenter.co.in/static/images/mail-banner-booknow.jpg" style="width: 100%; height: auto; margin-bottom: 20px;"></a>
    <p style="font-size: 16px; color: #000;">Dear {onside_visit.customer_name},</p>
    <p style="font-size: 14px; color: #000;">Your onsite service visit has been scheduled. Please find the visit confirmation attached.</p>

    <!-- Billing Address Section -->
    <table cellpadding="3" cellspacing="0" style="width: 100%; background-color:#f2f2f2; margin-bottom: 10px; padding: 10px; border-radius: 8px; border-collapse: collapse;">
        <tr>
            <td colspan="2" style="color: #ffffff;font-weight: bold;border-bottom: 1px solid #444;padding: 10px;background: #5a5a68;border-radius: 10px 10px 0px 0px;">Customer Details:</td>
        </tr>
        <tr>
            <td style="color: #000; padding: 10px;">Name:</td>
            <td style="color: #000; padding: 10px;">{onside_visit.customer_name or "-"}</td>
        </tr>
        <tr>
            <td style="color: #000; padding: 10px;">Mobile Number:</td>
            <td style="color: #000; padding: 10px;">{onside_visit.customer_mobile or "-"}</td>
        </tr>
        <tr>
            <td style="color: #000; padding: 10px;">Email:</td>
            <td style="color: #000; padding: 10px;">{onside_visit.customer_email or "-"}</td>
        </tr>
        <tr>
            <td style="color: #000; padding: 10px;">Address:</td>
            <td style="color: #000; padding: 10px;">{onside_visit.customer_address or "-"}</td>
        </tr>
    </table>

    <!-- Customer Information Section -->
    <table cellpadding="3" cellspacing="0" style="width: 100%; background-color: #f2f2f2; margin-bottom: 10px; padding: 10px; border-radius: 8px; border-collapse: collapse;">
        <tr>
            <td colspan="2" style="color: #ffffff;font-weight: bold;border-bottom: 1px solid #444;padding: 10px;background: #5a5a68;border-radius: 10px 10px 0px 0px;">Device Details:</td>
        </tr>
        <tr>
            <td style="color: #000; padding: 10px;">Device Name:</td>
            <td style="color: #000; padding: 10px;">{onside_visit.device_name or "-"}</td>
        </tr>
        <tr>
            <td style="color: #000; padding: 10px;">Issue Description:</td>
            <td style="color: #000; padding: 10px;">{onside_visit.issue_description or "-"}</td>
        </tr>
        <tr>
            <td style="color: #000; padding: 10px;">Serial Number:</td>
            <td style="color: #000; padding: 10px;">{onside_visit.device_serial_number or "-"}</td>
        </tr>
    </table>

    <!-- Service Details -->
    <table cellpadding="3" cellspacing="0" style="width: 100%; background-color: #f2f2f2; margin-bottom: 10px; padding: 10px; border-radius: 8px; border-collapse: collapse;">
        <tr>
            <td colspan="2" style="color: #ffffff;font-weight: bold;border-bottom: 1px solid #444;padding: 10px;background: #5a5a68;border-radius: 10px 10px 0px 0px;">Service Details:</td>
        </tr>
        <tr>
            <td style="color: #000; padding: 10px;">Service Center Name:</td>
            <td style="color: #000; padding: 10px;">{onside_visit.service_center_name or "-"}</td>
        </tr>
        <tr>
            <td style="color: #000; padding: 10px;">Visit Type:</td>
            <td style="color: #000; padding: 10px;">{onside_visit.visit_type or "-"}</td>
        </tr>
        <tr>
            <td style="color: #000; padding: 10px;">Visit Date:</td>
            <td style="color: #000; padding: 10px;">{ onside_visit.visit_date or "-"}</td>
        </tr>
        <tr>
            <td style="color: #000; padding: 10px;">Time Slot:</td>
            <td style="color: #000; padding: 10px;">{onside_visit.time_slot or "-"}</td>
        </tr>
    </table>

    
     <!-- Transaction Details Section -->
    <table cellpadding="3" cellspacing="0" style="width: 100%; background-color: #f2f2f2; margin-bottom: 10px; padding: 10px; border-radius: 8px; border-collapse: collapse;">
        <tr>
            <td colspan="2" style="color: #ffffff;font-weight: bold;border-bottom: 1px solid #444;padding: 10px;background: #5a5a68;border-radius: 10px 10px 0px 0px;">Transaction Details:</td>
        </tr>
        <tr>
            <td style="color: #000; padding: 10px;">Transaction ID:</td>
            <td style="color: #000; padding: 10px;">{reference_id or "-"}</td>
        </tr>
        <tr>
            <td style="color: #000; padding: 10px;">Amount:</td>
            <td style="color: #000; padding: 10px;">{onside_visit.service_charge or '-'}</td>
        </tr>
        <tr>
            <td style="color: #000; padding: 10px;">Date:</td>
            <td style="color: #000; padding: 10px;">{transaction_time or "-"}</td>
        </tr>
        <tr>
            <td style="color: #000; padding: 10px;">Payment Method:</td>
            <td style="color: #000; padding: 10px;">{onside_visit.payment_mode or "-"}</td>
        </tr>
    </table>



        <p style="font-size: 14px; color: #000;">If you have any questions or need assistance, please contact us at:</p>
        <p style="font-size: 14px; color: #000;">
        <a href="mailto:support@boseservicecenter.co.in" style="color: #000;">support@boseservicecenter.co.in</a> |
        Whatsapp: <a href="https://wa.me/919987223322?text=Hello%2C%20Required%20Assistance%20for%20Bose%20Products" target="_blank" style="color: #000;">9987223322</a>
    </p>
    <p style="font-size: 14px; color: #000;">Best regards,<br>Bose Service Center. (3rd Party Sales & Services).</p>
</div>
</body>
</html>
"""


        connection = get_connection(
                backend=settings.EMAIL_BACKEND_SECONDARY,
                host=settings.EMAIL_HOST_SECONDARY,
                port=settings.EMAIL_PORT_SECONDARY,
                username=settings.EMAIL_HOST_USER_SECONDARY,
                password=settings.EMAIL_HOST_PASSWORD_SECONDARY,
                use_ssl=settings.EMAIL_USE_SSL_SECONDARY,
            )
        to_email = [onside_visit.customer_email]  
        email = EmailMessage(
                subject=email_subject,
                body=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL_SECONDARY,
                to=to_email,
                # bcc=['klickinfosys@gmail.com', 'support@boseservicecenter.co.in'],
                bcc=[
                    # '"Bose Support" <klickinfosys@gmail.com>', 
                    '"Bose Support" <support@boseservicecenter.co.in>',
                    '"Bose Support" <bapu44@gmail.com>'
                ], 
                connection=connection,
            )
        email.attach('payment_confirmation.pdf', pdf_file, 'application/pdf')
        email.content_subtype = "html"
        email.send()
        return render(request, "onsite-appointment-confirmation.html")
     
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@csrf_exempt
def onsite_slot_check_book(request):
    if request.method == 'POST':
        visit_date = request.POST.get('visit_date')  
        if visit_date:
            available_time_slots = onsiteVisitServiceCenter.objects.filter(visit_date=visit_date).values('time_slot','payment_status').distinct()
            if available_time_slots:
                response_data = {'time_slots': list(available_time_slots)}
                return JsonResponse(response_data, safe=False)
            return JsonResponse({'status':404,"message": "No time slots available for the selected date"})

        return JsonResponse({"error": "Visit date is required"}, status=400)
    
    return JsonResponse({"error": "Invalid request method"}, status=400)



@csrf_exempt
def offsite_slot_check_book(request):
    if request.method == 'POST':
        visit_date = request.POST.get('visit_date')
        print(visit_date, '========================')  
        if visit_date:
            time_slots = (
                OffsiteServiceVisit.objects.filter(visit_date=visit_date)
                .values('time_slot')
                .annotate(slot_count=Count('time_slot'))
                .filter(slot_count__gte=2)  
            )
            if time_slots:
                time_slots_list = list(time_slots)
                response_data = {
                    'count': len(time_slots_list),
                    'time_slots': time_slots_list
                }
                print(response_data, '============')
                return JsonResponse(response_data, safe=False)
            
            return JsonResponse({'status': 404, "message": "No time slots available with count >= 2 for the selected date"})
        
        return JsonResponse({"error": "Visit date is required"}, status=400)
    
    return JsonResponse({"error": "Invalid request method"}, status=400)



def whatsapp_page(request):
    """Render a page with a form to send WhatsApp messages."""
    return render(request, "myapp/whatsapp_form.html")  


import requests

@csrf_exempt 
def send_whatsapp_messagess(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            phone_number = data.get("phone_number") 
            message = data.get("message", "Default message")

            if not phone_number:
                return JsonResponse({"error": "Phone number is required"}, status=400)

            API_URL = "https://api.ultramsg.com/instance109858/messages/chat"
            TOKEN = "qk1jr8xivs4ickyi" 

            payload = {
                "token": TOKEN,
                "to": phone_number,
                "body": message
            }

            headers = {
                "Content-Type": "application/x-www-form-urlencoded"
            }

            response = requests.post(API_URL, data=payload, headers=headers)

            return JsonResponse(response.json(), status=response.status_code)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    return JsonResponse({"error": "Invalid request method"}, status=405)



# manualDisabled

@csrf_exempt 
def create_manual_appointment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            device_name = data.get('device_name')
            issue_description = data.get("issue_description")
            device_serial_number = data.get("device_serial_number", "")
            service_center_name = data.get("service_center_name")
            customer_name = data.get("customer_name")
            customer_email = data.get("customer_email")
            customer_mobile = data.get("customer_mobile")
            customer_address = data.get("customer_address")
            visit_type = data.get("visit_type")
            visit_date = data.get("visit_date")
            time_slot = data.get("time_slot")

            print("Received Appointment Data:", data)

            if not all([device_name, issue_description, service_center_name, customer_name, customer_email, customer_mobile, customer_address, visit_type, visit_date, time_slot]):
                return JsonResponse({'status': 'error', 'message': 'Missing required fields.'}, status=400)

            record = ManualDisabled.objects.create(
                device_name=device_name,
                issue_description=issue_description,
                device_serial_number=device_serial_number,
                service_center_name=service_center_name,
                customer_name=customer_name,
                customer_email=customer_email,
                customer_mobile=customer_mobile,
                customer_address=customer_address,
                visit_type=visit_type,
                visit_date=visit_date,
                time_slot=time_slot,
                payment_status='disabled'
            )

            return JsonResponse({
                'status': 'success',
                'message': 'Manual appointment created successfully.',
                'appointment_id': record.id
            }, status=201)

        except Exception as e:
            print("Error creating appointment:", e)
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    else:
        return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed.'}, status=405)
    

@csrf_exempt
def manual_slot_check_book(request):
    if request.method == 'POST':
        visit_date = request.POST.get('visit_date')

        if visit_date:
            available_time_slots = ManualDisabled.objects.filter(
                visit_date=visit_date
            ).values('time_slot', 'payment_status').distinct()

            if available_time_slots.exists():
                return JsonResponse({'time_slots': list(available_time_slots)}, safe=False)
            else:
                return JsonResponse({'status': 404, 'message': 'No manual disabled slots found for the selected date'})

        return JsonResponse({'status': 400, 'error': 'Visit date is required'})

    return JsonResponse({'status': 405, 'error': 'POST method required'})
