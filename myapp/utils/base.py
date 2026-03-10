from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time
from django.views.decorators.csrf import csrf_exempt
from ..models import *




def fetch_reviews(url, max_reviews=20):
    reviews_data = []
    seen_names = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_selector('.jftiEf')
        def scroll_page():
            page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        scroll_times = 5
        previous_reviews_count = 0
        new_reviews_count = 0

        for _ in range(scroll_times):
            scroll_page()
            page.wait_for_selector('.jftiEf')
            html = page.content()
            soup = BeautifulSoup(html, 'html.parser')
            reviews = soup.find_all('div', {'class': 'jftiEf'})
            new_reviews_count = len(reviews)
            if new_reviews_count == previous_reviews_count or len(reviews_data) >= max_reviews:
                break
            previous_reviews_count = new_reviews_count
            for review in reviews:
                name = review.find('div', class_='d4r55').text.strip() if review.find('div', class_='d4r55') else 'N/A'
                if name in seen_names:
                    continue
                seen_names.add(name)

                filled_stars = review.find_all('span', class_='hCCjke google-symbols NhBTye elGi1d')
                rating = len(filled_stars)
                review_content = review.find('span', class_='wiI7pd').text.strip() if review.find('span', class_='wiI7pd') else 'N/A'
                img_tag = review.find('img', class_='NBa7we')
                img_url = img_tag['src'] if img_tag else 'N/A'

                review_dict = {
                    'name': name,
                    'rating': rating,
                    'review_content': review_content,
                    'image_url': img_url
                }
                reviews_data.append(review_dict)
                print(review_dict)
        browser.close()
    return reviews_data




@csrf_exempt
def share_products(request):
    if request.method=='POST':
        product_id=request.POST.get("item_id")
        product = ItemDetail.objects.filter(id=product_id).first()
        print(product, '===================================')
        if not product:
            return JsonResponse({'error': 'Product not found'}, status=404)
        context = {
            'image1': product.image1.url if product.image1 else None
        }

        return JsonResponse({"status":200,'message':context})
    return JsonResponse({"status":400,'message':"method not allowed"})

from django.http import HttpResponse

@csrf_exempt
def base_index(request):
    if request.method == 'POST':
        url = request.POST.get('url', None)
        if not url:
            return JsonResponse({"status":400,"message":"URL parameter is required"})
        reviews = fetch_reviews(url)
        return JsonResponse({"status":200,"data":reviews}, safe=False)
    return render(request,'index.html')
    # html_content = """
    # <!DOCTYPE html>
    # <html>
    #     <head>
    #         <title>Site is down for maintenance</title>
    #         <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    #         <meta name="viewport" content="width=device-width, initial-scale=1" />
    #         <style type="text/css">
    #             body { text-align: center; padding: 10%; font: 20px Helvetica, sans-serif; color: #333; }
    #             h1 { font-size: 50px; margin: 0; }
    #             article { display: block; text-align: left; max-width: 650px; margin: 0 auto; }
    #             a { color: #dc8100; text-decoration: none; }
    #             a:hover { color: #333; text-decoration: none; }
    #             @media only screen and (max-width : 480px) {
    #                 h1 { font-size: 40px; }
    #             }
    #         </style>
    #     </head>
    #     <body>
    #         <article>
    #             <h1>Site is temporarily unavailable.</h1>
    #             <p>Scheduled maintenance is currently in progress. Please check back soon.</p>
    #             <p>We apologize for any inconvenience.</p>
    #             <p id="signature">&mdash; <a href="mailto:[Email]">[Name]</a></p>
    #         </article>
    #     </body>
    # </html>
    # """
    # return HttpResponse(html_content)




def shipping_policy(request):
    return render(request,'shipping-policy.html')

def privacy_policy(request):
    return render(request,'privacy-policy.html')


def refund_returns_policy(request):
    return render(request,'refund-returns-policy.html')


def cancellation_policy(request):
    return render(request,'cancellation-policy.html')

@csrf_exempt
def profile_base(request):
    return render(request,'profile.html')


def forgate_password(request):
    return render(request,'forget-password-merge.html')


def pdfgenerateHtml(request):
    return render(request,'bill-pdf.html')


def appointment_form(request):
    return render(request,'form-appointment.html')
    # return render(request,'onsite-visit-pdf.html')


