from ..models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import logging
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.db.models import Count,Avg,Sum, Q
# live



# @csrf_exempt
# def search_with_title(request):
#     if request.method == 'POST':
#         filter_value = request.POST.get('filter', '').strip()
#     elif request.method == 'GET':
#         filter_value = request.GET.get('filter', '').strip()
#     else:
#         return JsonResponse({"error": "Invalid request method."}, status=400)
#     user_id = request.user.id if request.user.is_authenticated else None

#     categories = {
#         "remote_items": ItemDetail.Category.REMOTE,
#         "cushion_items": ItemDetail.Category.CUSHION,
#         "power_supply_items": ItemDetail.Category.POWER_SUPPLY,
#         "cable_items": ItemDetail.Category.CABLE,
#         "carrycase_items": ItemDetail.Category.CARRY_CASE,
#         "adapter_items": ItemDetail.Category.ADAPTER,
#         "others_items": ItemDetail.Category.OTHERS,
#         "stayhear_items": ItemDetail.Category.STAYHEAR,
#         "wireless_items": ItemDetail.Category.WIRELESS,
#         "noisecancelling_items": ItemDetail.Category.NOISECANCELLING,
#         "earbuds_items": ItemDetail.Category.EARBUDS,
#         "portablebluetooth_items": ItemDetail.Category.PORTABLE_BLUETOOTH,
#         "homeaudio_items": ItemDetail.Category.HOME_AUDIO,
#         "homecinema_items": ItemDetail.Category.HOME_CINEMA,
#         "soundbars_items": ItemDetail.Category.SOUND_BARS,
#         "stereo_items": ItemDetail.Category.STEREO,
#         "computerspeaker_items": ItemDetail.Category.COMPUTER_SPEAKER,
#         "portablepa_items": ItemDetail.Category.PORTABLE_PA,
#     }

#     response_data = {
#         "user_id": user_id
#     }

#     for key, cat in categories.items():
#         # items = ItemDetail.objects.filter(Q(category=cat) & Q(category__icontains=filter_value))
#         if filter_value:
#             items = ItemDetail.objects.filter(
#                 Q(category=cat) & 
#                 (Q(category__icontains=filter_value) | Q(title__icontains=filter_value))
#             )
#         else:
#             items = ItemDetail.objects.filter(Q(category=cat))

#         item_list = []
#         for item in items:
#             review_count = item.reviews.count()
#             avg_rating = item.reviews.aggregate(average_rating=Avg('rating'))['average_rating'] or 0.0
#             item_data = {
#                 "id": item.id,
#                 "title": item.title,
#                 "add_card": item.add_card,
#                 "mrp_price": item.mrp_price,
#                 "final_price": item.final_price,
#                 "discount_amount": item.discount_amount,
#                 "discount_percentage": item.discount_percentage,
#                 "shipping_charges": item.shipping_charges,
#                 "slug": item.slug,
#                 "image1": item.image1.url if item.image1 else None,
#                 "image2": item.image2.url if item.image2 else None,
#                 "image3": item.image3.url if item.image3 else None,
#                 "image4": item.image4.url if item.image4 else None,
#                 "image5": item.image5.url if item.image5 else None,
#                 "user_id": item.user_id,
#                 "category": item.category,
#                 "review_count": review_count,
#                 "average_rating": avg_rating,
#                 "box_content": item.box_content,
#                 "dimension_weight": item.dimension_weight,
#                 "materials": item.materials,
#                 "battery": item.battery,
#                 "bluetooth": item.bluetooth,
#                 "inputs": item.inputs,
#                 "microphones": item.microphones,
#                 "controls": item.controls,
#                 "compatible_app": item.compatible_app,
#                 "additions_informations": item.additions_informations,
#                 "heading1": item.heading1,
#                 "heading2": item.heading2,
#                 "heading3": item.heading3,
#                 "heading4": item.heading4,
#                 "heading5": item.heading5,
#                 "heading6": item.heading6,
#                 "overview": item.overview,
#                 "compability": item.compability,
#             }
#             item_list.append(item_data)
        
#         response_data[key] = item_list
#         response_data[f"{key}_count"] = len(item_list)
#     response_data = {key: value if value else None for key, value in response_data.items()}
#     return JsonResponse(response_data)


@csrf_exempt
def fetch_details(request):
    if request.method == 'POST':
        filter_value = request.POST.get('filter', '').strip()
    elif request.method == 'GET':
        filter_value = request.GET.get('filter', '').strip()
    else:
        return JsonResponse({"error": "Invalid request method."}, status=400)
    user_id = request.user.id if request.user.is_authenticated else None
    categories = {
        "remote_items": ItemDetail.Category.REMOTE,
        "cushion_items": ItemDetail.Category.CUSHION,
        "power_supply_items": ItemDetail.Category.POWER_SUPPLY,
        "cable_items": ItemDetail.Category.CABLE,
        "carrycase_items": ItemDetail.Category.CARRY_CASE,
        "adapter_items": ItemDetail.Category.ADAPTER,
        "others_items": ItemDetail.Category.OTHERS,
        "wireless_items": ItemDetail.Category.WIRELESS,
        "noisecancelling_items": ItemDetail.Category.NOISECANCELLING,
        "earbuds_items": ItemDetail.Category.EARBUDS,
        "portablebluetooth_items": ItemDetail.Category.PORTABLE_BLUETOOTH,
        "homeaudio_items": ItemDetail.Category.HOME_AUDIO,
        "homecinema_items": ItemDetail.Category.HOME_CINEMA,
        "soundbars_items": ItemDetail.Category.SOUND_BARS,
        "stereo_items": ItemDetail.Category.STEREO,
        "computerspeaker_items": ItemDetail.Category.COMPUTER_SPEAKER,
        "portablepa_items": ItemDetail.Category.PORTABLE_PA,
        "stayhear_items": ItemDetail.Category.STAYHEAR,
    }

    response_data = {
        "user_id": user_id 
    }

    for key, cat in categories.items():
        items = ItemDetail.objects.filter(Q(category=cat) & Q(category__icontains=filter_value))

        item_list = []
        for item in items:
            review_count = item.reviews.count()
            avg_rating = item.reviews.aggregate(average_rating=Avg('rating'))['average_rating'] or 0.0
            item_data = {
                "id": item.id,
                "title": item.title,
                "add_card": item.add_card,
                "mrp_price": item.mrp_price,
                "final_price": item.final_price,
                "discount_amount": item.discount_amount,
                "discount_percentage": item.discount_percentage,
                "shipping_charges": item.shipping_charges,
                "slug": item.slug,
                "image1": item.image1.url if item.image1 else None,
                "image2": item.image2.url if item.image2 else None,
                "image3": item.image3.url if item.image3 else None,
                "image4": item.image4.url if item.image4 else None,
                "image5": item.image5.url if item.image5 else None,
                "user_id": item.user_id,
                "category": item.category,
                "review_count": review_count,
                "average_rating": avg_rating,
                "box_content": item.box_content,
                "dimension_weight": item.dimension_weight,
                "materials": item.materials,
                "battery": item.battery,
                "bluetooth": item.bluetooth,
                "inputs": item.inputs,
                "microphones": item.microphones,
                "controls": item.controls,
                "compatible_app": item.compatible_app,
                "additions_informations": item.additions_informations,
                "heading1": item.heading1,
                "heading2": item.heading2,
                "heading3": item.heading3,
                "heading4": item.heading4,
                "heading5": item.heading5,
                "heading6": item.heading6,
                "overview": item.overview,
                "compability": item.compability,
            }
            item_list.append(item_data)
        
        response_data[key] = item_list
        response_data[f"{key}_count"] = len(item_list)
    response_data = {key: value if value else None for key, value in response_data.items()}
    return JsonResponse(response_data)




@csrf_exempt
def fetch_item_details(request, item_id):
    """
    Fetch details for a specific item by ID.
    """
    if request.method == 'GET':
        item = get_object_or_404(ItemDetail, id=item_id)
        item_data = {
            "id": item.id,
            "title": item.title,
            'availability':item.availability,
            "category": item.get_category_display(),
            "price": item.mrp_price,            
        }
        return JsonResponse({"status":200,'message':'successfully','data':item_data})
    else:
        return JsonResponse({"error": "Invalid request method."}, status=400)
    




def fetch_item_detailsss(request, item_slug):
    item = get_object_or_404(ItemDetail, slug=item_slug)
    type_colors = TypeColor.objects.filter(product=item)
    color_names = [color.color_name for color in type_colors]
    context = {
        'item': item,
        'image1': item.image1.url if item.image1 else None,
        'image2': item.image2.url if item.image2 else None,
        'image3': item.image3.url if item.image3 else None,
        'image4': item.image4.url if item.image4 else None,
        'image5': item.image5.url if item.image5 else None,
        'color_names': color_names
    }
    return render(request, 'myapp/item_details.html',context)


@csrf_exempt
def item_colors_view(request, item_id):
    if request.method=='GET':
        item_detail = get_object_or_404(ItemDetail, id=item_id)
        type_colors = TypeColor.objects.filter(product=item_detail)
        colors_data = []
        for color in type_colors:
            colors_data.append({
                'products_id': item_detail.id, 
                'type_color_id': color.type_color_id,
                'color_name': color.color_name,
                'image1': color.image1.url if color.image1 else None,
                'image2': color.image2.url if color.image2 else None,
                'image3': color.image3.url if color.image3 else None,
                'image4': color.image4.url if color.image4 else None,
                'image5': color.image5.url if color.image5 else None,
            })
        return JsonResponse({'item_detail': item_detail.id, 'colors': colors_data})

