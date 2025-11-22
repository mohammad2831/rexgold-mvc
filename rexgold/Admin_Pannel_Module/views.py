# API/Price/views.py
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UpdateCommissionAPISerializer
#from GoldData.models import SellGoldToUs, BuyGoldFromUs
from Product_Data_Module.models import Product, Category
from Price_Mnage_Module.models import Access_All,Access_By_User,Access_By_UserGroup
import json
import logging
from django.utils import timezone
#from GoldData_Module.models import SellGoldToUs, BuyGoldFromUs
import secrets
from django.core.cache import cache
from drf_spectacular.utils import extend_schema
from . serializers import AdminUpdateUserViewSerializer,AdminListUserGroupViewSerializer,AdminAddUserGroupViewSerializer,AdminAddUserViewSerializer,AdminDetailUserViewSerializer,AdminListUserViewSerializer,AdminLoginViewSerializer,AdminVerifyLoginViewSerializer
import re
from Utils.sendotp import send_otp
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import generics
from rest_framework import viewsets
from .filters import UserFilter
import django_filters as filter # ⬅️ نام مستعار (alias) اشتباه
from django_filters.rest_framework import DjangoFilterBackend
#from GeneratePrice_Module.Serializers import DetailProfitByUserGroupViewSerializer
from rest_framework.generics import ListAPIView
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from Account_Module.models import User, UserGroup
from .permissions import employee, user_manager, usergroup_manager
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import Permission

from Account_Module.constants import USER_TYPE_CHOICES, USER_REQUEST_STATUS_CHOICES,USER_STATUS_CHOICES

logger = logging.getLogger(__name__)







@extend_schema(
        summary="Retrieve authenticated  admin user's information",
        description="This endpoint returns the details of the currently authenticated user.",
        responses={
            200: {
                "description": "User information retrieved successfully",
                "example": {
                    "id": 1,
                    "phone_number": "+1234567890",
                    "username": "user123",
                    "first_name": "John",
                    "last_name": "Doe",
                    # سایر فیلدهای مورد نیاز
                }
            },
            401: {"description": "Unauthorized. User is not authenticated."}
        },
        tags=['Admin Pannel (oath)']
    )
class AdminGetMeView(APIView):
    permission_classes = [IsAuthenticated]

    
    def get(self, request):
        user = request.user
        groups = list(user.groups.values_list('name', flat=True))
        all_permissions = user.get_all_permissions()  
        permissions_codenames = {perm.split('.')[-1] for perm in all_permissions}

        user_data = {
            "id": user.id,
            "phone_number": user.phone_number,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "groups": groups,
            "permissions": list(permissions_codenames),
            "is_superuser": user.is_superuser,
            "is_staff": user.is_staff,
        }
        return Response(user_data, status=status.HTTP_200_OK)




@extend_schema(
    tags=['Admin Pannel (user)'],
    parameters=[
        # جستجوی ترکیبی
        OpenApiParameter(
            name='search',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description='جستجو در نام کاربری و شماره تلفن',
            required=False,
        ),
        # نوع کاربر
        OpenApiParameter(
            name='user_type',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description='دسته‌بندی کاربر',
            enum=[choice[0] for choice in User.TYPE_CHOICES2],
            required=False,
        ),
        # وضعیت درخواست
        OpenApiParameter(
            name='request_status',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description='وضعیت درخواست کاربر',
            enum=[choice[0] for choice in User.TYPE_CHOICES],
            required=False,
        ),
        # آنلاین/آفلاین
        OpenApiParameter(
            name='is_online',
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            description='آنلاین بودن کاربر',
            required=False,
        ),
        # فعال/غیرفعال
        OpenApiParameter(
            name='status',
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            description='فعال/غیرفعال بودن حساب',
            required=False,
        ),
    ]
)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminListUserViewSerializer
    permission_classes = [IsAuthenticated, user_manager, employee] 
    filter_backends = [DjangoFilterBackend] 
    filterset_class = UserFilter


    def get_queryset(self):
        # فقط فیلدهای لازم رو بگیر
        return super().get_queryset().only(
            'id', 'username', 'phone_number', 'active_session_key',
            'user_type', 'group__name', 'user_status', 'request_status'
        )




































#user
@extend_schema(
        tags=['Admin Pannel (user)']
    )

class UserTypeChoicesAPIView(APIView):
    permission_classes = [IsAuthenticated, employee] 

    def get(self, request):
        return Response({
            "user_types": USER_TYPE_CHOICES
        })


@extend_schema(
        tags=['Admin Pannel (user)']
    )
class UserRequestStatusChoisesAPIView(APIView):
    permission_classes = [IsAuthenticated, employee] 

    def get(self, request):
        return Response({
            "request_status": USER_REQUEST_STATUS_CHOICES
        })


@extend_schema(
        tags=['Admin Pannel (user)']
    )
class UserStatusChoicesAPIView(APIView):
    permission_classes = [IsAuthenticated, employee] 

    def get(self, request):
        return Response({
            "user_status": USER_STATUS_CHOICES
        })  




@extend_schema(
        request=AdminAddUserViewSerializer,
        tags=['Admin Pannel (user)']
    )
class AdminAddUserView(APIView):
    permission_classes = [IsAuthenticated, employee, user_manager] 
    def post(self, request):
        many = isinstance(request.data, list)
        serializer = AdminAddUserViewSerializer(data=request.data, many=many)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
        tags=['Admin Pannel (user)'],
        request=AdminUpdateUserViewSerializer
    )
class AdminUpdateUserView(APIView):
    permission_classes = [IsAuthenticated, employee, user_manager] 

    def put(self, request, pk):
        try:
            user = User.objects.get(id=pk)
        except user.DoesNotExist:
            return Response({"error": "user with this id not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = AdminUpdateUserViewSerializer(instance=user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
        tags=['Admin Pannel (user)']
    )
class AdminDetailUserView(APIView):
    permission_classes = [IsAuthenticated, employee, user_manager] 

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serdata = AdminDetailUserViewSerializer(user)
        return Response(serdata.data, status=status.HTTP_200_OK)


@extend_schema(
        tags=['Admin Pannel (user)']
    )
class AdminListUserView(APIView):
    permission_classes = [IsAuthenticated, employee, user_manager] 

    def get(self, request):
        users = User.objects.all().select_related('group')
        
        serdata = AdminListUserViewSerializer(
            users, 
            many=True, 
            context={'request': request}  
        )
        
        return Response(serdata.data, status=status.HTTP_200_OK)


@extend_schema(
        tags=['Admin Pannel (user)']
    )
class AdminDeleteUserView(APIView):
    permission_classes = [IsAuthenticated, employee, user_manager] 

    def delete(self, request, pk):
        try:
            product = User.objects.get(id=pk)
        except Product.DoesNotExist:
            return Response({"error": "کاربر با این ID وجود ندارد."}, status=status.HTTP_404_NOT_FOUND)

        product.delete()
        return Response({"message": "کاربر با موفقیت حذف شد."}, status=status.HTTP_200_OK)



















@extend_schema(
    tags=['Admin Pannel (user)'],
    parameters=[
        # جستجوی ترکیبی
        OpenApiParameter(
            name='search',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description='جستجو در نام کاربری و شماره تلفن',
            required=False,
        ),
        # نوع کاربر
        OpenApiParameter(
            name='user_type',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description='دسته‌بندی کاربر',
            enum=[choice[0] for choice in User.TYPE_CHOICES2],
            required=False,
        ),
        # وضعیت درخواست
        OpenApiParameter(
            name='request_status',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description='وضعیت درخواست کاربر',
            enum=[choice[0] for choice in User.TYPE_CHOICES],
            required=False,
        ),
        # آنلاین/آفلاین
        OpenApiParameter(
            name='is_online',
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            description='آنلاین بودن کاربر',
            required=False,
        ),
        # فعال/غیرفعال
        OpenApiParameter(
            name='status',
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            description='فعال/غیرفعال بودن حساب',
            required=False,
        ),
    ]
)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminListUserViewSerializer
    permission_classes = [IsAuthenticated, employee, user_manager] 
    filter_backends = [DjangoFilterBackend] 
    filterset_class = UserFilter


    def get_queryset(self):
        return super().get_queryset().only(
        'id',  # حتماً باید باشد
        'username', 'phone_number',
        'user_type', 'group__name', 'request_status', 'is_active'
    )















































#user group
@extend_schema(
        summary="detail user group endpoint",
        tags=['Admin Pannel (user group)']
    )
class AdminDetailUserGroupView(APIView):
    permission_classes = [IsAuthenticated, employee, usergroup_manager] 

    def get(self, request, pk):
        usergroup = get_object_or_404(UserGroup, pk=pk)
        users = usergroup.members.all()

        users_data = DetailProfitByUserGroupViewSerializer(users, many=True).data

        response_data = {
            "group_id": usergroup.id,
            "group_name": usergroup.name,
            "users": users_data
        }

        return Response(response_data, status=status.HTTP_200_OK)


@extend_schema(
        summary="detail user group endpoint",
        tags=['Admin Pannel (user group)']
    )
class AdminUpdateUserGroupView(APIView):
    permission_classes = [IsAuthenticated, employee, usergroup_manager] 

    def put(self, request):
        pass




@extend_schema(
        summary="list user group endpoint",
        tags=['Admin Pannel (user group)']
    )
class AdminListUserGroupView(APIView):
    permission_classes = [IsAuthenticated, employee, usergroup_manager] 

    def get(self, request):
        usergroups = UserGroup.objects.all()
        serdata =  AdminListUserGroupViewSerializer(usergroups, many=True)
        return Response(serdata.data, status=status.HTTP_200_OK)


@extend_schema(
        summary="delete user group endpoint",
        tags=['Admin Pannel (user group)']
    )
class AdminDeleteUserGroupView(APIView):
    permission_classes = [IsAuthenticated, employee, usergroup_manager] 

    def delete(self, request, pk):
        try:
            product = UserGroup.objects.get(id=pk)
        except UserGroup.DoesNotExist:
            return Response({"error": "'گروه کاربران یافت نشد'"}, status=status.HTTP_404_NOT_FOUND)

        product.delete()
        return Response({"message": "گروه کاربران با موفقیت حذف شد"}, status=status.HTTP_200_OK)


@extend_schema(
        summary="add user group endpoint",
        request=AdminAddUserGroupViewSerializer,
        tags=['Admin Pannel (user group)']
    )
class AdminAddUserGroupView(APIView):
    permission_classes = [IsAuthenticated, employee, usergroup_manager] 

    
    def post(self, request):
        serdata = AdminAddUserGroupViewSerializer(data=request.data)
        if serdata.is_valid():
            serdata.save()
            return Response(serdata.data, status=status.HTTP_201_CREATED)
        return Response(serdata.errors, status=status.HTTP_400_BAD_REQUEST)

























































































































@extend_schema(
        tags=['Admin Pannel (user)']
    )
class AdminListUserView(ListAPIView):
    permission_classes = [IsAuthenticated, employee, user_manager] 

    queryset = User.objects.all().select_related('group')
    serializer_class = AdminListUserViewSerializer














'''

class UpdateCommissionAPIView(APIView):
    ITEM_MAP = {
        "1": "abshode_naghd_farda",
        "2":

 "abshode_with_gateway",
        "3": "seke_tamam_1386",
        "4": "seke_nim_1386",
        "5": "seke_rob_1386",
        "6": "seke_tamam_sal_payeen",
        "7": "seke_rob_sal_payeen_ta_80",
        "8": "seke_nim_sal_payeen_ta_80",
        "9": "seke_rob_1403",
        "10": "seke_tamam_1403",
    }

    def post(self, request, *args, **kwargs):
        # 1. Validate serializer
        serdata = UpdateCommissionSerializer(data=request.data)
        if not serdata.is_valid():
            return Response({"error": serdata.errors}, status=status.HTTP_400_BAD_REQUEST)

        # 2. Extract validated data
        data = serdata.validated_data
        action = data['action']
        item_id = data['item_id']
        commission_value = data['commission']
        is_active = data['is_active']

        # 3. Validate item_id
        base_field = self.ITEM_MAP.get(item_id)
        if not base_field:
            return Response({"error": f"Invalid item_id: {item_id}"}, status=status.HTTP_400_BAD_REQUEST)

        # 4. Determine model and fields
        if action == "sell":
            model_class = SellGoldToUs
            suffix = "_sell"
            message = "Sell commission updated successfully."
        elif action == "buy":
            model_class = BuyGoldFromUs
            suffix = "_buy"
            message = "Buy commission updated successfully."
        else:
            return Response({"error": "Invalid action. Use 'buy' or 'sell'."}, status=status.HTTP_400_BAD_REQUEST)

        commission_field = f"{base_field}{suffix}"
        time_field = f"{base_field}_time{suffix}"
        status_field = f"{base_field}{suffix}_status"

        # 5. Check if fields exist in model
        for field in [commission_field, time_field, status_field]:
            if not hasattr(model_class, field):
                logger.error(f"Field {field} does not exist in {model_class.__name__}")
                return Response({"error": f"Field {field} does not exist in {model_class.__name__}"}, 
                               status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 6. Update or create object within transaction
        try:
            with transaction.atomic():
                obj, created = model_class.objects.select_for_update().get_or_create(defaults={})
                setattr(obj, commission_field, commission_value)
                setattr(obj, status_field, is_active)
                setattr(obj, time_field, timezone.now())
                obj.save()
                logger.info(f"Updated {action} commission for item_id {item_id}")
        except Exception as e:
            logger.error(f"Error updating commission: {str(e)}")
            return Response({"error": "An error occurred while updating commission."}, 
                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 7. Return success response
        return Response({"status": "success", "message": message}, status=status.HTTP_200_OK)

'''

class BuyCommissionAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            payload = json.loads(request.body.decode("utf-8"))
            data = payload.get("data", {})
            item_id = data.get("item_id")
            buy_active = data.get("buy_active")
            buy_comm_raw = data.get("buy_commission")
        except json.JSONDecodeError:
            return Response({"error": "JSON نامعتبر است."}, status=status.HTTP_400_BAD_REQUEST)

        # ... (پیاده‌سازی منطق مشابه برای به‌روزرسانی مدل BuyGoldFromUs)

        return Response({"status": "success", "message": "کمیسیون خرید با موفقیت به‌روزرسانی شد."}, status=status.HTTP_200_OK)
    


    

def generate_otp(phone_number, timeout=300):
    otp = ''.join(secrets.choice('0123456789') for _ in range(4))
    cache.set(f"otp_{phone_number}", otp, timeout=timeout)
    return otp




@extend_schema(
        summary="Generates and sends an OTP for admin user login",
        description="This endpoint sends an OTP to the admin user's phone number for login.",
        request=AdminLoginViewSerializer,
        responses={
            200: {"description": "OTP sent for login."},
            400: {"description": "Invalid phone number or other errors."},
            403: {"description": "User account is not active."},
            406: {"description": "User is not a admin"},
        },
        tags=['Admin Pannel (oath)']
    )
class AdminLoginGenerateOTPView(APIView):
    #permission_classes = [employee]

    def post(self, request):
        serializer = AdminLoginViewSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone_number']

            user = get_object_or_404(User, phone_number=phone)
            if not phone or not re.match(r'^\+?[0-9]\d{1,14}$', phone):
                return Response({
                    'status': 'warning',
                    "message": "the phone number format it is not correct"}, status=status.HTTP_400_BAD_REQUEST)

            if not User.objects.filter(phone_number=phone).exists():
                return Response({"error": "Phone number not registered."}, status=status.HTTP_400_BAD_REQUEST)

            if not user.is_active:
                return Response({
                    'status': 'error',
                    "message": "user it is not active"}, status=status.HTTP_403_FORBIDDEN)
            

            otp = generate_otp(phone)
            cache_key = f"otp_{phone}"
            cache.set(cache_key, otp, timeout=300)
            try:
                print(f"Login OTP for {phone}: {cache.get(cache_key)}")
                send_otp(pattern='69u9der8ondg7dn', otp=otp, phone=phone)
                return Response({"message": "OTP sent for login."}, status=status.HTTP_200_OK)
            except:
                return Response({"message": "can not send otp"}, status=status.HTTP_400_BAD_REQUEST)
            


        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(
    summary="Verifies OTP and provides access tokens for admin user",
    description="This endpoint verifies the OTP sent to the admin user's phone number. If successful, it returns refresh and access tokens.",
    request=AdminVerifyLoginViewSerializer,
    responses={
        200: {
            "description": "OTP verified successfully",
            "example": {
                "message": "OTP verified successfully",
                "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
        },
        400: {
            "description": "Invalid phone number, expired OTP, or validation errors.",
            "example": {
                "error": "Invalid phone number or expired OTP"
            }
        }
    },
        tags=['Admin Pannel (oath)']
)

class AdminVerifyOTPView(APIView):
    def post(self, request):
        serializer = AdminVerifyLoginViewSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        phone = serializer.validated_data['phone_number']
        otp = serializer.validated_data['otp']

      

        cache_key = f"otp_{phone}"
        cached_otp = cache.get(cache_key)

        if cached_otp and cached_otp == otp:
            user = User.objects.get(phone_number=phone)
            allowed_statuses = ['admin', 'employee']
            
            if user.user_status not in allowed_statuses:
                return Response(
                    {"error": "Access denied. Only Admin or Employee accounts can login here."},
                    status=status.HTTP_403_FORBIDDEN # 403 Forbidden مناسب‌تر است
                )

            cache.delete(cache_key)

            refresh = RefreshToken.for_user(user)
            
            

            return Response({
                "message": "ورود با موفقیت انجام شد",
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            }, status=status.HTTP_200_OK)

        return Response({"error": "Invalid phone number or expired OTP"}, status=status.HTTP_400_BAD_REQUEST)













