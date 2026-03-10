from django.shortcuts import render
from ..models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Avg, Count
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import FileSystemStorage
# live
@csrf_exempt
def ClusteringDetails(request):
    if request.method == 'GET':
        fetch_products = ItemDetail.objects.all()
        result = {
            'speaker': {},
            'headphone': {},
            'accessories': {}
        }
        for item in fetch_products:
            category = item.category
            item_data = {
                "id": item.id,
                "title": item.title,
                "category": item.get_category_display(),
                "price": item.mrp_price,
                'image1': item.image1.url if item.image1 else None,
                'slug':item.slug,  
                'average_rating': item.reviews.aggregate(average_rating=Avg('rating'))['average_rating'] or 0,
                'review_count': item.reviews.count()
                
            }
            if category in ['portablebluetooth','homecinema','soundbars','stereo','computerspeaker','portablepa','homeaudio']:
                if category not in result['speaker']:
                    result['speaker'][category] = []
                result['speaker'][category].append(item_data)
            elif category in ['remote', 'cushion', 'powersupply','cable','carrycase','adapter','others']:
                if category not in result['accessories']:
                    result['accessories'][category] = []
                result['accessories'][category].append(item_data)
            elif category in ['wireless','noisecancelling','earbuds']:
                if category not in result['headphone']:
                    result['headphone'][category] = []
                result['headphone'][category].append(item_data)
        return JsonResponse({'status': 'success', 'data': result})
    return JsonResponse({'status':404,'message':'not found data'})

@csrf_exempt
def change_profile(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            userid = request.POST.get('userid')
            try:
                user_to_update = User.objects.get(id=userid)
            except User.DoesNotExist:
                return JsonResponse({
                    'status': 'error',
                    'message': 'User with the given ID does not exist'
                })

            if 'filename' in request.FILES:
                image = request.FILES['filename']
                
                user_profile, created = UserProfile.objects.get_or_create(user=user_to_update)
                user_profile.profile_image = image
                user_profile.save()
                
                file_url = user_profile.profile_image.url
                return JsonResponse({
                    'status': 'success',
                    'message': 'Profile image uploaded successfully',
                    'image_url': file_url,
                    'userid': userid,
                    'filename': image.name  
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'No image file uploaded'
                })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'User not authenticated'
            })
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid request method'
        })

@csrf_exempt
def get_user_profile(request):
    if request.method == 'POST':
        userid = request.POST.get('userid')
        
        if not userid:
            return JsonResponse({'error': 'User ID is required'}, status=400)
        try:
            user_profile = UserProfile.objects.get(user__id=userid)
            profile_data = {
                'user_id': user_profile.user.id,
                'username': user_profile.user.username,
                'email': user_profile.user.email,
                'profile_image_url': user_profile.profile_image.url if user_profile.profile_image else None
            }
            return JsonResponse({'user_profile': profile_data}, status=200)
        
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

    return JsonResponse({'error': 'Invalid request method'}, status=405)