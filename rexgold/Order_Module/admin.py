from django.contrib import admin
from .models import Payment, Order 

# ----------------------------------------------------
# ۱. مدیریت مدل Order (سفارشات/معاملات)
# ----------------------------------------------------

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # فیلدهایی که در لیست ادمین نمایش داده می‌شوند
    list_display = (
        'factor_number',
        'get_type_of_deal_display', # نمایش نام کامل (خرید/فروش)
        'price', 
        'user', 
        'get_payment_status_display', # نمایش وضعیت پرداخت
        'get_deal_status_display',    # نمایش وضعیت کلی معامله
        'created_at',
        'is_paid_status', # متد سفارشی برای نمایش وضعیت پرداخت (اختیاری)
    )

    # فیلدهای قابل جستجو
    search_fields = ('factor_number', 'user__username', 'description')

    # فیلدهای قابل فیلتر
    list_filter = (
        'type_of_deal', 
        'deal_status', 
        'payment_status', 
        'delivery_status', 
        'buy_date'
    )
    
    # تنظیم نحوه نمایش فیلدها در صفحه جزئیات (برای سازماندهی بهتر)
    fieldsets = (
        ('اطلاعات پایه معامله', {
            'fields': ('factor_number', 'type_of_deal', 'user', 'description')
        }),
        ('جزئیات اقلام و قیمت', {
            'fields': ('wight', 'soot', 'price', 'main_price')
        }),
        ('وضعیت و تاریخ‌', {
            'fields': ('buy_date', 'delivery_date', 'payment_status', 'delivery_status', 'deal_status')
        }),
        ('امور مالی و پاسخ', {
            'fields': ('user_debt_amount', 'user_credit_amount', 'ok_responde')
        }),
    )
    
    # فیلدهای فقط خواندنی
    readonly_fields = ('created_at', 'buy_date') 

    # متد سفارشی برای نمایش رنگی یا بهتر وضعیت پرداخت
    @admin.display(description='وضعیت پرداخت')
    def is_paid_status(self, obj):
        if obj.payment_status == 'payed':
            return "پرداخت شده"
        elif obj.payment_status == 'unpaid':
            return "پرداخت نشده"
        return "نامشخص"


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'payment_id', 
        'price', 
        'user', 
        'get_type_of_payment_display', # نمایش نوع پرداخت (کارت، آنلاین، نقدی)
        'get_status_display',         # نمایش وضعیت (تایید شده/ناموفق)
        'date', 
    )

    search_fields = ('payment_id', 'user__username', 'account_destination_number')
    
    list_filter = ('status', 'type_of_payment')
    
    fieldsets = (
        ('جزئیات پرداخت', {
            'fields': ('payment_id', 'price', 'type_of_payment', 'date', 'status', 'user')
        }),
        ('شماره حساب‌ها', {
            'fields': ('account_destination_number', 'account_genesis_number')
        }),
    )

 