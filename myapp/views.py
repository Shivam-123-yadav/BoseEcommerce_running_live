from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from django.http import JsonResponse
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time
from django.http import HttpResponse
# ============================ feedback google========================
from django.http import JsonResponse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time



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


def service_panel(request):
    return render(request,'service.html')

def file_upload(request):
    return render(request,'file_upload.html')


def abouts_us(request):
    return render(request,'aboutus.html')

import json
import logging

logger = logging.getLogger(__name__)


def contacte_us(request):
    return render(request,'contactus.html')

def test_404(request):
    return render(request, "404.html", status=404)  



# @csrf_exempt
# def cashfree_webhook(request):
#     if request.method != "POST":
#         return JsonResponse({'error': 'Invalid method'}, status=405)

#     try:
#         data = json.loads(request.body.decode('utf-8'))
#         print(data,'========================================')
#         logger.info(f"[Cashfree Webhook] Data received: {data}")
#         # Optional: Do basic order ID logging here
#         order_id = data.get("order", {}).get("order_id")
#         tx_status = data.get("order", {}).get("status")

#         # Save to DB or queue for processing later
#         return JsonResponse({'status': 'ok'}, status=200)

#     except Exception as e:
#         logger.error(f"Error in webhook: {str(e)}")
#         return JsonResponse({'error': 'Invalid payload'}, status=400)
@csrf_exempt
def cashfree_webhook(request):
    if request.method != "POST":
        return JsonResponse({'error': 'Invalid method'}, status=405)

    try:
        raw_body = request.body.decode('utf-8')
        print("Raw POST Body:", raw_body)  # <-- Print full POST body as-is from Cashfree

        # Optionally log this
        logger.info(f"[Cashfree Webhook] Raw POST body: {raw_body}")

        data = json.loads(raw_body)
        print("Parsed JSON Data:", data)

        order_id = data.get("order", {}).get("order_id")
        tx_status = data.get("order", {}).get("status")
        print(f"Order ID: {order_id}, Status: {tx_status}")

        return JsonResponse({'status': 'ok'}, status=200)

    except Exception as e:
        logger.error(f"Error in webhook: {str(e)}")
        return JsonResponse({'error': 'Invalid payload'}, status=400)


def scrape_google_reviews(request):
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-extensions')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    reviews_json = []
    try:
        url = "https://www.google.com/maps/place/Bose+Service+Center/@19.1361556,72.8009109,15z/data=!4m8!3m7!1s0x3be7b7c6d331a3ad:0xdd69bc9ce2201a20!8m2!3d19.1407135!4d72.833408!9m1!1b1!16s%2Fg%2F11l1_s28x1?entry=ttu"
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "m6QErb"))
        )

        review_container = driver.find_element(By.CLASS_NAME, "m6QErb")
        driver.execute_script("arguments[0].scrollIntoView();", review_container)
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "jftiEf"))
        )

        review_blocks = review_container.find_elements(By.CLASS_NAME, "jftiEf")

        unique_names = set()
        unique_reviews = set()

        for block in review_blocks:
            try:
                name = ""
                img_src = None
                rating = None
                inner_html = None
                name_elements = block.find_elements(By.CLASS_NAME, "d4r55")
                if name_elements:
                    name = name_elements[0].text.strip()
                    if not name or name in unique_names:
                        continue
                    unique_names.add(name)
                img_elements = block.find_elements(By.CLASS_NAME, "NBa7we")
                if img_elements:
                    img_src = img_elements[0].get_attribute("src")
                rating_elements = block.find_elements(By.CLASS_NAME, "wiI7pd")
                if rating_elements:
                    rating = rating_elements[0].get_attribute("aria-label") or rating_elements[0].text
                du9pgb_elements = block.find_elements(By.CLASS_NAME, "DU9Pgb")
                if du9pgb_elements:
                    inner_html = driver.execute_script("return arguments[0].innerHTML;", du9pgb_elements[0])
                    if not inner_html or inner_html in unique_reviews:
                        continue
                    unique_reviews.add(inner_html)

                reviews_json.append({
                    "reviewer_name": name,
                    "profile_image_url": img_src,
                    "rating": rating,
                    "review_html": inner_html
                })

            except Exception as e:
                continue
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    finally:
        driver.quit()

    return JsonResponse(reviews_json, safe=False)



def robots_txt(request):
    content = """
User-agent: *
Disallow:

User-agent: FacebookBot
Allow: /

User-agent: WhatsApp
Allow: /

User-agent: Twitterbot
Allow: /

User-agent: Instagram
Allow: /

User-agent: LinkedInBot
Allow: /

User-agent: Pinterest
Allow: /

Sitemap: https://boseservicecenter.co.in/sitemap.xml
"""
    return HttpResponse(content.strip(), content_type="text/plain")


