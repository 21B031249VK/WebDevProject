from django.shortcuts import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated

from bkm_api.serializers import Category2Serializer, CategorySerializer, Product2Serializer, CategoryProductsSerializer, OrderSerializer, CommentSerializer, ProductCommentSerializer
from bkm_api.models import Category, Product, Order, Comment

class CategoryListAPIView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        permission_classes = (IsAuthenticated,)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        permission_classes = (IsAuthenticated,)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryProductsAPIView(APIView):
    def get_object(self, pk):
        try:
            return Category.objects.get(id=pk)
        except Category.DoesNotExist as e:
            raise Http404

    def get(self, request, pk=None):
        category = self.get_object(pk)
        serializer = CategoryProductsSerializer(category)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def ProductList(request):
    if request.method == 'GET':
        prod = Product.objects.all()
        serializer = Product2Serializer(prod, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        permission_classes = (IsAuthenticated,)
        serializer = Product2Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class CommentListAPIView(APIView):
    def get_object(self, pk):
        try:
            return Product.objects.get(id=pk)
        except Product.DoesNotExist as e:
            raise Http404

    def get(self, request, pk=None):
        product = self.get_object(pk)
        serializer = ProductCommentSerializer(product)
        return Response(serializer.data)

    def post(self, request, pk):
        product = self.get_object(pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def ProductDetail(request, pk):
    try:
        prod = Product.objects.get(id=pk)
    except Product.DoesNotExist as e:
        return Response({'message': str(e)}, status=400)

    if request.method == 'GET':
        serializer = Product2Serializer(prod)
        return Response(serializer.data)
    elif request.method == 'PUT':
        permission_classes = (IsAuthenticated,)
        serializer = Product2Serializer(instance=prod, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    elif request.method == 'DELETE':
        permission_classes = (IsAuthenticated,)
        prod.delete()
        return Response({'message': 'deleted'}, status=204)


@api_view(['GET', 'POST'])
def OrderList(request):
    if request.method == 'GET':
        ord = Order.objects.all()
        serializer = OrderSerializer(ord, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        permission_classes = (IsAuthenticated,)
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
