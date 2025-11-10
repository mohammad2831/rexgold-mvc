import django_filters
from django.db.models import Q
from .models import Order # مطمئن شوید که Order در دسترس است

class OrderFilter(django_filters.FilterSet):
    """
    فیلتر پیشرفته برای مدل سفارشات (Order)
    """
    
    # فیلتر جستجوی عمومی (بر اساس شماره فاکتور)
    search = django_filters.CharFilter(method='filter_search', label='جستجو (شماره فاکتور)')
    
    # فیلترهای مورد نیاز شما که قبلاً در View اعمال کردید:
    id = django_filters.NumberFilter(field_name='id', lookup_expr='exact', label='شماره سفارش')
    
    # فیلتر وضعیت معامله (deal_status)
    # از TYPE_CHOICES2 در مدل Order استفاده کنید.
    deal_status = django_filters.ChoiceFilter(
        choices=Order.TYPE_CHOICES2, 
        field_name='deal_status', 
        label='وضعیت معامله'
    )
    
    # فیلتر محصول (بر اساس ID محصول)
    product = django_filters.NumberFilter(field_name='product__id', lookup_expr='exact', label='ID محصول')

    # فیلتر تاریخ ایجاد (بازه)
    created_at__gte = django_filters.DateFilter(field_name='created_at', lookup_expr='date__gte', label='تاریخ ایجاد از')
    created_at__lte = django_filters.DateFilter(field_name='created_at', lookup_expr='date__lte', label='تاریخ ایجاد تا')
    
    # فیلتر نوع معامله (buy/sell)
    type_of_deal = django_filters.ChoiceFilter(
        choices=Order.TYPE_CHOICES,
        field_name='type_of_deal',
        label='نوع معامله'
    )
    
    # متد جستجوی سفارشی (فیلتر کردن بر اساس شماره فاکتور و ID)
    def filter_search(self, queryset, name, value):
        if not value:
            return queryset
        
        # اگر کاربر عدد وارد کرد، روی ID هم جستجو کند.
        # در غیر این صورت، فقط روی factor_number جستجو کند.
        
        filter_query = Q(factor_number__icontains=value)
        
        if value.isdigit():
            filter_query |= Q(id=int(value))
            
        return queryset.filter(filter_query)

    class Meta:
        model = Order
        fields = [
            'search', 
            'id', 
            'deal_status', 
            'product', 
            'type_of_deal', 
            'created_at__gte', 
            'created_at__lte',
        ]