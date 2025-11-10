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
from rest_framework_simplejwt.exceptions import TokenError
from django.core.cache import cache
import time

ONLINE_USERS_SET_KEY = "online:users:set"
USER_ONLINE_KEY = lambda uid: f"online:user:{uid}"

USER_ONLINE_KEY_PREFIX = "online_user_"
ONLINE_TIMEOUT_SECONDS = 900







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
    # ... (Permission classes and serializer setup remain the same) ...

    def post(self, request):
        serializer = VerifyLoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        phone = serializer.validated_data['phone_number']
        otp = serializer.validated_data['otp']

        # ... (اعتبارسنجی‌ها و بررسی OTP remain the same) ...

        cache_key = f"otp_{phone}"
        cached_otp = cache.get(cache_key)

        if cached_otp and cached_otp == otp:
            user = User.objects.get(phone_number=phone)
            cache.delete(cache_key)

            refresh = RefreshToken.for_user(user)
            user_id = str(user.id)

            # --- مدیریت کاربر آنلاین در Redis ---
            
            # ۱. ساخت کلید منحصر به فرد برای این کاربر:
            # کلید نهایی در Redis چیزی شبیه به 'mykey::1:online_user_123' خواهد بود.
            user_online_key = f"{USER_ONLINE_KEY_PREFIX}{user_id}"

            # ۲. ذخیره کلید کاربر با زمان انقضای ۱۵ دقیقه (900 ثانیه):
            # ما مقدار '1' را ذخیره می‌کنیم؛ چون فقط به وجود کلید اهمیت می‌دهیم نه مقدار آن.
            cache.set(user_online_key, "1", timeout=ONLINE_TIMEOUT_SECONDS)
            
            # نکته: هر بار که کاربر لاگین کند، این کلید دوباره ذخیره و زمان انقضای آن تمدید می‌شود.
            
            # ------------------------------------

            # ... (Rest of the response remains the same) ...
            return Response({
                "message": "OTP verified successfully",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)

        return Response({"error": "Invalid phone number or expired OTP"}, status=status.HTTP_400_BAD_REQUEST)


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
            token = RefreshToken(refresh_token)
            user_id = token.payload.get('user_id')

            if not user_id:
                return Response({"error": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)

            # بررسی وجود و فعال بودن کاربر
            try:
                # اگر از جنگو استفاده می‌کنید، باید مدل User را از جای مناسب Import کنید
                user = User.objects.get(id=user_id, is_active=True)
            except User.DoesNotExist:
                return Response({"error": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)

            # --- مدیریت آنلاین بودن در Redis (تمدید ۱۵ دقیقه‌ای) ---
            user_id_str = str(user_id)
            
            # ۱. ساخت کلید دقیق
            user_online_key = f"{USER_ONLINE_KEY_PREFIX}{user_id_str}"

            # ۲. ذخیره (تمدید) کلید کاربر با زمان انقضای ۱۵ دقیقه (900 ثانیه):
            # این دستور تضمین می‌کند که هر بار کاربر توکن را رفرش می‌کند،
            # حضور او به مدت ۱۵ دقیقه دیگر تمدید شود (TTL ریست شود).
            cache.set(user_online_key, "1", timeout=ONLINE_TIMEOUT_SECONDS) 

            # --- حذف منطق اشتباه Set ---
            # current_set = cache.get(ONLINE_USERS_SET_KEY, set())
            # current_set.add(user_id_str)
            # cache.set(ONLINE_USERS_SET_KEY, current_set, timeout=16 * 60)

            # --- پاسخ با توکن دسترسی جدید ---
            return Response({
                "access": str(token.access_token)
            }, status=status.HTTP_200_OK)

        except TokenError:
            return Response({"error": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # بهتر است خطای کلی Exception را برای محیط پروداکشن به یک پیام عمومی تبدیل کنید
            return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



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
            return Response(
                {"error": "Refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = request.user

        # پاک کردن سشن
        User.objects.filter(id=user.id).update(active_session_key=None)
        '''
        fresh_user = User.objects.get(id=user.id)
        print("SESSION KEY AFTER LOGOUT:", fresh_user.active_session_key)
        '''
        # blacklist کردن توکن
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()  # حالا کار می‌کنه!
        except TokenError:
            pass  # توکن قبلاً blacklist شده یا نامعتبر

        return Response(
            {"message": "با موفقیت خارج شدید."},
            status=status.HTTP_205_RESET_CONTENT
        )



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