from ..models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import logging
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.views import View
from django.utils.decorators import method_decorator

import logging

logger = logging.getLogger(__name__)

# live
@csrf_exempt
def add_review(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            email = request.POST.get('email')
            review_text = request.POST.get('reviewtxt')
            rating = request.POST.get('rating')
            item_id = request.POST.get('item_id')
            if not name or not email or not review_text or not rating or not item_id:
                return JsonResponse({"error": "All fields are required."}, status=400)
            try:
                rating = int(rating)
            except ValueError:
                return JsonResponse({"error": "Invalid rating value."}, status=400)
            try:
                product = ItemDetail.objects.get(id=item_id)
            except ItemDetail.DoesNotExist:
                return JsonResponse({"error": "Product not found."}, status=404)
            if not request.user.is_authenticated:
                return JsonResponse({"error": "User is not authenticated."}, status=401)
            review = Review.objects.create(
                product=product,
                user=request.user,
                name=name,
                email=email,
                review_text=review_text,
                rating=rating,
            )

            return JsonResponse({"message": "Review added successfully."}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)   





@csrf_exempt
def fetch_reviews(request):
    if request.method == 'GET':
        item_id = request.GET.get('item_id')
        if not item_id:
            return JsonResponse({"error": "Item ID is required."}, status=400)

        try:
            product = ItemDetail.objects.get(id=item_id)
            logger.info(f"Product found: {product}") 
        except ItemDetail.DoesNotExist:
            return JsonResponse({"error": "Product not found."}, status=404)

        reviews = Review.objects.filter(product=product).values(
            'id','name', 'rating', 'review_text', 'created_at', 'likes', 'dislikes'
        )
        print(reviews,'====================')
        average_rating = Review.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg'] or 0
        total_reviews = reviews.count()
        review_data = [
            {   "id": review["id"], 
                "name": review["name"],
                "rating": review["rating"],
                "review_text": review["review_text"],
                "date": review["created_at"].strftime('%B %d, %Y'),
                "likes": review["likes"],
                "dislikes": review["dislikes"],
            }
            for review in reviews
        ]
        return JsonResponse({"reviews": review_data,"average_rating": average_rating,"total_reviews": total_reviews}, status=200)

    return JsonResponse({"error": "Invalid request method."}, status=405)


# @csrf_exempt
# def like_unlike_review(request):
#     """
#     Handle like/dislike functionality for a product review and include the username of the user
#     performing the action, along with review details and user-specific like/dislike counts for each review.
#     """
#     if request.method == 'POST':
#         review_id = request.POST.get('review_id')
#         action = request.POST.get('action')

#         if not review_id or action not in ['like', 'dislike', 'remove']:
#             return JsonResponse({'error': 'Invalid data provided'}, status=400)

#         review = get_object_or_404(Review, id=review_id)

#         if action == 'remove':
#             existing_like_dislike = LikeUnlike.objects.filter(review=review, user=request.user).first()
#             if existing_like_dislike:
#                 existing_like_dislike.delete()
#             else:
#                 return JsonResponse({'error': 'No action to remove'}, status=400)
#         else:
#             existing_like_dislike = LikeUnlike.objects.filter(review=review, user=request.user).first()

#             if existing_like_dislike:
#                 if action == 'like':
#                     existing_like_dislike.liked = True
#                     existing_like_dislike.save()
#                 elif action == 'dislike':
#                     existing_like_dislike.liked = False
#                     existing_like_dislike.save()
#             else:
#                 if action == 'like':
#                     LikeUnlike.objects.create(review=review, user=request.user, liked=True)
#                 elif action == 'dislike':
#                     LikeUnlike.objects.create(review=review, user=request.user, liked=False)

#         likes_count = LikeUnlike.objects.filter(review=review, liked=True).count()
#         dislikes_count = LikeUnlike.objects.filter(review=review, liked=False).count()

#         user_like_dislike = LikeUnlike.objects.filter(review=review, user=request.user).first()

#         review_data = {
#             'review_id': review.id,
#             'review_title': review.name,
#             'review_content': review.review_text,
#             'product_name': review.product.title,
#             'product_id': review.product.id,
#             'likes_count': likes_count,
#             'dislikes_count': dislikes_count,
#             'user_action': 'liked' if user_like_dislike and user_like_dislike.liked else 'disliked' if user_like_dislike else 'none'
#         }

#         print(review_data, '========================')

#         response_data = {
#             "username": request.user.username,
#             "review": review_data
#         }

#         return JsonResponse(response_data)

#     else:
#         return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def like_unlike_review(request):
    """
    Handle like/dislike functionality for a product review and include the username of the user
    performing the action, along with review details and user-specific like/dislike counts for each review.
    """
    if request.method == 'POST':
        review_id = request.POST.get('review_id')
        action = request.POST.get('action')

        if not review_id or action not in ['like', 'dislike', 'remove']:
            return JsonResponse({'error': 'Invalid data provided'}, status=400)

        review = get_object_or_404(Review, id=review_id)
        if action == 'remove':
            existing_like_dislike = LikeUnlike.objects.filter(review=review, user=request.user).first()
            if existing_like_dislike:
                existing_like_dislike.delete()
            else:
                return JsonResponse({'error': 'No action to remove'}, status=400)

        else:
            existing_like_dislike = LikeUnlike.objects.filter(review=review, user=request.user).first()

            if existing_like_dislike:
                if action == 'like':
                    if existing_like_dislike.liked:
                        existing_like_dislike.delete()
                    else:
                        existing_like_dislike.liked = True
                        existing_like_dislike.save()
                elif action == 'dislike':
                    if existing_like_dislike.liked:
                        existing_like_dislike.liked = False
                        existing_like_dislike.save()
                    else:
                        existing_like_dislike.save()
            else:
                if action == 'like':
                    LikeUnlike.objects.create(review=review, user=request.user, liked=True)
                elif action == 'dislike':
                    LikeUnlike.objects.create(review=review, user=request.user, liked=False)

        likes_count = LikeUnlike.objects.filter(review=review, liked=True).count()
        dislikes_count = LikeUnlike.objects.filter(review=review, liked=False).count()

        user_like_dislike = LikeUnlike.objects.filter(review=review, user=request.user).first()
        review_data = {
            'review_id': review.id,
            'review_title': review.name,
            'review_content': review.review_text,
            'product_name': review.product.title,
            'product_id': review.product.id,
            'likes_count': likes_count,
            'dislikes_count': dislikes_count,
            'user_action': 'liked' if user_like_dislike and user_like_dislike.liked else 'disliked' if user_like_dislike else 'none'
        }

        response_data = {
            "username": request.user.username,
            "review": review_data
        }

        return JsonResponse(response_data)

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def count_likes_dislikes(request):
    """
    Handle the retrieval of total likes and dislikes count for a specific review based on review_id.
    """
    if request.method == 'POST':
        review_id = request.POST.get('review_id')

        if not review_id:
            return JsonResponse({'error': 'Review ID is required'}, status=400)

        review = get_object_or_404(Review, id=review_id)
        likes_count = LikeUnlike.objects.filter(review=review, liked=True).count()
        dislikes_count = LikeUnlike.objects.filter(review=review, liked=False).count()

        review_data = {
            'review_id': review.id,
            'likes_count': likes_count,
            'dislikes_count': dislikes_count
        }

        response_data = {
            "review": review_data
        }

        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
