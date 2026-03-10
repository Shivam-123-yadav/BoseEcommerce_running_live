import pandas as pd
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
from ..models import *
from django.core.files.storage import FileSystemStorage
import os
from django.core.files import File
import csv
from io import StringIO
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

# live
# this is for image uploading

# @csrf_exempt
# def upload_csv(request):
#     if request.method == 'POST' and request.FILES.get('file'):
#         csv_file = request.FILES['file']
        
#         if not csv_file.name.endswith('.csv'):
#             return JsonResponse({'status': 400, 'message': 'Only CSV files are allowed.'}, status=400)
        
#         fs = FileSystemStorage()
#         filename = fs.save(csv_file.name, csv_file)
#         file_path = fs.path(filename)

#         try:
#             data_upload_instance, created = Dataupload.objects.get_or_create(
#                 file=csv_file,
#                 uploaded_by=request.user.username,
#                 user=request.user
#             )
            
#             df = pd.read_csv(file_path, encoding='ISO-8859-1')
#             # df = pd.read_csv(file_path, encoding='utf-8')

#             for index, row in df.iterrows():
#                 item_detail = ItemDetail(
#                     title=str(row.get('title', '')).strip(),
#                     availability=row.get('availability',''),
#                     mrp_price=row.get('MRP Price', 0.00),
#                     discount_percentage=row.get('discount_percentage', 0.00),
#                     shipping_charges=row.get('shipping charges', 0.00),
#                     user=request.user,
#                     dataupload=data_upload_instance,
#                     category=row.get('category', 'otherproducts'),
#                     box_content=str(row.get('box content', '')).strip(),
#                     dimension_weight=str(row.get('dimension weight', '')).strip(),
#                     materials=str(row.get('materials', '')).strip(),
#                     battery=str(row.get('battery', '')).strip(),
#                     bluetooth=str(row.get('bluetooth', '')).strip(),
#                     inputs=str(row.get('inputs', '')).strip(),
#                     microphones=str(row.get('microphones', '')).strip(),
#                     controls=str(row.get('controls', '')).strip(),
#                     compatible_app=str(row.get('compatible app', '')).strip(),
#                     additions_informations=str(row.get('additions informations', '')).strip(),
#                     heading1=str(row.get('heading1', '')).strip(),
#                     heading2=str(row.get('heading2', '')).strip(),
#                     heading3=str(row.get('heading3', '')).strip(),
#                     heading4=str(row.get('heading4', '')).strip(),
#                     heading5=str(row.get('heading5', '')).strip(),
#                     heading6=str(row.get('heading6', '')).strip(),
#                     overview=str(row.get('overview','')).strip(),
#                     compability=str(row.get('compability','')).strip()
#                 )
#                 item_detail.save()
#                 for i in range(1, 6):
#                     image_path = row.get(f'image{i}', '')  
#                     print(image_path,'========================')
#                     if isinstance(image_path, str): 
#                         image_path = image_path.strip()
#                         print(image_path,'============================================================')
#                     else:
#                         image_path = ''
                    
#                     if image_path: 
#                         if os.path.exists(image_path):
#                             media_path = os.path.join('media', 'allproducts', item_detail.category)
#                             os.makedirs(media_path, exist_ok=True)

#                             with open(image_path, 'rb') as img_file:
#                                 image_file_name = os.path.basename(image_path)
#                                 main_image_path = os.path.join(media_path, image_file_name)
#                                 with open(main_image_path, 'wb') as destination:
#                                     destination.write(img_file.read())
#                                 setattr(item_detail, f'image{i}', os.path.join('allproducts', item_detail.category, image_file_name))
#                 item_detail.save()
#                 color_definitions = {
#                     "alpine-sage":["image1_alpine-sage","image2_alpine-sage","image3_alpine-sage","image4_alpine-sage","image5_alpine-sage"],
#                     "aquatic-blue":["image1_aquatic-blue","image2_aquatic-blue","image3_aquatic-blue","image4_aquatic-blue","image5_aquatic-blue"],
#                     "arctic-white":["image1_arctic-white","image2_arctic-white","image3_arctic-white","image4_arctic-white","image5_arctic-white"],
#                     "baltic-blue":["image1_baltic-blue","image2_baltic-blue","image3_baltic-blue","image4_baltic-blue","image5_baltic-blue"],
#                     "black": ["image1_black", "image2_black", "image3_black", "image4_black", "image5_black"],
#                     "blue":["image1_blue","image2_blue","image3_blue","image4_blue","image5_blue"],
#                     "blue-dusk":["image1_blue-dusk","image2_blue-dusk","image3_blue-dusk","image4_blue-dusk","image5_blue-dusk"],
#                     "bright-orange":["image1_bright-orange","image2_bright-orange","image3_bright-orange","image4_bright-orange","image5_bright-orange"],
#                     "carmine-red":["image1_carmine-red","image2_carmine-red","image3_carmine-red","image4_carmine-red","image5_carmine-red"],
#                     "charcoal-black":["image1_charcoal-black","image2_charcoal-black","image3_charcoal-black","image4_charcoal-black","image5_charcoal-black"],
#                     "chilled-lilac":["image1_chilled-lilac","image2_chilled-lilac","image3_chilled-lilac","image4_chilled-lilac","image5_chilled-lilac"],
#                     "coral-red":["image1_coral-red","image2_coral-red","image3_coral-red","image4_coral-red","image5_coral-red"],
#                     "cypress-green":["image1_cypress-green","image2_cypress-green","image3_cypress-green","image4_cypress-green","image5_cypress-green"],
#                     "diamond":["image1_diamond","image2_diamond","image3_diamond","image4_diamond","image5_diamond"],
#                     "eclipse-gray":["image1_eclipse-gray","image2_eclipse-gray","image3_eclipse-gray","image4_eclipse-gray","image5_eclipse-gray"],
#                     "glacier-white":["image1_glacier-white","image2_glacier-white","image3_glacier-white","image4_glacier-white","image5_glacier-white"],
#                     "green": ["image1_green", "image2_green", "image3_green", "image4_green", "image5_green"],
#                     "grey":["image1_grey","image2_grey","image3_grey","image4_grey","image5_grey"],
#                     "lunar-blue":["image1_lunar-blue","image2_lunar-blue","image3_lunar-blue","image4_lunar-blue","image5_lunar-blue"],
#                     "luxe-silver":["image1_luxe-silver","image2_luxe-silver","image3_luxe-silver","image4_luxe-silver","image5_luxe-silver"],
#                     "midnight-blue":["image1_midnight-blue","image2_midnight-blue","image3_midnight-blue","image4_midnight-blue","image5_midnight-blue"],
#                     "moonstone-blue":["image1_moonstone-blue","image2_moonstone-blue","image3_moonstone-blue","image4_moonstone-blue","image5_moonstone-blue"],
#                     "navy-blue":["image1_navy-blue","image2_navy-blue","image3_navy-blue","image4_navy-blue","image5_navy-blue"],
#                     "polar-white":["image1_polar-white","image2_polar-white","image3_polar-white","image4_polar-white","image5_polar-white"],
#                     "red":["image1_red","image2_red","image3_red","image4_red","image5_red"],
#                     "sandstone":["image1_sandstone","image2_sandstone","image3_sandstone","image4_sandstone","image5_sandstone"],
#                     "silver":["image1_silver","image2_silver","image3_silver","image4_silver","image5_silver"],
#                     "soapstone":["image1_soapstone","image2_soapstone","image3_soapstone","image4_soapstone","image5_soapstone"],
#                     "soft-black":["image1_soft-black","image2_soft-black","image3_soft-black","image4_soft-black","image5_soft-black"],
#                     "stone-blue":["image1_stone-blue","image2_stone-blue","image3_stone-blue","image4_stone-blue","image5_stone-blue"],
#                     "triple-black":["image1_triple-black","image2_triple-black","image3_triple-black","image4_triple-black","image5_triple-black"],
#                     "white":["image1_white","image2_white","image3_white","image4_white","image5_white"],
#                     "white-smoke":["image1_white-smoke","image2_white-smoke","image3_white-smoke","image5_white-smoke"],
#                     "yellow-citron":["image1_yellow-citron","image2_yellow-citron","image3_yellow-citron","image4_yellow-citron","image5_yellow-citron"]
#                 }
#                 for color_name, image_columns in color_definitions.items():
#                     color_images = []
                    
#                     for column in image_columns:
#                         image_path = row.get(column, None)
#                         if isinstance(image_path, str) and image_path:
#                             image_path = image_path.strip()
#                             if os.path.exists(image_path):
#                                 media_path = os.path.join('media', 'allproducts', item_detail.category, color_name)
#                                 os.makedirs(media_path, exist_ok=True)
#                                 with open(image_path, 'rb') as img_file:
#                                     image_file_name = os.path.basename(image_path)
#                                     color_image_path = os.path.join(media_path, image_file_name)
                                    
#                                     with open(color_image_path, 'wb') as destination:
#                                         destination.write(img_file.read()) 
#                                     color_images.append(os.path.join('allproducts', item_detail.category, color_name, image_file_name))
#                     if color_images:
#                         TypeColor.objects.create(
#                             product=item_detail,
#                             color_name=color_name,
#                             image1=color_images[0] if len(color_images) > 0 else None,
#                             image2=color_images[1] if len(color_images) > 1 else None,
#                             image3=color_images[2] if len(color_images) > 2 else None,
#                             image4=color_images[3] if len(color_images) > 3 else None,
#                             image5=color_images[4] if len(color_images) > 4 else None
#                         )
#             os.remove(file_path)
#             return JsonResponse({'status': 200, 'message': 'Successfully uploaded CSV file.'}, status=200)
#         except Exception as e:
#             if os.path.exists(file_path):
#                 os.remove(file_path)
#             return JsonResponse({'status': 500, 'message': f'Error processing file: {str(e)}'}, status=500)

@csrf_exempt
def upload_csv(request):
    if request.method == 'POST' and request.FILES.get('file'):
        csv_file = request.FILES['file']
        
        if not csv_file.name.endswith('.csv'):
            return JsonResponse({'status': 400, 'message': 'Only CSV files are allowed.'}, status=400)
        
        fs = FileSystemStorage()
        filename = fs.save(csv_file.name, csv_file)
        file_path = fs.path(filename)

        try:
            data_upload_instance, created = Dataupload.objects.get_or_create(
                file=csv_file,
                uploaded_by=request.user.username,
                user=request.user
            )
            
            df = pd.read_csv(file_path, encoding='ISO-8859-1')

            df['MRP Price'] = pd.to_numeric(df['MRP Price'], errors='coerce').fillna(0.00)
            df['discount_percentage'] = pd.to_numeric(df['discount_percentage'], errors='coerce').fillna(0.00)
            df['shipping charges'] = pd.to_numeric(df['shipping charges'], errors='coerce').fillna(0.00)

            for index, row in df.iterrows():
                title = str(row.get('title', '')).strip()
                item_detail, created = ItemDetail.objects.update_or_create(
                    title=title,
                    defaults={
                        'availability': row.get('availability', ''),
                        'mrp_price': row.get('MRP Price', 0.00),
                        'discount_percentage': row.get('discount_percentage', 0.00),
                        'shipping_charges': row.get('shipping charges', 0.00),
                        'user': request.user,
                        'dataupload': data_upload_instance,
                        'category': row.get('category', 'otherproducts'),
                        'box_content': str(row.get('box content', '')).strip(),
                        'dimension_weight': str(row.get('dimension weight', '')).strip(),
                        'materials': str(row.get('materials', '')).strip(),
                        'battery': str(row.get('battery', '')).strip(),
                        'bluetooth': str(row.get('bluetooth', '')).strip(),
                        'inputs': str(row.get('inputs', '')).strip(),
                        'microphones': str(row.get('microphones', '')).strip(),
                        'controls': str(row.get('controls', '')).strip(),
                        'compatible_app': str(row.get('compatible app', '')).strip(),
                        'additions_informations': str(row.get('additions informations', '')).strip(),
                        'heading1': str(row.get('heading1', '')).strip(),
                        'heading2': str(row.get('heading2', '')).strip(),
                        'heading3': str(row.get('heading3', '')).strip(),
                        'heading4': str(row.get('heading4', '')).strip(),
                        'heading5': str(row.get('heading5', '')).strip(),
                        'heading6': str(row.get('heading6', '')).strip(),
                        'overview': str(row.get('overview', '')).strip(),
                        'compability': str(row.get('compability', '')).strip(),
                    }
                )

                for i in range(1, 6):
                    image_path = row.get(f'image{i}', '')  
                    print(image_path,'========================')
                    if isinstance(image_path, str): 
                        image_path = image_path.strip()
                        print(image_path,'============================================================')
                    else:
                        image_path = ''
                    
                    if image_path: 
                        if os.path.exists(image_path):
                            media_path = os.path.join('media', 'allproducts', item_detail.category)
                            os.makedirs(media_path, exist_ok=True)

                            with open(image_path, 'rb') as img_file:
                                image_file_name = os.path.basename(image_path)
                                main_image_path = os.path.join(media_path, image_file_name)
                                with open(main_image_path, 'wb') as destination:
                                    destination.write(img_file.read())
                                setattr(item_detail, f'image{i}', os.path.join('allproducts', item_detail.category, image_file_name))
                item_detail.save()

                color_definitions = {
                    "alpine-sage":["image1_alpine-sage","image2_alpine-sage","image3_alpine-sage","image4_alpine-sage","image5_alpine-sage"],
                    "aquatic-blue":["image1_aquatic-blue","image2_aquatic-blue","image3_aquatic-blue","image4_aquatic-blue","image5_aquatic-blue"],
                    "arctic-white":["image1_arctic-white","image2_arctic-white","image3_arctic-white","image4_arctic-white","image5_arctic-white"],
                    "baltic-blue":["image1_baltic-blue","image2_baltic-blue","image3_baltic-blue","image4_baltic-blue","image5_baltic-blue"],
                    "black": ["image1_black", "image2_black", "image3_black", "image4_black", "image5_black"],
                    "blue":["image1_blue","image2_blue","image3_blue","image4_blue","image5_blue"],
                    "blue-dusk":["image1_blue-dusk","image2_blue-dusk","image3_blue-dusk","image4_blue-dusk","image5_blue-dusk"],
                    "bright-orange":["image1_bright-orange","image2_bright-orange","image3_bright-orange","image4_bright-orange","image5_bright-orange"],
                    "carmine-red":["image1_carmine-red","image2_carmine-red","image3_carmine-red","image4_carmine-red","image5_carmine-red"],
                    "charcoal-black":["image1_charcoal-black","image2_charcoal-black","image3_charcoal-black","image4_charcoal-black","image5_charcoal-black"],
                    "chilled-lilac":["image1_chilled-lilac","image2_chilled-lilac","image3_chilled-lilac","image4_chilled-lilac","image5_chilled-lilac"],
                    "coral-red":["image1_coral-red","image2_coral-red","image3_coral-red","image4_coral-red","image5_coral-red"],
                    "cypress-green":["image1_cypress-green","image2_cypress-green","image3_cypress-green","image4_cypress-green","image5_cypress-green"],
                    "diamond":["image1_diamond","image2_diamond","image3_diamond","image4_diamond","image5_diamond"],
                    "eclipse-gray":["image1_eclipse-gray","image2_eclipse-gray","image3_eclipse-gray","image4_eclipse-gray","image5_eclipse-gray"],
                    "glacier-white":["image1_glacier-white","image2_glacier-white","image3_glacier-white","image4_glacier-white","image5_glacier-white"],
                    "green": ["image1_green", "image2_green", "image3_green", "image4_green", "image5_green"],
                    "grey":["image1_grey","image2_grey","image3_grey","image4_grey","image5_grey"],
                    "lunar-blue":["image1_lunar-blue","image2_lunar-blue","image3_lunar-blue","image4_lunar-blue","image5_lunar-blue"],
                    "luxe-silver":["image1_luxe-silver","image2_luxe-silver","image3_luxe-silver","image4_luxe-silver","image5_luxe-silver"],
                    "midnight-blue":["image1_midnight-blue","image2_midnight-blue","image3_midnight-blue","image4_midnight-blue","image5_midnight-blue"],
                    "moonstone-blue":["image1_moonstone-blue","image2_moonstone-blue","image3_moonstone-blue","image4_moonstone-blue","image5_moonstone-blue"],
                    "navy-blue":["image1_navy-blue","image2_navy-blue","image3_navy-blue","image4_navy-blue","image5_navy-blue"],
                    "polar-white":["image1_polar-white","image2_polar-white","image3_polar-white","image4_polar-white","image5_polar-white"],
                    "red":["image1_red","image2_red","image3_red","image4_red","image5_red"],
                    "sandstone":["image1_sandstone","image2_sandstone","image3_sandstone","image4_sandstone","image5_sandstone"],
                    "silver":["image1_silver","image2_silver","image3_silver","image4_silver","image5_silver"],
                    "soapstone":["image1_soapstone","image2_soapstone","image3_soapstone","image4_soapstone","image5_soapstone"],
                    "soft-black":["image1_soft-black","image2_soft-black","image3_soft-black","image4_soft-black","image5_soft-black"],
                    "stone-blue":["image1_stone-blue","image2_stone-blue","image3_stone-blue","image4_stone-blue","image5_stone-blue"],
                    "triple-black":["image1_triple-black","image2_triple-black","image3_triple-black","image4_triple-black","image5_triple-black"],
                    "white":["image1_white","image2_white","image3_white","image4_white","image5_white"],
                    "white-smoke":["image1_white-smoke","image2_white-smoke","image3_white-smoke","image5_white-smoke"],
                    "yellow-citron":["image1_yellow-citron","image2_yellow-citron","image3_yellow-citron","image4_yellow-citron","image5_yellow-citron"]
                }
                
                for color_name, image_columns in color_definitions.items():
                    color_images = []

                    for column in image_columns:
                        image_path = row.get(column, None)
                        if isinstance(image_path, str) and image_path:
                            image_path = image_path.strip()
                            print(image_path, 'pathhhhhhhhhhhhhhhhhhhhhhh')
                            if os.path.exists(image_path):
                                media_path = os.path.join('media', 'allproducts', item_detail.category, color_name)
                                os.makedirs(media_path, exist_ok=True)
                                image_file_name = os.path.basename(image_path)
                                color_image_path = os.path.join(media_path, image_file_name)
                                print(color_image_path, '==================================================')
                                if os.path.exists(color_image_path):
                                    print(f"Image {image_file_name} already exists. It will be overwritten.")
                                    os.remove(color_image_path)

                                with open(image_path, 'rb') as img_file:
                                    with open(color_image_path, 'wb') as destination:
                                        destination.write(img_file.read())
                                color_images.append(os.path.join('allproducts', item_detail.category, color_name, image_file_name))
                            else:
                                print(f"Image path {image_path} does not exist.")
                    
                        if color_images:
                            type_color_instance = TypeColor.objects.filter(product=item_detail, color_name=color_name).first()
                            if type_color_instance:
                                for i in range(1, 6):
                                    if len(color_images) >= i:
                                        image_field = f"image{i}"
                                        current_image = getattr(type_color_instance, image_field, None)
                                        new_image = color_images[i - 1] if len(color_images) >= i else None
                                        
                                        if current_image != new_image:
                                            setattr(type_color_instance, image_field, new_image)
                                type_color_instance.save()
                            else:
                                TypeColor.objects.create(
                                    product=item_detail,
                                    color_name=color_name,
                                    image1=color_images[0] if len(color_images) > 0 else None,
                                    image2=color_images[1] if len(color_images) > 1 else None,
                                    image3=color_images[2] if len(color_images) > 2 else None,
                                    image4=color_images[3] if len(color_images) > 3 else None,
                                    image5=color_images[4] if len(color_images) > 4 else None
                                )

            
            os.remove(file_path)
            return JsonResponse({'status': 200, 'message': 'Successfully uploaded CSV file.'}, status=200)

        except Exception as e:
            if os.path.exists(file_path):
                os.remove(file_path)
            return JsonResponse({'status': 500, 'message': f'Error processing file: {str(e)}'}, status=500)

@csrf_exempt
def filterations_color(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        try:
            product = ItemDetail.objects.get(id=product_id)
            colors = TypeColor.objects.filter(product=product)
            color_data = []
            for color in colors:
                color_data.append({
                    'id': color.id,
                    'product_id': color.product.id,
                    'color_name': color.color_name,
                    'image1': color.image1.url if color.image1 else None,
                    'image2': color.image2.url if color.image2 else None,
                    'image3': color.image3.url if color.image3 else None,
                    'image4': color.image4.url if color.image4 else None,
                    'image5': color.image5.url if color.image5 else None,
                })
            return JsonResponse({
                'status': 'success',
                'product': {
                    'id': product.id,
                },
                'colors': color_data,
            })
        except ItemDetail.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Product not found.'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

    