from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from bkm_api.class_views import CategoryListAPIView, CategoryProductsAPIView, ProductList, ProductDetail, OrderList, CommentListAPIView

urlpatterns=[
    path('login/', obtain_jwt_token),

    path('categories/', CategoryListAPIView.as_view()),
    path('categories/<int:pk>/products/', CategoryProductsAPIView.as_view()),
    path('products/', ProductList),
    path('products/<int:pk>/', ProductDetail),
    path('orders/', OrderList),
    path('products/<int:pk>/comments/', CommentListAPIView.as_view())
]