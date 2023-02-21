from django.shortcuts import render
from django.http import HttpResponse
import requests
import json
# from . import Phone

# Create your views here.
def hi(request, pk):
    if pk=='1':
        return HttpResponse('nipun')
    elif pk=='2':
        return HttpResponse('akshay')
    else:
        return HttpResponse('vyshnav')

def compare(request):
    return render(request, 'template.html')

def home(request):
    model1 = request.POST.get('model1')
    model2 = request.POST.get('model2')

    model1_data = get_response(model1)
    model2_data = get_response(model2)
    # d = json.dumps(model2_data)
    # name1 = model1_data['data'][0]['name']
    # price1 = model1_data['data'][0]['price']
    # phone_data = Phone(name=name1, price=price1)
    # phone_data.save()
    # return HttpResponse(d)
    return render(
        request, 
        'table.html',
        {
            'model1_name': model1_data['data'][0]['name'],
            'model2_name': model2_data['data'][0]['name'],
            'model1_price': model1_data['data'][0]['price'],
            'model2_price': model2_data['data'][0]['price'],
            'model1_mrp': model1_data['data'][0]['source_mrp'],
            'model2_mrp': model2_data['data'][0]['source_mrp'],
            'model1_rating': model1_data['data'][0]['rating'],
            'model2_rating': model2_data['data'][0]['rating'],
            'model1_image': model1_data['data'][0]['image'],
            'model2_image': model2_data['data'][0]['image']
        }
    )


    # if msg == 'vyshnav':
    #     return render(request, 'test.html',{'msg': msg})
    # else:
    #     return render(request, 'template.html')

def get_response(search_term):
    for i in range(10):
        params = {
            'searchtext': search_term,
            'category': 'mobiles',
            'v_s_type': 'phones',
            'exclude_productId': '',
            'exclude_variantId': '',
            'compare_flag': '1',
        }

        response = requests.get('https://www.gadgets360.com/search/ajax-suggest', params=params)
        if response.json():
            return response.json()


        

