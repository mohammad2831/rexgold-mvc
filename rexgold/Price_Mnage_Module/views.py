from django.shortcuts import render
import logging
from django.db import transaction
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Account_Module.models import User, UserGroup
from Product_Data_Module.models import Product
from . models import Access_All,Access_By_User,Access_By_UserGroup, Config_Price_Manage
from .serializers import AdminAddConfigPriceManageViewSerializer,AdminAddProfitAllViewSerializer,AdminAddProfitUserGroupViewSerializer,AdminAddProfitUserViewSerializer,AdminGetLastProfitAllViewSerializer,AdminGetProfitUserGroupViewSerializer,AdminGetProfitUserViewSerializer
logger = logging.getLogger(__name__)



@extend_schema(
        tags=['Admin Pannel (profit all)'],
)
class AdminGetConfigPriceManageView(APIView):
    def get(self, request):
            try:
                config = Config_Price_Manage.objects.all().first()
                if config:
                    serializer = AdminAddConfigPriceManageViewSerializer(config)
                    
                    return Response(
                        {
                            "message": "تنظیمات جاری با موفقیت بازیابی شد.",
                            "data": serializer.data
                        },
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {
                            "message": "تنظیمات پیکربندی هنوز در پایگاه داده ذخیره نشده است.",
                            "data": {}
                        },
                        status=status.HTTP_404_NOT_FOUND
                    )

            except Exception as e:
                return Response(
                    {"message": "خطایی در هنگام بازیابی تنظیمات رخ داد.", "detail": str(e)}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

@extend_schema(
        tags=['Admin Pannel (profit all)'],
        request = AdminAddConfigPriceManageViewSerializer
)
class AdminAddConfigPriceManageView(APIView):
    def post(self, request):
        serializer = AdminAddConfigPriceManageViewSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            with transaction.atomic():

                Config_Price_Manage.objects.all().delete()
                

                new_config = Config_Price_Manage.objects.create(**serializer.validated_data)
                
 
            response_serializer = AdminAddConfigPriceManageViewSerializer(new_config)
            
            return Response(
                {
                    "message": "تنظیمات با موفقیت ذخیره و به روز رسانی شد.",
                    "data": response_serializer.data
                },
                status=status.HTTP_201_CREATED # استفاده از 201 برای ایجاد موفقیت‌آمیز
            )
            
        except Exception as e:
            return Response(
                {"message": "خطایی در هنگام ذخیره سازی تنظیمات رخ داد.", "detail": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

#profit user
@extend_schema(
        tags=['Admin Pannel (profit user)'],
        request = AdminAddProfitUserViewSerializer
)
class AdmiAddProfitUserView(APIView):
    def post(self, request):
        serializer = AdminAddProfitUserViewSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data.copy()
        product_id = data.pop('product_id', None)
        user_id = data.pop('user_id', None)

        if not product_id:
            return Response(
                {"error": "فیلد 'product_id' الزامی است."},
                status=status.HTTP_400_BAD_REQUEST
            )


        if not user_id:
            return Response(
                {"error": "فیلد 'user_id' الزامی است."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response(
                {"error": f"محصول با آیدی {product_id} پیدا نشد."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                {"error": f"کاربر با آیدی {user_id} پیدا نشد."},
                status=status.HTTP_404_NOT_FOUND
            )


        data['product'] = product
        data['user'] = user

        try:
            access = Access_By_User.objects.create(**data)
        except Exception as e:
            logger.exception("خطا در ایجاد Access_By_UserGroup: %s", e)
            return Response(
                {"error": "خطا در ایجاد رکورد جدید."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # 7. پاسخ: فقط message و data (ورودی کاربر)
        return Response({
            "message": "تنظیمات با موفقیت ایجاد شد.",
            "user": user_id,
            "product": product_id,
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)


@extend_schema(
        tags=['Admin Pannel (profit user)'],
)
class AdminGetLastProfitUserView(APIView):
    def get(self, request, product_id, user_id):
        # 1. دریافت آخرین رکورد
        profit = Access_By_User.objects.filter(
            product__id=product_id,
            user__id=user_id  # درست: group
        ).order_by('-id').first()

        # 2. اگر وجود نداشت
        if not profit:
            return Response(
                {"error": f"هیچ تنظیماتی برای محصول {product_id} و گروه {user_id} پیدا نشد."},
                status=status.HTTP_404_NOT_FOUND
            )

        # 3. سریالایز کردن خروجی
        serializer = AdminGetProfitUserViewSerializer(profit)

        # 4. پاسخ
        return Response({
            "message": "آخرین تنظیمات با موفقیت دریافت شد.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)




#profit user group
@extend_schema(
        tags=['Admin Pannel (profit user group)'],
)
class AdminGetLastProfitUserGroupView(APIView):
    def get(self, request, product_id, usergroup_id):
        # 1. دریافت آخرین رکورد
        profit = Access_By_UserGroup.objects.filter(
            product__id=product_id,
            group__id=usergroup_id  # درست: group
        ).order_by('-id').first()

        # 2. اگر وجود نداشت
        if not profit:
            return Response(
                {"error": f"هیچ تنظیماتی برای محصول {product_id} و گروه {usergroup_id} پیدا نشد."},
                status=status.HTTP_404_NOT_FOUND
            )

        # 3. سریالایز کردن خروجی
        serializer = AdminGetProfitUserGroupViewSerializer(profit)

        # 4. پاسخ
        return Response({
            "message": "آخرین تنظیمات با موفقیت دریافت شد.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


@extend_schema(
        tags=['Admin Pannel (profit user group)'],
        request = AdminAddProfitUserGroupViewSerializer) 
class AdmiAddProfitUserGroupView(APIView):
    def post(self, request):
        serializer = AdminAddProfitUserGroupViewSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data.copy()
        product_id = data.pop('product_id', None)
        group_id = data.pop('group_id', None)

        if not product_id:
            return Response(
                {"error": "فیلد 'product_id' الزامی است."},
                status=status.HTTP_400_BAD_REQUEST
            )


        if not group_id:
            return Response(
                {"error": "فیلد 'group_id' الزامی است."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response(
                {"error": f"محصول با آیدی {product_id} پیدا نشد."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        try:
            group = UserGroup.objects.get(pk=group_id)
        except UserGroup.DoesNotExist:
            return Response(
                {"error": f"گروه با آیدی {group_id} پیدا نشد."},
                status=status.HTTP_404_NOT_FOUND
            )


        data['product'] = product
        data['group'] = group

        try:
            access = Access_By_UserGroup.objects.create(**data)
        except Exception as e:
            logger.exception("خطا در ایجاد Access_By_UserGroup: %s", e)
            return Response(
                {"error": "خطا در ایجاد رکورد جدید."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # 7. پاسخ: فقط message و data (ورودی کاربر)
        return Response({
            "message": "تنظیمات با موفقیت ایجاد شد.",
            "group": group_id,
            "product": product_id,
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)





#profit all
@extend_schema(
        tags=['Admin Pannel (profit all)'],
    )
class AdminGetLastProfitAllView(APIView):
    def get(self, request, product_id,user_id):
       
        profit = Access_All.objects.filter(product__id=product_id).order_by('-id').first()
       
        if not profit:
            return Response(
                {"error": f"هیچ تنظیماتی برای محصول با آیدی {pk} پیدا نشد."},
                status=status.HTTP_404_NOT_FOUND
            )

       
        serializer = AdminGetLastProfitAllViewSerializer(profit)

        return Response({
            "message": "آخرین تنظیمات با موفقیت دریافت شد.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)



@extend_schema(
        tags=['Admin Pannel (profit all)'],
        request = AdminAddProfitAllViewSerializer
    )    
class AdmiAddProfitAllView(APIView):
    def post(self, request):
        # 1. اعتبارسنجی ورودی
        serializer = AdminAddProfitAllViewSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data.copy()
        product_id = data.pop('product_id', None)

        if not product_id:
            return Response(
                {"error": "فیلد 'product_id' الزامی است."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response(
                {"error": f"محصول با آیدی {product_id} پیدا نشد."},
                status=status.HTTP_404_NOT_FOUND
            )

        data['product'] = product

        try:
            access = Access_All.objects.create(**data)
        except Exception as e:
            logger.exception("خطا در اعمال تنظیمات: %s", e)
            return Response(
                {"error": "خطا در اعمال تنظیمات."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # 6. پاسخ موفقیت
        return Response({
            "message": "تنظیمات با موفقیت ایجاد شد.",
            "product": product_id,

            "data":serializer.data,
        }, status=status.HTTP_201_CREATED)






