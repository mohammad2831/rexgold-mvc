from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from .models import Product, Category
from .serializers import AdminAddCategoryViewSerializer,AdminAddProductViewSerializer,AdminDeleteProductSerializer,AdminDetailCategoryViewSerializer,AdminDetailProductViewSerializer,AdminListCategoryViewSerializer,AdminListViewProductserializer,AdminUpdateProductViewSerializer
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core.cache import cache
from .price_cache import LATEST_PRICES_KEY, LATEST_UPDATE_KEY
from . price_cache import get_all_prices
from .permissions import product_manager, category_manager
from Admin_Pannel_Module.permissions import employee
from rest_framework.permissions import IsAuthenticated



@extend_schema(
        tags=['Price'],    
    )
def latest_prices_view(request):
    data = get_all_prices()
    return JsonResponse(data, json_dumps_params={'ensure_ascii': False})








#category

@extend_schema(
        tags=['Admin Pannel (product category)'],
        request = AdminAddCategoryViewSerializer
    )
class AdminAddCategoryView(APIView):
    permission_classes = [IsAuthenticated, employee, category_manager] 

    def post(self, request):
        serdata = AdminAddCategoryViewSerializer(data=request.data)
        if serdata.is_valid():
            serdata.save()
            return Response(serdata.data, status=status.HTTP_201_CREATED)
        return Response(serdata.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
        tags=['Admin Pannel (product category)']
    )
class AdminDeleteCategoryView(APIView):
    permission_classes = [IsAuthenticated, employee, category_manager] 

    def delete(self, request, pk):
        try:
            cattegory = Category.objects.get(id=pk)
        except Category.DoesNotExist:
            return Response({"error": "دسته بندی با این ID وجود ندارد."}, status=status.HTTP_404_NOT_FOUND)

        cattegory.delete()
        return Response({"message": "دسته بندی با موفقیت حذف شد."}, status=status.HTTP_200_OK)



@extend_schema(
        tags=['Admin Pannel (product category)']
    )
class AdminDetailCategoryView(APIView):
    permission_classes = [IsAuthenticated, employee, category_manager] 

    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk) 
        serdata = AdminDetailCategoryViewSerializer(category) 
        return Response(serdata.data, status=status.HTTP_200_OK)



@extend_schema(
        tags=['Admin Pannel (product category)']
    )
class AdminListCategoryView(APIView):
    permission_classes = [IsAuthenticated, employee, category_manager] 

    def get(self, request):
        categories = Category.objects.all()
        serdata =  AdminListCategoryViewSerializer(categories, many=True)
        return Response(serdata.data, status=status.HTTP_200_OK)

class AdminUpdateCategoryView(APIView):
    permission_classes = [IsAuthenticated, employee, category_manager] 

    pass






#product

@extend_schema(
        tags=['Admin Pannel (products)'],
        request=AdminListViewProductserializer,


    )
class AdminListProductView(APIView):
    
    permission_classes = [IsAuthenticated, employee, product_manager] 

    def get(self, request):
        products= Product.objects.all()

        print(products)

        serdata=AdminListViewProductserializer(products, many=True)
        return Response(serdata.data, status=status.HTTP_200_OK)


@extend_schema(
        tags=['Admin Pannel (products)']
    )
class AdminDetailProductView(APIView):
    permission_classes = [IsAuthenticated, employee, product_manager] 


    def get(self, request, pk):
        
        try:
            product = Product.objects.get(pk=pk)
        
        except Product.DoesNotExist:
            return Response(
                {"error": f"Product with ID {pk} not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        print(product)
        serializer = AdminDetailProductViewSerializer(product)
        print(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    tags=['Admin Pannel (products)'],
    request=AdminAddProductViewSerializer,
    responses={
        # پاسخ موفقیت‌آمیز برای ایجاد یک محصول
        status.HTTP_201_CREATED: AdminAddProductViewSerializer,
        # پاسخ خطا (Validation Error, Bad Request)
        status.HTTP_400_BAD_REQUEST: {
            'description': 'خطاهای اعتبارسنجی (Validation Errors) یا درخواست نامعتبر.',
            'content': {
                'application/json': {
                    'example': {
                        "weight": ["وزن برای فروش بر اساس وزن اجباری است."],
                        "price": ["قیمت نمی‌تواند منفی باشد."],
                        "user": ["کاربر معتبر نیست."]
                    }
                }
            }
        }
    }
)
class AdminAddProductView(APIView):
    permission_classes = [IsAuthenticated, employee, product_manager] 

    def post(self, request):
        many = isinstance(request.data, list)
        serializer = AdminAddProductViewSerializer(data=request.data, many=many)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
        tags=['Admin Pannel (products)'],
        request=AdminUpdateProductViewSerializer,

        
    )
class AdminUpdataProductView(APIView):
    permission_classes = [IsAuthenticated, employee, product_manager] 

    def put(self, request, pk):
        try:
            product = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            return Response({"error": "محصول با این ID وجود ندارد."}, status=status.HTTP_404_NOT_FOUND)

        serializer = AdminUpdateProductViewSerializer(instance=product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
        tags=['Admin Pannel (products)']
    )
class AdminDeleteProductView(APIView):
    permission_classes = [IsAuthenticated, employee, product_manager] 

    def delete(self, request, pk):
        try:
            product = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            return Response({"error": "محصول با این ID وجود ندارد."}, status=status.HTTP_404_NOT_FOUND)

        product.delete()
        return Response({"message": "محصول با موفقیت حذف شد."}, status=status.HTTP_200_OK)




