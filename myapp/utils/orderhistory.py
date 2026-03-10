from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from ..models import *
import logging

logger = logging.getLogger(__name__)


@csrf_exempt
def orderHistory_customer(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        
        if not user_id:
            return JsonResponse({"status": 404, 'message': 'User ID not found'})
        try:
            payment_status = paymentStatus.objects.select_related('user').filter(user__id=user_id)
            if not payment_status.exists():
                return JsonResponse({'error': 'No payment status found for this user'}, status=404)
            payment_data = []
            for payment in payment_status:
                payment_data.append({
                    'user': payment.user.username,
                    'status': payment.status,
                    "payment_id":payment.id,
                    'amount': str(payment.amount),
                    "quantity":payment.order_item.quantity,
                    "image_url":payment.order_item.type_color_image_url,
                    'item_title': payment.order_item.item.title,
                    'product_id':payment.order_item.item.id,
                    "update_status":payment.update_status,
                    'item_slug': payment.order_item.item.slug,  # Include slug
                    "created_at":payment.created_at,
                })

            return JsonResponse({'payment_status': payment_data})

        except paymentStatus.DoesNotExist:
            return JsonResponse({'error': 'Payment status not found'}, status=404)
        





@csrf_exempt
def update_payment_status(request):
    if request.method == 'POST':

        product_id = request.POST.get('product_id')  
        update_status = request.POST.get('update_status') 
        user_id = request.POST.get('user_id')
        print(f"Product ID: {product_id}, Update Status: {update_status}, User ID: {user_id}")

        try:
            user = User.objects.get(id=user_id)
            payment_status = paymentStatus.objects.get(id=product_id)
            if payment_status.user_id == user.id:
                payment_status.update_status = update_status
                payment_status.save()
                return JsonResponse({'success': True, 'message': 'Payment status updated successfully'})
            else:
                return JsonResponse({'success': False, 'message': 'You are not authorized to update this product'})
        except paymentStatus.DoesNotExist:
            logger.error(f"PaymentStatus with payment_id {product_id} does not exist.")
            return JsonResponse({'success': False, 'message': 'Product not found'})

        except User.DoesNotExist:
            logger.error(f"User with ID {user_id} does not exist.")
            return JsonResponse({'success': False, 'message': 'User not found'})

        except Exception as e:
            logger.error(f"Unexpected error occurred: {str(e)}")
            return JsonResponse({'success': False, 'message': 'An error occurred while updating the status'})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})