
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from Product_Data_Module.models import Product  # مسیر واقعی
from .models import Order
from .serializers import AdminAddOrderViewSerializer,AdminListOrderViewSerializer
from django.utils import timezone
import jdatetime
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.generics import ListAPIView
from .filters import OrderFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from .models import Order 
# ... بقیه ایمپورت‌ها ...





@extend_schema(
    tags=['Admin Panel (order)'],
    parameters=[
        OpenApiParameter(
            name='search',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description='جستجو در شماره فاکتور و ID سفارش',
            required=False,
        ),
        OpenApiParameter(
            name='id',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description='فیلتر دقیق بر اساس ID سفارش',
            required=False,
        ),
        OpenApiParameter(
            name='deal_status',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description='وضعیت معامله',
            enum=[choice[0] for choice in Order.TYPE_CHOICES2],
            required=False,
        ),
        OpenApiParameter(
            name='product',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description='فیلتر بر اساس ID محصول',
            required=False,
        ),
        OpenApiParameter(
            name='type_of_deal',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description='نوع معامله (خرید/فروش)',
            enum=[choice[0] for choice in Order.TYPE_CHOICES],
            required=False,
        ),
        OpenApiParameter(
            name='created_at__gte',
            type=OpenApiTypes.DATE, 
            location=OpenApiParameter.QUERY,
            description='تاریخ ایجاد از (مثال: 2025-10-01)',
            required=False,
        ),
        OpenApiParameter(
            name='created_at__lte',
            type=OpenApiTypes.DATE, 
            location=OpenApiParameter.QUERY,
            description='تاریخ ایجاد تا (مثال: 2025-10-31)',
            required=False,
        ),
    ]
)
class OrderViewSet(viewsets.ModelViewSet):

    queryset = Order.objects.all() 
    serializer_class = AdminListOrderViewSerializer
    filter_backends = [DjangoFilterBackend] 
    filterset_class = OrderFilter
    
    # permission_classes = [IsAdminUser] 
    def get_queryset(self):

        fields_to_select = [
            'id', 'type_of_deal', 'wight', 'main_price', 'price', 
            'factor_number', 'created_at', 'deal_status',

            'user', 'product' 
        ]
        
        queryset = super().get_queryset()

        queryset = queryset.select_related('user', 'product')
        

        return queryset.order_by('-created_at')

@extend_schema(
        tags=['Admin Pannel (order)'],
        request=AdminAddOrderViewSerializer,
        )
class AdminAddOrderView(APIView):
    # permission_classes = [IsAdminUser] # فقط ادمین

    def post(self, request):
        serializer = AdminAddOrderViewSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                "success": False,
                "message": "داده‌های ارسالی نامعتبر است.",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data


        type_of_deal = data['type_of_deal']
      
        weight = data['weight'] 
        price = data['price']
        main_price = data['main_price']
        
        product = data['product'] 
        user = data['user']      
        

        if not user:
            return Response({
                "success": False,
                "message": "ID کاربر ارسالی نامعتبر یا خالی است."
            }, status=status.HTTP_400_BAD_REQUEST)



        source = 'admin_pannel'
        

        today_str = timezone.now().strftime('%y%m%d')
        prefix = f"NL-{today_str}-"
        last_order = Order.objects.filter(
            factor_number__startswith=prefix
        ).order_by('-factor_number').first()

        seq = 1
        if last_order and last_order.factor_number.startswith(prefix):
            try:

                seq = int(last_order.factor_number.split('-')[-1]) + 1
            except ValueError: # اگر بخش آخر عدد نباشد
                seq = 1
        factor_number = f"{prefix}{seq:03d}"

        try:
            order = Order.objects.create(
                user=user,           # <<< ارسال شیء User
                type_of_deal=type_of_deal,
                weight=weight,
                price=price,
                main_price=main_price,
                product=product,     # <<< ارسال شیء Product (نه product_id)
                source_order=source,
                factor_number=1,
                payment_status='unpaid',
                delivery_status='not_deliver',
                deal_status='unknown'
     
            )
        except Exception as e:
            return Response({
                "success": False,
                "message": f"خطا در ذخیره سفارش: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
        output_serializer = AdminAddOrderViewSerializer(order)
        jalali_date = order.get_jalali_date()

        return Response({
            "success": True,
            "message": "سفارش با موفقیت توسط ادمین ایجاد شد.",
            "data": {
                **output_serializer.data,
                "factor_number": factor_number,
                "jalali_date": jalali_date
            }
        }, status=status.HTTP_201_CREATED)







@extend_schema(
        tags=['Admin Pannel (order)'],
        request=AdminAddOrderViewSerializer,
        )
class AdminListOrderView(APIView):

   # permission_classes = [IsAdminUser] # فقط ادمین

    def get(self, request):
      
        queryset = Order.objects.all().order_by('-created_at')
        
    
        serializer = AdminListOrderViewSerializer(queryset, many=True)
        
   
        return Response({
            "success": True,
            "message": "لیست سفارشات با موفقیت بازیابی شد.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)












