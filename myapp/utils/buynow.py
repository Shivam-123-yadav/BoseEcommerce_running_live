from django.http import JsonResponse
from ..models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render,redirect
from django.http import HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
from django.shortcuts import redirect
import uuid
import requests
import logging
from django.views import View
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.template.loader import render_to_string
from weasyprint import HTML
from django.core.mail import EmailMessage
from django.utils import timezone 
from django.core.mail import send_mail
# live

logger = logging.getLogger(__name__)
# cashfree_url = 'https://test.cashfree.com/api/v1/order/create'
cashfree_url = 'https://api.cashfree.com/api/v1/order/create'



@csrf_exempt
def buy_products(request, item_slug):
    """
    Fetch details for a specific item by slug and display it.
    """
    if request.method == 'GET':
        item = get_object_or_404(ItemDetail, slug=item_slug)
        quantity = int(request.GET.get('quantity', 1))  

        product_price = item.mrp_price or 0
        discount_amount = item.discount_amount or 0
        shipping_charges = item.shipping_charges or 0
        total_subtotal = product_price * quantity
        total_discount = discount_amount * quantity
        total_shipping_charge = shipping_charges
        total_amount = total_subtotal - total_discount + total_shipping_charge
        logger.info(f"Product Price: {product_price} x {quantity}")
        logger.info(f"Discount: -{total_discount}")
        logger.info(f"Shipping Charges: +{total_shipping_charge}")
        logger.info(f"Total Amount: {total_amount}")

        item_data = {
            "id": item.id,
            "slug":item.slug,
            "title": item.title,
            "category": item.get_category_display(),
            "mrp_price": product_price,
            "discount_percentage": item.discount_percentage,
            "discount_amount": total_discount,
            "final_price": item.final_price,
            "shipping_charges": total_shipping_charge,
            "total_amount": total_amount,
            "image1_url": item.image1.url if item.image1 else None,
            "quantity": quantity
        }
        return render(request, 'myapp/buyproducts.html', {"data": item_data})



@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(login_required, name='dispatch')
class BuyNowView(View):
    def post(self, request, *args, **kwargs):
        try:
            existing_order = Order.objects.filter(user=request.user, payment_status='pending').first()
            if existing_order:
                existing_order.delete()
                
            product_id = request.POST.get('fetch_id')
            quantity = request.POST.get('quantity')
            color_name=request.POST.get("color_name")
            imagesrc=request.POST.get("imagesrc")
            print(product_id, '=================', quantity, '====================',color_name,imagesrc)
            
            if not product_id:
                return JsonResponse({'status': 'error', 'message': 'Product ID is required.'}, status=400)
            
            product = ItemDetail.objects.filter(id=product_id).first()
            if not product:
                return JsonResponse({'status': 'error', 'message': 'Invalid product.'}, status=404)
            
            product_price = product.mrp_price or 0
            discount_amount = product.discount_amount or 0
            shipping_charges = product.shipping_charges or 0
            total_subtotal = product_price * int(quantity)
            total_discount = discount_amount * int(quantity)
            total_shipping_charge = shipping_charges * int(quantity)
            total_amount = total_subtotal - total_discount + total_shipping_charge

            logger.info(f"Product Price: {product_price}")
            logger.info(f"Discount: -{discount_amount}")
            logger.info(f"Shipping Charges: +{shipping_charges}")
            logger.info(f"Total Amount: {total_amount}")
            
            order_uuid = uuid.uuid4()
            order_id = f"order_{order_uuid}"

            order = Order.objects.create(
                order_id=order_id,
                user=request.user,
                total_amount=total_amount,
                payment_status='pending',
                order_note=f"Purchase of {product.title} (Quantity: {quantity})",
                payment_link='',
            )

            OrderItem.objects.create(
                order=order,
                item=product,
                quantity=int(quantity),
                total_price=product.final_price * int(quantity),
                type_color_name=color_name,
                type_color_image_url=imagesrc
            )

            payment_data = {
                "appId": settings.CASHFREE_CLIENT_ID,
                "secretKey": settings.CASHFREE_SECRET_KEY,
                "orderId": order_id,
                "orderAmount": str(total_amount),
                "orderCurrency": "INR",
                "customerName": request.user.user_details.first_name,
                "customerEmail": request.user.user_details.email,
                "customerPhone": request.user.user_details.phone_number,
                "orderNote": f"Purchase of {product.title} (Quantity: {quantity})",
                # "returnUrl": "https://www.boseservicecenter.co.in/payment-return",
                # "returnUrl": "https://boseservicecenter.co.in/payment-returns-buynow",
                "returnUrl": "https://www.boseservicecenter.co.in/payment-returns-buynow",
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
                order.payment_link = response_data['paymentLink']
                order.save()

                return JsonResponse({'status': 'success', 'payment_link': response_data['paymentLink']}, status=200)
            else:
                logger.error(f"Failed to create payment link: {response_data}")
                return JsonResponse({'status': 'error', 'message': 'Failed to create payment link.'}, status=500)

        except Exception as e:
            logger.error(f"Error occurred while processing the Buy Now request: {e}")
            return JsonResponse({'status': 'error', 'message': 'An error occurred. Please try again later.'}, status=500)




# 
# def get_request_data_buy(request, key):
    # return request.GET.get(key) or request.POST.get(key)
# 
# 
# @csrf_exempt
# def payment_returns_buynow(request):
    # print(request.POST,'========POSTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT')
    # if request.method not in ["POST", "GET"]:
        # return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)
    # try:
        # order_id = get_request_data_buy(request, 'orderId')
        # tx_status = get_request_data_buy(request, 'txStatus')
        # payment_mode = get_request_data_buy(request, 'paymentMode')
        # reference_id = get_request_data_buy(request, 'referenceId')
        # signature = get_request_data_buy(request, 'signature')
        # transaction_time = get_request_data_buy(request, 'txTime')
# 
        # if not order_id or not tx_status:
            # return JsonResponse({'status': 'error', 'message': 'Missing required parameters.'}, status=400)
        # 
# 
        # if tx_status in ['USER_DROPPED', 'INCOMPLETE', 'FAILED']:
            # try:
                # order = Order.objects.get(order_id=order_id)
                # if tx_status == 'USER_DROPPED':
                    # order.status = Order.OrderStatus.USER_DROPPED
                    # order.payment_mode = payment_mode
                    # order.reference_id = reference_id
                    # order.signature = signature
                # elif tx_status == 'INCOMPLETE':
                    # order.status = Order.OrderStatus.INCOMPLETE
                # elif tx_status == 'FAILED':
                    # order.status = Order.OrderStatus.CANCELLED 
                    # order.payment_status = 'failed'
                    # if order.user.email:
                        # subject = "Transaction Failed"
                        # message = f"Dear {order.user.username},\n\nYour transaction has failed. Please try again."
                        # from_email = settings.DEFAULT_FROM_EMAIL
                        # recipient_list = [order.user.email]
                        # send_mail(subject, message, from_email, recipient_list)
                # order.save()
            # except Order.DoesNotExist:
                # logger.warning(f"Order not found: {order_id}")
                # return JsonResponse({'status': 'error', 'message': 'Order not found.'}, status=404)
            # return redirect('https://boseservicecenter.co.in/products-category?filter=portablebluetooth')
# 
        # 
        # verify_url = f"https://api.cashfree.com/pg/orders/{order_id}?version=2022-09-01"
        # headers = {
            # "x-client-id": settings.CASHFREE_CLIENT_ID,
            # "x-client-secret": settings.CASHFREE_SECRET_KEY,
            # "x-api-version": "2022-09-01",
        # }
# 
        # try:
            # response = requests.get(verify_url, headers=headers)
            # response_data = response.json()
        # except requests.RequestException as e:
            # logger.error(f"Cashfree API error: {str(e)}")
            # return JsonResponse({'status': 'error', 'message': 'Failed to connect to Cashfree API.'}, status=500)
# 
        # if response.status_code != 200:
            # return JsonResponse({'status': 'error', 'message': 'Failed to verify payment.'}, status=500)
        # try:
            # order = Order.objects.get(order_id=order_id)
        # except Order.DoesNotExist:
            # logger.warning(f"Order not found: {order_id}")
            # return JsonResponse({'status': 'error', 'message': 'Order not found.'}, status=404)
# 
        # cashfree_status = response_data.get('order_status')
        # order.payment_mode = payment_mode
        # order.reference_id = reference_id
        # order.signature = signature
        # order.transaction_time = transaction_time
        # order.payment_status = 'success' if tx_status == 'SUCCESS' and cashfree_status == 'PAID' else 'failed'
        # if tx_status == 'SUCCESS' and cashfree_status == 'PAID':
            # order.status = Order.OrderStatus.PAID
        # order.save()
# 
        # Cart.objects.filter(user=order.user).delete()
# 
        # order_item_instances = order.order_items.all()
# 
        # item_details = [
            # {
                # 'title': order_item.item.title,
                # 'quantity': order_item.quantity,
                # 'final_price': order_item.item.final_price,  
                # 'color_name': (order_item.type_color_name.replace("-", " ").title() if order_item.type_color_name else "N/A"),
# 
                # 'color_image_url': order_item.type_color_image_url,  # Add color image URL
            # }
            # for order_item in order_item_instances
        # ]
# 
        # order_item_instance = None
        # if order.order_items.exists():
            # order_item_instance = order.order_items.first()
# 
        # payment_status, created = paymentStatus.objects.update_or_create(
            # order=order,
            # order_item=order_item_instance,
            # defaults={
                # 'user': order.user,
                # 'amount': order.total_amount,
                # 'status': order.payment_status,
                # 'transaction_id': reference_id, 
                # 'customer_name': order.user.user_details.first_name,
                # 'customer_email': order.user.user_details.email,
                # 'customer_phone': order.user.user_details.phone_number,
                # 'customer_address': order.user.user_details.address,
                # 'gateway_response': response_data,
            # }
        # )
# 
        # if isinstance(order.transaction_time, str):
            # try:
                # timestamp = datetime.strptime(order.transaction_time, "%Y-%m-%d %H:%M:%S")
                # print(timestamp,'timestamp===============================================')
            # except ValueError:
                # logger.error(f"Failed to parse transaction_time: {order.transaction_time}")
                # return JsonResponse({'status': 'error', 'message': 'Invalid transaction time format'}, status=400)
        # else:
            # timestamp = order.transaction_time
        # if timestamp.tzinfo is None:
            # timestamp = timezone.make_aware(timestamp)
# 
        # date_only = timestamp
        # pdf_context = {
            # 'user': order.user,
            # 'amount': order.total_amount,
            # 'status': order.payment_status,
            # 'transaction_id': reference_id,
            # 'customer_name': order.user.user_details.first_name,
            # 'customer_email': order.user.user_details.email,
            # 'customer_phone': order.user.user_details.phone_number,
            # 'customer_address': order.user.user_details.address,
            # 'customer_state': order.user.user_details.state,
            # 'customer_city': order.user.user_details.city,
            # 'customer_zipcode': order.user.user_details.postal_code,
            # 'gateway_response': response_data,
            # "payment_mode":order.payment_mode,
            # "transaction_date": date_only,
            # "item_details":item_details,
        # }

def get_request_data_buy(request, key):
    return request.GET.get(key) or request.POST.get(key)

@csrf_exempt
def payment_returns_buynow(request):
    if request.method not in ["POST", "GET"]:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

    try:
        order_id = get_request_data_buy(request, 'orderId')
        tx_status = get_request_data_buy(request, 'txStatus')
        payment_mode = get_request_data_buy(request, 'paymentMode')
        reference_id = get_request_data_buy(request, 'referenceId')
        signature = get_request_data_buy(request, 'signature')
        transaction_time = get_request_data_buy(request, 'txTime')

        if not order_id or not tx_status:
            return JsonResponse({'status': 'error', 'message': 'Missing required parameters.'}, status=400)

        # Handle drop, incomplete, or failed transactions
        if tx_status in ['USER_DROPPED', 'INCOMPLETE', 'FAILED']:
            try:
                order = Order.objects.get(order_id=order_id)
                order.payment_mode = payment_mode
                order.reference_id = reference_id
                order.signature = signature

                if tx_status == 'USER_DROPPED':
                    order.status = Order.OrderStatus.USER_DROPPED

                elif tx_status == 'INCOMPLETE':
                    order.status = Order.OrderStatus.INCOMPLETE

                elif tx_status == 'FAILED':
                    order.status = Order.OrderStatus.CANCELLED
                    order.payment_status = 'failed'

                    # Email on failed payment
                    if order.user.email:
                        subject = "Your Bose Service Payment Failed"
                        message = f"Dear {order.user.username},\n\nYour transaction has failed. Please try again or contact support."
                        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [order.user.email])

                order.save()
            except Order.DoesNotExist:
                logger.warning(f"Order not found: {order_id}")
                return JsonResponse({'status': 'error', 'message': 'Order not found.'}, status=404)

            return redirect('https://www.boseservicecenter.co.in/products-category?filter=portablebluetooth')

        # ✅ Verify payment via Cashfree API
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

        order_item_instances = order.order_items.all()

        item_details = [
            {
                'title': item.item.title,
                'quantity': item.quantity,
                'final_price': item.item.final_price,
                'color_name': item.type_color_name.replace("-", " ").title() if item.type_color_name else "N/A",
                'color_image_url': item.type_color_image_url,
            }
            for item in order_item_instances
        ]

        order_item_instance = order_item_instances.first() if order_item_instances.exists() else None

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

        if isinstance(order.transaction_time, str):
            try:
                timestamp = datetime.strptime(order.transaction_time, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                logger.error(f"Failed to parse transaction_time: {order.transaction_time}")
                return JsonResponse({'status': 'error', 'message': 'Invalid transaction time format'}, status=400)
        else:
            timestamp = order.transaction_time

        if timestamp.tzinfo is None:
            timestamp = timezone.make_aware(timestamp)

        date_only = timestamp

        # ✅ Generate PDF
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
            # email_body = f"Dear {order.user.user_details.first_name},\n\nYour payment was successful. Please find the order confirmation attached. "background-color: #ef6950;
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
#             email_body = f"""
# <html>
# <body style="margin: 0px;
# 	  padding: 0px;
# 	  -webkit-box-sizing: border-box;
# 	  -moz-box-sizing: border-box;
# 	  box-sizing: border-box; color:#fff;overflow:hidden;font-family: var(--font-muli);">

# <div style="padding:10px; display:block; width:100%; background:#222; color:#fff;"><p style="color:#fff;">Dear {order.user.user_details.first_name},</p>

# <p style="color:#fff;">Your payment has been successfully processed. We are now preparing your order. You will receive a confirmation email shortly.</p>

# <div style="background:#333; margin-bottom:5px; border-bottom:5px #333; padding:10px;">
# <p style="color:#fff;"><b>Billing Address:</b><br>
# <span style="color:#fff;">---------------------------------</span><br>
# <b style="color:#fff;">Name:</b> <span style="color:#fff;">{order.user.user_details.first_name or "-"}</span><br>
# <b style="color:#fff;">Address:</b> <span style="color:#fff;">{order.user.user_details.address or "-"}</span><br>
# <b style="color:#fff;">State:</b> <span style="color:#fff;">{order.user.user_details.state or "-"}</span><br>
# <b style="color:#fff;">City:</b> <span style="color:#fff;">{order.user.user_details.city or "-"}</span><br>
# <b style="color:#fff;">Zip Code:</b> <span style="color:#fff;">{order.user.user_details.postal_code or "-"}</span></p></div>

# <div style="background:#333; margin-bottom:5px; border-bottom:5px #333; padding:10px;"><p style="color:#fff;"><b>Customer Information:</b><br>
# <span style="color:#fff;">---------------------------------</span><br>
# <b style="color:#fff;">Email:</b> <span style="color:#fff;">{order.user.user_details.email or "-"}</span><br>
# <b style="color:#fff;">Mobile Number:</b> <span style="color:#fff;">{order.user.user_details.phone_number or "-"}</span><br></div>

# <div style="background:#333; margin-bottom:5px; border-bottom:5px #333; padding:10px;"><p style="color:#fff;"><b>Transaction Details:</b><br>
# <span style="color:#fff;">---------------------------------</span><br>
# <b style="color:#fff;">Transaction ID:</b> <span style="color:#fff;">{reference_id or "-"}</span><br>
# <b style="color:#fff;">Transaction Date:</b> <span style="color:#fff;">{date_only or "-"}</span><br>
# <b style="color:#fff;">Payment Method:</b> <span style="color:#fff;">{order.payment_mode or "-"}</span><br></div>

# <div style="background:#333; margin-bottom:5px; border-bottom:5px #333; padding:10px;"><p style="color:#fff;"><b style="color:#fff;">Product Details:</b><br>
# <span style="color:#fff;">---------------------------------</span><br>
#  """
#             for item in item_details:
#                 email_body += f"""
# <b style="color:#fff;">Product Name:</b> <span style="color:#fff;">{item['title'] or "-"}</span><br>
# <b style="color:#fff;">Color Name:</b> <span style="color:#fff;">{item['color_name'] or "-"}</span><br>
# <b style="color:#fff;">Quantity:</b> <span style="color:#fff;">{item['quantity'] or "-"}</span><br>
# <b style="color:#fff;">Price:</b> <span style="color:#fff;">₹{item['final_price'] or "-"}</span><br>
# <b style="color:#fff;">Total:</b> <span style="color:#fff;">₹{item['quantity'] * item['final_price'] if item['final_price'] else "-"}</span><br>
# <br>
# """

#             email_body += f"""
# <b style="color:#fff;">Grand Total:</b> <span style="color:#fff;">₹{order.total_amount or "-"}</span></div><br>

# <div style="background:#333; margin-top:5px;  padding:10px;">
# <p style="color:#fff;">If you have any questions or need to reschedule, please contact us at:<br>
# <a href="mailto:sales@boseservicecenter.co.in">sales@boseservicecenter.co.in</a> | Whatsapp No. <a href="https://wa.me/919987223322?text=Hello%2C%20Required%20Assistance%20for%20Bose%20Products" class="floatbtn" target="_blank">9987223322</a></p>

# <p style="color:#fff;">Best regards,<br>
# Bose Service Center</p>
# </div>
# </div>
# </body>
# </html>
# """   





#             email_body = f"""
# <html>
# <body>
# <p>Dear {order.user.user_details.first_name},</p>

# <p>Your payment has been successfully processed. We are now preparing your order. You will receive a confirmation email shortly.</p>

# <p><b>Billing Address:</b><br>
# ---------------------------------<br>
# <b>Name:</b> {order.user.user_details.first_name or "-"}<br>
# <b>Address:</b> {order.user.user_details.address or "-"}</p><br>
# <b>State:</b> {order.user.user_details.state or "-"}</p><br>
# <b>City:</b> {order.user.user_details.city or "-"}</p><br>
# <b>Zip Code:</b> {order.user.user_details.postal_code or "-"}</p>

# <p><b>Customer Information:</b><br>
# ---------------------------------<br>
# <b>Email:</b> {order.user.user_details.email or "-"}<br>
# <b>Mobile Number:</b> {order.user.user_details.phone_number or "-"}<br>

# <p><b>Transaction Details:</b><br>
# ---------------------------------<br>
# <b>Transaction ID:</b> {reference_id or "-"}<br>
# <b>Transaction Date:</b> {date_only or "-"}<br>
# <b>Payment Method:</b> {payment_mode or "-"}<br>

# <p><b>Product Details:</b><br>
# ---------------------------------<br>
# """
#             for item in item_details:
#                 email_body += f"""
# <b>Product:</b> {item['title'] or "-"}<br>
# <b>Color Name:</b> {item['color_name'] or "-"}<br>
# <b>Quantity:</b> {item['quantity'] or "-"}<br>
# <b>Price:</b> ₹{item['final_price'] or "-"}<br>
# <b>Total:</b> ₹{item['quantity'] * item['final_price'] if item['final_price'] else "-"}<br>
# <br>
# """

#             email_body += f"""
# <b>Grand Total:</b> ₹{order.total_amount or "-"}<br>

# <p>If you have any questions or need to reschedule, please contact us at:<br>
# <a href="mailto:sales@boseservicecenter.co.in">sales@boseservicecenter.co.in</a> | Whatsapp No. <a href="https://wa.me/919987223322?text=Hello%2C%20Required%20Assistance%20for%20Bose%20Products" class="floatbtn" target="_blank">9987223322</a></p>

# <p>Best regards,<br>
# Bose Service Center
# <br>Thank you for your Order at Bose Service Center!</p>
# </body>
# </html>
# """


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
