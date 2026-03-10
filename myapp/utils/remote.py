from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


def accessories_remote(request):
    return render(request,'myapp/remote.html')



def products_details(request):
    return render(request,'myapp/product-details.html')


def fetch_details_data(request):
    return render(request,'myapp/product-details.html')

@csrf_exempt
def color_types(request):
    return render(request,'myapp/color_type.html')