from django.shortcuts import render
from django.http import HttpResponse
import requests
import json
import requests
import urllib3
from myapp.models import Phone

requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = "ALL:@SECLEVEL=1"
# from . import Phone

# Create your views here.
def hi(request, pk):
    if pk == "1":
        return HttpResponse("nipun")
    elif pk == "2":
        return HttpResponse("akshay")
    else:
        return HttpResponse("vyshnav")


def compare(request):
    return render(request, "template.html")


def home(request):
    model1 = request.POST.get("model1")
    model2 = request.POST.get("model2")
    database = request.POST.get("fetchDatabase")
    print(database)

    if not database:
        model1_data = get_response(model1)
        model2_data = get_response(model2)
    else:
        model1_data = get_matched(model1)
        model2_data = get_matched(model2)
    if not model1_data or not model2_data:
        return render(request, "template.html")
    
    model1_data = model1_data["data"][0]
    model2_data = model2_data["data"][0]

    data = {
        "model1_name": model1_data["name"],
        "model2_name": model2_data["name"],
        "model1_price": model1_data["price"],
        "model2_price": model2_data["price"],
        "model1_mrp": model1_data["source_mrp"],
        "model2_mrp": model2_data["source_mrp"],
        "model1_rating": model1_data["rating"],
        "model2_rating": model2_data["rating"],
        "model1_image": model1_data["image"],
        "model2_image": model2_data["image"],
    }

    return render(request, "table.html", data)


def get_matched(model):

    data = []
    for j in model.split():
        for i in Phone.objects.filter(name__contains=j):
            data.append(i.id-1)
    if not data:
        model_data = get_response(model)
        return model_data
    
    match_count = {data.count(i): i for i in data}
    maximum = match_count[max(match_count.keys())]

    matched_model = Phone.objects.all()[maximum]
    data = {
        "name": matched_model.name,
        "price": matched_model.price,
        "source_mrp": matched_model.mrp,
        "rating": matched_model.rating,
        "image": matched_model.image_url
    }

    return {'data': [data]}
    






def update_database(data):

    for i in data['data']:
        if Phone.objects.filter(name__contains=i['name']):
            continue
        phone = Phone(
            name=i["name"],
            price=i["price"],
            mrp=i["source_mrp"],
            rating=i["rating"],
            image_url=i["image"],
        )

        phone.save()
    return


def get_response(search_term):
    try:
        for i in range(10):
            params = {
                "searchtext": search_term,
                "category": "mobiles",
                "v_s_type": "phones",
                "exclude_productId": "",
                "exclude_variantId": "",
                "compare_flag": "1",
            }

            response = requests.get(
                "https://www.gadgets360.com/search/ajax-suggest",
                params=params,
            )
            if response.json():
                update_database(response.json())
                return response.json()
    except Exception as e:
        print(e)
        return False
