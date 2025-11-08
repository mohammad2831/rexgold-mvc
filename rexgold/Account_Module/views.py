# accounts/views.py
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import RegisterVerifyOTPSerializer, LoginSerializer, VerifyLoginSerializer
import random
import secrets
import re
from Utils.sendotp import send_otp
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated
import uuid


def generate_otp(phone_number, timeout=300):
    otp = ''.join(secrets.choice('0123456789') for _ in range(4))
    cache.set(f"otp_{phone_number}", otp, timeout=timeout)
    return otp




@extend_schema(
        summary="Generates and sends an OTP for user login",
        description="This endpoint sends an OTP to the user's phone number for login.",
        request=LoginSerializer,
        responses={
        200: {"description": "کد یکبار مصرف با موفقیت ارسال شد."},
        400: {"description": "شماره تلفن نامعتبر یا اکانت ثبت نشده."},
        403: {"description": "اکانت کاربر فعال نیست."},
    },
        tags=['Authentication']
    )
class LoginGenerateOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone_number']

            user = get_object_or_404(User, phone_number=phone)
            if not phone or not re.match(r'^\+?[0-9]\d{1,14}$', phone):
                return Response({
                    'status': 'warning',
                    "message": "شماره تلفن را بصورت درست ارسال کنید"}, status=status.HTTP_400_BAD_REQUEST)

            if not User.objects.filter(phone_number=phone).exists():
                return Response({"error": "اکانتی با این شماره تلفن در سیستم ثبت نشده است"}, status=status.HTTP_400_BAD_REQUEST)

            if not user.is_active:
                return Response({
                    'status': 'error',
                    "message": "حساب کاربری شما فعال نیست."}, status=status.HTTP_403_FORBIDDEN)

            otp = generate_otp(phone)
            cache_key = f"otp_{phone}"
            cache.set(cache_key, otp, timeout=300)
            try:
                print(f"Login OTP for {phone}: {cache.get(cache_key)}")
                send_otp(pattern='69u9der8ondg7dn', otp=otp, phone=phone)
                return Response({"message": "کد یکبار مصرف ارسال شد"}, status=status.HTTP_200_OK)
            except:
                return Response({"message": "خطا در ارسال کد یکبار مصرف. لطفاً دوباره تلاش کنید"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






@extend_schema(
    summary="Verifies OTP and provides access tokens",
    description="This endpoint verifies the OTP sent to the user's phone number. If successful, it returns refresh and access tokens.",
    request=VerifyLoginSerializer,
    responses={
        200: {
            "description": "OTP verified successfully",
            "example": {
                "message": "ورود با موفقیت انجام شد",
                "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
        },
        400: {
            "description": "Invalid phone number, expired OTP, or validation errors.",
            "example": {
                "error": "کد یکبار مصرف وارد شده نامعتبر یا منقضی شده است"
            }
        }
    },
    tags=['Authentication']
)
class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyLoginSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone_number']
            otp = serializer.validated_data['otp']

            cache_key = f"otp_{phone}"
            cached_otp = cache.get(cache_key)
            if not phone or not re.match(r'^\+?[0-9]\d{1,14}$', phone):
                return Response({
                    'status': 'warning',
                    "message": "لطفاً شماره تلفن را به صورت صحیح ارسال کنید"}, status=status.HTTP_400_BAD_REQUEST)

            if not User.objects.filter(phone_number=phone).exists():
                return Response({"error": "کاربری با این شماره تلفن یافت نشد"}, status=status.HTTP_400_BAD_REQUEST)

            if cached_otp and cached_otp == otp:

                user, created = User.objects.get_or_create(phone_number=phone)
                cache.delete(cache_key)

                refresh = RefreshToken.for_user(user)
                jti = str(uuid.uuid4())
                refresh['jti'] = jti

                # ذخیره JTI در active_session_key
                user.active_session_key = jti
                user.save(update_fields=['active_session_key'])
               
                return Response({
                    "message": "ورود با موفقیت انجام شد",
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }, status=status.HTTP_200_OK)

            return Response({"error": "کد یکبار مصرف وارد شده نامعتبر یا منقضی شده است"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






@extend_schema(
    summary="Refreshes an access token using a refresh token",
    description="This endpoint takes a refresh token and returns a new, valid access token.",
    request={"application/json": {"example": {"refresh": "string"}}},
    responses={
        200: {
            "description": "New access token generated successfully.",
            "example": {
                "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
        },
        400: {
            "description": "Invalid or missing refresh token.",
            "example": {
                "error": "Invalid refresh token"
            }
        }
    },
    tags=['Authentication']
)
class RefreshAccessTokenView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh')

        if not refresh_token:
            return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh = RefreshToken(refresh_token)
            new_access_token = str(refresh.access_token)
            return Response({
                "access": new_access_token
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)
        




@extend_schema(
    summary="Logs out the user by blacklisting their refresh token",
    description="This endpoint requires the user's refresh token in the request body to invalidate it.",
    request={
        "application/json": {
            "example": {
                "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
        }
    },
    responses={
        205: {"description": "Logout successful. Token blacklisted."},
        400: {"description": "Bad Request. Refresh token is missing or invalid."},
        401: {"description": "Unauthorized. User is not authenticated."}
    },
    tags=['Admin Pannel (oath)','Authentication' ]
)
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"error": "Refresh token is required."}, status=400)

        user = request.user

        # روش ۱: update مستقیم (بدون کش)
        User.objects.filter(id=user.id).update(active_session_key=None)

        # روش ۲: یا save با update_fields
        # user.active_session_key = None
        # user.save(update_fields=['active_session_key'])

        print(f"User {user.id} offline - active_session_key cleared")

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            print("Token blacklisted")
        except TokenError as e:
            print(f"Token already invalid: {e}")

        return Response({"message": "با موفقیت خارج شدید."}, status=205)



@extend_schema(
    summary="Generates and sends an OTP for user signup",
    description="This endpoint sends an OTP to the user's phone number for signup and creates a new user record.",
    request=RegisterVerifyOTPSerializer,
    tags=['Authentication' ]
)
class SignupGenerateOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterVerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            referral_code = serializer.validated_data['referral_code']
            cod_meli = serializer.validated_data['cod_meli']

            phone = User.objects.filter(phone_number=str(phone_number)).first()
            if phone:
                return Response({
                    "status": "warning",
                    "message": "شماره تلفن قبلا ثبت شده است."
                }, status=status.HTTP_400_BAD_REQUEST)
            
            referrer = User.objects.filter(invite_code=str(referral_code)).first()
            if not referrer:
                return Response({
                    "status": "warning",
                    "message": "کد معرف صحیح نیست."
                }, status=status.HTTP_400_BAD_REQUEST)

            if not referrer.can_invite:
                return Response({
                    "status": "error",
                    "message": "وضعیت زیرمجموعه‌گیری کاربر فعال نیست."
                }, status=status.HTTP_400_BAD_REQUEST)

            if User.objects.filter(cod_meli=str(cod_meli)).exists():
                return Response({
                    "status": "warning",
                    "message": "کد ملی قبلا ثبت شده است."
                }, status=status.HTTP_400_BAD_REQUEST)

            if User.objects.filter(invite_code=str(cod_meli)).exists():
                return Response({
                    "status": "error",
                    "message": "کد ملی قبلا استفاده شده است."
                }, status=status.HTTP_400_BAD_REQUEST)

            # تولید OTP و ذخیره در cache
            otp = generate_otp(phone_number)
            cache_key = f"otp_{phone_number}"
            cache.set(cache_key, otp, timeout=300)  # 5 دقیقه انقضا

            # ذخیره اطلاعات کاربر در cache
            data_cache_key = f"signup_data_{phone_number}"
            signup_data = {
                'phone_number': phone_number,
                'referral_code': str(referral_code),
                'cod_meli': str(cod_meli),
                'referrer_id': referrer.id  # ذخیره ID referrer برای جلوگیری از مشکلات
            }
            cache.set(data_cache_key, signup_data, timeout=300)  # 5 دقیقه انقضا

            try:
                # چاپ برای دیباگ (می‌توانید در تولید حذف کنید)
                print(f"Signup OTP for {phone_number}: {cache.get(cache_key)}")
                '''
                # ایجاد کاربر جدید
                new_user = User.objects.create(
                    first_name=phone_number,
                    phone_number=phone_number,
                    username=phone_number,
                    is_active=False,
                    invited_by=referrer,
                    cod_meli=str(cod_meli),
                    invite_code=str(cod_meli),
                    verification_code=otp  # ذخیره OTP در مدل
                )
                new_user.set_password(make_password(get_random_string(length=12)))
                new_user.save()
'''
                # ارسال OTP
                send_otp(pattern='69u9der8ondg7dn', otp=otp, phone=phone_number)
                return Response({
                    "status": "success",
                    "message": "اطلاعات شما ثبت شد و کد تأیید به شماره تلفن شما ارسال شد."
                }, status=status.HTTP_201_CREATED)

            except Exception as e:
                # در صورت خطا، کاربر را حذف می‌کنیم
                #if 'new_user' in locals():
                   # new_user.delete()
                print(f"Error: {str(e)}")
                return Response({
                    "status": "error",
                    "message": "خطا در ارسال کد تأیید."
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            "status": "error",
            "message": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    



@extend_schema(
    request=VerifyLoginSerializer,
    tags=['Authentication' ]
)
class SignupVerifyOtpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyLoginSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            verification_code = serializer.validated_data['otp']

            otp_cache_key = f"otp_{phone_number}"
            cached_otp = cache.get(otp_cache_key)

            if not cached_otp or cached_otp != verification_code:
                return Response({
                    "status": "error",
                    "message": "کد تأیید نادرست است یا منقضی شده."
                }, status=status.HTTP_400_BAD_REQUEST)

            # گرفتن اطلاعات از cache
            data_cache_key = f"signup_data_{phone_number}"
            signup_data = cache.get(data_cache_key)
            if not signup_data:
                return Response({
                    "status": "error",
                    "message": "اطلاعات ثبت‌نام یافت نشد یا منقضی شده است."
                }, status=status.HTTP_400_BAD_REQUEST)

            # اعتبارسنجی مجدد برای امنیت (اختیاری، اما خوب است)
            if User.objects.filter(phone_number=phone_number).exists():
                return Response({
                    "status": "warning",
                    "message": "شماره قبلا ثبت شده است."
                }, status=status.HTTP_400_BAD_REQUEST)

            if User.objects.filter(cod_meli=signup_data['cod_meli']).exists():
                return Response({
                    "status": "warning",
                    "message": "کد ملی قبلا ثبت شده است."
                }, status=status.HTTP_400_BAD_REQUEST)

            if User.objects.filter(invite_code=signup_data['cod_meli']).exists():
                return Response({
                    "status": "error",
                    "message": "کد ملی قبلا استفاده شده است."
                }, status=status.HTTP_400_BAD_REQUEST)

            referrer = User.objects.get(id=signup_data['referrer_id'])

            print(signup_data['referral_code'])

            # ایجاد کاربر جدید
            try:
                new_user = User.objects.create(
                    phone_number=phone_number,
                    username=phone_number,
                    is_active=False,  
                    invited_by=referrer,
                    cod_meli=signup_data['cod_meli'],
             
                )
                new_user.set_password(make_password(get_random_string(length=12)))
                new_user.save()

                # پاک کردن cache
                cache.delete(otp_cache_key)
                cache.delete(data_cache_key)

                return Response({
                    "status": "success",
                    "message": "اطلاعات شما با موفقیت ثبت شد. کارشناسان ما به زودی با شما تماس خواهند گرفت."
                }, status=status.HTTP_201_CREATED)

            except Exception as e:
                print(f"Error: {str(e)}")
                return Response({
                    "status": "error",
                    "message": "خطایی رخ داد. لطفا شماره تلفن و کد معرف و کد ملی را بررسی کنید."
                }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "status": "error",
            "message": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)