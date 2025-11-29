# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.db import transaction
from Order_Module.models import Order
from .serializers import UserAddOrderViewSerializer
import jdatetime
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from Price_Mnage_Module.models import Access_All,Access_By_User,Access_By_UserGroup



def get_user_product_access(user, product, weight, deal_type):
    permission_classes = [IsAuthenticated] 

    """
    بررسی دسترسی کاربر به محصول با این قوانین:
    - اگر سطح دسترسی وجود نداشت → اسکیپ کن و به بعدی برو
    - اگر سطح وجود داشت + فعال بود + وزن مجاز نبود → سفارش رد بشه
    - سود فقط از سطوح فعال جمع میشه
    - اولویت وزن: شخصی > گروهی > عمومی
    """
    is_buy = deal_type == 'buy'
    total_profit = 0
    weight_validated = False
    validated_by = None
    
    # 1. سطح شخصی — فقط اگر وجود داشت
    personal = Access_By_User.objects.filter(user=user, product=product).first()
    if personal:  # فقط اگر وجود داشت
        active = personal.active_for_buy if is_buy else personal.active_for_sell
        if active:  # فقط اگر فعال بود
            min_w = getattr(personal, f'min_weight_{deal_type}') or 0
            max_w = getattr(personal, f'max_weight_{deal_type}') or 0

            if weight < min_w or (max_w > 0 and weight > max_w):
                return {
                    "allowed": False,
                    "profit": 0,
                    "message": f"وزن خارج از محدوده دسترسی شخصی ({min_w}–{max_w} گرم)",
                    "failed_at": "personal"
                }
            else:
                # وزن مجاز بود → دیگر نیاز به چک سطوح پایین‌تر نیست
                weight_validated = True
                validated_by = "personal"

            # فقط اگر فعال بود سودش رو اضافه کن
            total_profit += getattr(personal, f'profit_{deal_type}')

    # 2. سطح گروهی — فقط اگر شخصی وزن رو تأیید نکرده بود
    if not weight_validated and user.group:
        group = Access_By_UserGroup.objects.filter(group=user.group, product=product).first()
        if group:  # فقط اگر وجود داشت
            active = group.active_for_buy if is_buy else group.active_for_sell
            if active:
                min_w = group.min_weight_buy if is_buy else group.min_weight_sell
                max_w = group.max_weight_buy if is_buy else group.max_weight_sell

                if weight < min_w or (max_w > 0 and weight > max_w):
                    return {
                        "allowed": False,
                        "profit": 0,
                        "message": f"وزن خارج از محدوده دسترسی گروهی ({min_w}–{max_w} گرم)",
                        "failed_at": "group"
                    }
                else:
                    weight_validated = True
                    validated_by = "group"

                total_profit += getattr(group, f'profit_{deal_type}')

    # 3. سطح عمومی — اگر تا الان وزن تأیید نشده بود
    if not weight_validated:
        global_access = Access_All.objects.filter(product=product).first()
        if global_access:  # اگر وجود داشت
            active = global_access.active_for_buy if is_buy else global_access.active_for_sell
            if active:
                # Access_All محدودیت وزن نداره → اگر فعال بود، وزن اوکیه
                weight_validated = True
                validated_by = "global"
                total_profit += getattr(global_access, f'profit_{deal_type}')

    # اگر وزن در هیچ سطحی تأیید نشد
    if not weight_validated:
        return {
            "allowed": False,
            "profit": 0,
            "message": "وزن سفارش مجاز نیست یا هیچ سطح دسترسی فعالی وجود ندارد.",
            "failed_at": "no_valid_level"
        }

    # همه چیز اوکی
    return {
        "allowed": True,
        "profit": total_profit,
        "validated_by": validated_by,
        "message": f"سفارش مجاز است — وزن توسط سطح '{validated_by}' تأیید شد",
        "total_profit": total_profit
    }        
        





@extend_schema(
        tags=['User Pannel (add order)'],
        request = UserAddOrderViewSerializer,
    )
class UserAddOrderView(APIView):
    #permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        serializer = UserAddOrderViewSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "message": "داده‌های ارسالی معتبر نیست.",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        user = request.user
        group = user.groups.first()  # فرض بر این است که هر کاربر فقط در یک گروه است
        product = data['product']  # محصول انتخاب شده
        weight = data['weight']
        deal_type = data['type_of_deal']  # 'buy' یا 'sell'

        # چک 1: آیا کاربر اجازه تراکنش کلی داره؟
        if not getattr(user, 'possibel_transaction', False):
            return Response({
                "message": "شما دسترسی انجام تراکنش را ندارید. لطفا با پشتیبانی تماس بگیرید."
            }, status=status.HTTP_403_FORBIDDEN)
        access = get_user_product_access(user, product, weight, deal_type)

        if not access["allowed"]:
            return Response({
                "message": access["message"],
                "جزئیات": access.get("failed_at")
            }, status=403)
                
        
        
        
        
        
        
        
        
        order = Order(
            user=user,
            product=data['product_id'],
            type_of_deal=data['type_of_deal'],
            weight=data['weight'],
            soot=data.get('soot', 0.0),
            price=data['price'],
            main_price=data.get('main_price', data['price']),
            delivery_date=data.get('delivery_date'),
            description=data.get('description', ''),
            source_order='user_pannel',  # همیشه از پنل کاربر

            # وضعیت‌های اولیه (بیزنس رول)
            payment_status='unpaid',
            delivery_status='not_deliver',
            deal_status='unknown',

            #factor_number=new_factor_number,
            ok_responde=0,
        )

        order.save()

        # پاسخ نهایی با تاریخ شمسی
        return Response({
            "message": "سفارش با موفقیت ثبت شد.",
            "order_id": order.id,
            "factor_number": order.factor_number,
            "jalali_date": order.get_jalali_date(),
            "status": {
                "payment": order.get_payment_status_display(),
                "delivery": order.get_delivery_status_display(),
                "deal": order.get_deal_status_display(),
            }
        }, status=status.HTTP_201_CREATED)