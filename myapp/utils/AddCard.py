from django.http import JsonResponse
from ..models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render,redirect
from django.http import HttpResponseNotFound
from django.http import Http404

# live 

@csrf_exempt
def add_to_cart(request):
    try:
        if request.method == 'POST':
            if not request.user.is_authenticated:
                return JsonResponse({'status': 404, 'message': 'Please login to continue.'})
            item_id = request.POST.get('item_id')
            quantity = int(request.POST.get('quantity', 1))
            image_url = request.POST.get('image_url')
            color_name = request.POST.get('color_name')

            try:
                item = get_object_or_404(ItemDetail, id=item_id)
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': 'Item not found'}, status=404)
            cart, created = Cart.objects.get_or_create(user=request.user)
            existing_cart_item = CartItem.objects.filter(cart=cart, item=item).first()
            if existing_cart_item:
                return JsonResponse({
                    'status': 'error',
                    'message': f"{item.title} is already in your cart. You cannot add it again."
                }, status=400)
            cart_item = CartItem(cart=cart, item=item, quantity=quantity, 
                                 type_color_image_url=image_url, type_color_name=color_name)
            cart_item.save()
            cart_items = CartItem.objects.filter(cart=cart)
            cart_item_details = [
                {
                    'item_id': cart_item.item.id,
                    'item_title': cart_item.item.title,
                    'quantity': cart_item.quantity,
                    'image_url': cart_item.type_color_image_url,
                    'color_name': cart_item.type_color_name
                }
                for cart_item in cart_items
            ]

            total_cart_value = cart.total_cart_value()
            response_data = {
                'status': 'success',
                'message': f"{item.title} added to cart!",
                'item_id': item.id,
                'quantity': cart_item.quantity,
                'total_cart_value': total_cart_value,
                'cart_items': cart_item_details 
            }
            return JsonResponse(response_data)

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': 'An error occurred. Please try again.'}, status=500)


# @csrf_exempt
# def countaddcard(request):
#     cart = get_object_or_404(Cart, user=request.user)
#     cart_items = CartItem.objects.filter(cart=cart)
#     product_count = sum(cart_item.quantity for cart_item in cart_items)
#     return JsonResponse({'status':200,'message':'successfully','count':product_count})

@csrf_exempt
def countaddcard(request):
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        return JsonResponse({'status': 404, 'message': 'Cart not found for this user.'}, status=404)
    cart_items = CartItem.objects.filter(cart=cart)
    product_count = sum(cart_item.quantity for cart_item in cart_items)

    return JsonResponse({'status': 200, 'message': 'successfully', 'count': product_count})


@csrf_exempt
def UpdateAddcardDetails(request):
    if request.method == 'POST':
        user_id=request.user.id
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': 'Please log in to update your cart.'}, status=403)

        item_id = request.POST.get('item_id')
        quantity = int(request.POST.get('quantity', 0))
        print(item_id,quantity,'===================')

        if item_id is None:
            return JsonResponse({'status': 'error', 'message': 'Item ID is required.'}, status=400)
        cart = get_object_or_404(Cart, user=request.user)
        try:
            cart_item = get_object_or_404(CartItem, cart=cart, item=item_id)
        except CartItem.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Item not found in cart.'}, status=404)

        if quantity <= 0:
            removed_quantity = cart_item.quantity
            cart_item.delete()
            response_data = {
                'status': 'success',
                'message': "Item removed from cart.",
                'item_id': item_id,
                'removed_quantity': removed_quantity,
                'total_cart_value': cart.total_cart_value(),
            }
        else:
            cart_item.quantity = quantity
            cart_item.save()
            response_data = {
                'status': 'success',
                'message': f"Quantity updated for {cart_item.item.title}.",
                'item_id': item_id,
                'quantity': cart_item.quantity,
                'total_cart_value': cart.total_cart_value(),
            }

        return JsonResponse(response_data)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)


@csrf_exempt
def get_cart_details(user):
    """Fetch cart details and prepare context."""
    try:
        cart = get_object_or_404(Cart, user=user)
    except Http404:
        return {"error": "Cart not found for the user."}

    cart_items = CartItem.objects.filter(cart=cart)

    if not cart_items.exists():
        return {"message": "Cart is empty.", "total_value": 0, "items": []}

    items = []
    total_value = 0

    for cart_item in cart_items:
        try:
            item = cart_item.item 
        except ItemDetail.DoesNotExist:
            return HttpResponseNotFound(f"Item with ID {cart_item.item_id} does not exist.")
        
        item_total = cart_item.quantity * item.mrp_price+item.shipping_charges
        total_value += item_total

        items.append({
            'item_id': item.id,
            'title': item.title,
            'slug':item.slug,
            'quantity': cart_item.quantity,
            'mrp_price': item.mrp_price,
            'discount_percentage': item.discount_percentage,
            'discount_amount': item.discount_amount,
            'final_price': item.final_price,
            'total_price': item_total,
            'shipping_charge': item.shipping_charges,
            'image': item.image1.url.replace('/media', '', 1) if item.image1 else None,
            'color_image_url': cart_item.type_color_image_url if cart_item.type_color_image_url else None,  # Default to None
            'color_name': cart_item.type_color_name if cart_item.type_color_name else None,  # Default to None
        })
        print(item,'===============ss')

    return {
        'cart': cart,
        'cart_items': items,
        'total_cart_value': total_value,
    }


@csrf_exempt
def viewAddDetails(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    context = get_cart_details(request.user)
    return render(request, 'myapp/shopping-cart.html', context)


@csrf_exempt
def chekout_now(request):
    user = request.user
    if not user.is_authenticated:
        return HttpResponseNotFound("User is not authenticated.")
    cart = get_object_or_404(Cart, user=user)
    cart_items = CartItem.objects.filter(cart=cart)

    items = []
    total_value = 0
    total_subtotal = 0
    total_discount = 0
    total_shipping_charge = 0
    for cart_item in cart_items:
        try:
            item = cart_item.item 
        except ItemDetail.DoesNotExist:
            return HttpResponseNotFound(f"Item with ID {cart_item.item_id} does not exist.")
        
        item_total = cart_item.quantity * item.final_price
        total_value += item_total

        total_subtotal += item.mrp_price * cart_item.quantity
        total_discount += item.discount_amount * cart_item.quantity
        total_shipping_charge += item.shipping_charges
        
        items.append({
            'id': item.id, 
            'slug': item.slug,
            'title': item.title,
            'mrp_price': item.mrp_price,
            'quantity': cart_item.quantity, 
            'image': item.image1.url.replace('/media', '', 1) if item.image1 else None,
            'color_image_url': cart_item.type_color_image_url if cart_item.type_color_image_url else None,  # Default to None
            'color_name': cart_item.type_color_name if cart_item.type_color_name else None,  # Default to None
        })
    final_total_price = total_subtotal - total_discount + total_shipping_charge
    context = {
        'cart': cart,
        'cart_items': items,
        'total_subtotal': total_subtotal,
        'total_discount': total_discount,
        'total_shipping_charge': total_shipping_charge,
        'final_total_price': final_total_price,
    }
    return render(request, 'myapp/checkout.html', context)



@csrf_exempt
def add_to_wishlist(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'User not logged in'}, status=401)
        item_id = request.POST.get('item_id')    
        item = ItemDetail.objects.get(id=item_id)
       
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        wish_item, created = WishlistItems.objects.get_or_create(wish=wishlist, item=item)

        if created:
            return JsonResponse({'status':200,'message': 'Item added to wishlist'})
        else:
            return JsonResponse({'message': 'Item already in wishlist'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def get_wishlist_count(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User not logged in'}, status=401)
    count = Wishlist.objects.filter(user=request.user).count()
    return JsonResponse({'wishlist_count': count})

@csrf_exempt
def countwishcard(request):
    wish = get_object_or_404(Wishlist, user=request.user)
    wish_items = WishlistItems.objects.filter(wish=wish)
    wish_count = wish_items.count()
    return JsonResponse({'status': 200, 'message': 'successfully', 'count': wish_count})



def wish_details(user):
    """Fetch cart details and prepare context."""
    try:
        wish = Wishlist.objects.get(user=user)
    except Wishlist.DoesNotExist:
        return {
            'wish': None,
            'wish_items': [],
            'message': 'No wishlist found for this user.'
        }

    wish_items = WishlistItems.objects.filter(wish=wish)

    items = []

    for wish_item in wish_items:
        try:
            item = wish_item.item  
        except ItemDetail.DoesNotExist:
            return HttpResponse(f"Item with ID {wish_item.item_id} does not exist.", status=404)
        
        item_total = item.final_price

        items.append({
            'item_id': item.id,
            'title': item.title,
            'mrp_price': item.mrp_price,
            'discount_percentage': item.discount_percentage,
            'discount_amount': item.discount_amount,
            'final_price': item.final_price,
            'total_price': item_total,
            'shipping_charge': item.shipping_charges,
            'image': item.image1.url.replace('/media', '', 1) if item.image1 else None,
            'slug': item.slug
        })

    return {
        'wish': wish,
        'wish_items': items,
    }

@csrf_exempt
def wishlist(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    context = wish_details(request.user)
    return render(request, 'myapp/wishlist.html', context)


@csrf_exempt
def update_wish_list_details(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': 'Please log in to update your wishlist.'}, status=403)

        item_id = request.POST.get('item_id')
        if not item_id:
            return JsonResponse({'status': 'error', 'message': 'Item ID is required.'}, status=400)
        try:
            wishlist = Wishlist.objects.get(user=request.user)
        except Wishlist.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Wishlist not found.'}, status=404)
        try:
            wish_item = WishlistItems.objects.get(wish=wishlist, item_id=item_id)
            wish_item.delete()
            return JsonResponse({'status': 'success', 'message': 'Item removed from wishlist.'})
        except WishlistItems.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Item not found in wishlist.'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

