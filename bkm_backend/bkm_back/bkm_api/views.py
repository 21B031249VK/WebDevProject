from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from bkm_api.models import Category, Product, Order
import json


# Create your views here.


@csrf_exempt
def category_list(request):
    if request.method == 'GET':
        category = Category.objects.all()
        category_json = [cat.to_json() for cat in category]
        return JsonResponse(category_json, safe=False)
    elif request.method == 'POST':
        data = json.loads(request.body)
        try:
            category = Category.objects.create(name=data['name'])
        except Exception as e:
            return JsonResponse({'message': str(e)})

        return JsonResponse(category.to_json())


def category_products(request, category_id):
    try:
        category = Category.objects.get(id=category_id).products.all()
        category_json = [prod.to_json() for prod in category]
        return JsonResponse(category_json, safe=False)
    except Category.DoesNotExist as e:
        return JsonResponse({'message': str(e)}, status=400)


@csrf_exempt
def product_list(request):
    if request.method == 'GET':
        product_list = Product.objects.all()
        product_json = [prod.to_json() for prod in product_list]
        return JsonResponse(product_json, safe=False)
    elif request.method == 'POST':
        data = json.loads(request.body)
        try:
            product = Product.objects.create(name=data['name'], description=data['description'], price=data['price'], category_id=data['category_id'])
        except Exception as e:
            return JsonResponse({'message': str(e)})

        return JsonResponse(product.to_json())


@csrf_exempt
def product_detail(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist as e:
        return JsonResponse({'message': str(e)}, status=400)

    if request.method == 'GET':
        return JsonResponse(product.to_json())
    elif request.method == 'PUT':
        data = json.loads(request.body)
        product.name = data['name']
        product.description = data['description']
        product.price = data['price']
        product.category_id = data['category_id']
        product.save()
        return JsonResponse(product.to_json())
    elif request.method == 'DELETE':
        product.delete()
        return JsonResponse({'message': 'deleted'}, status=204)


