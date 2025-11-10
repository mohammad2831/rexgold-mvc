from django.db import models
from Account_Module.models import User
from django.utils.timezone import now
import jdatetime
from Product_Data_Module.models import Product


class Payment(models.Model):
    TYPE_CHOICES = (
        ('card', 'کارت به کارت'),
        ('online', 'آنلاین'),
        ('cash', 'نقدی'),
    )

    TYPE_CHOICES2 = (
        ('confirm', 'تایید شده'),
        ('failed', 'ناموفق'),
    )

    payment_id = models.BigIntegerField(default=0)
    price = models.BigIntegerField(default=0)
    type_of_payment = models.CharField(max_length=200, choices=TYPE_CHOICES)
    date = models.CharField(max_length=200)
    account_destination_number = models.BigIntegerField(default=0)
    account_genesis_number = models.BigIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(choices=TYPE_CHOICES2, max_length=100, default='failed')

    def __str__(self):
        return f'{self.payment_id}'
    





class Order(models.Model):
    TYPE_CHOICES = (
        ('sell', 'فروش'),
        ('buy', 'خرید'),
    )

    TYPE_CHOICES2 = (
        ('unknown', 'نامشخص'),
        ('expire', 'فسخ شده'),
        ('confirm', 'تایید شده'),
    )

    TYPE_CHOICES3 = (
        ('unpaid', 'پرداخت نشده'),
        ('payed', 'پرداخت شده'),
    )

    TYPE_CHOICES4 = (
        ('not_deliver', 'تحویل داده نشده'),
        ('deliver', 'تحویل داده شده'),
    )
    TYPE_CHOICES5 = (
        ('admin_pannel', 'پنل ادمین'),
        ('user_pannel', 'پنل کاربری'),
    )
    created_at = models.DateTimeField(default=now)
    type_of_deal = models.CharField(max_length=200, choices=TYPE_CHOICES)
    weight = models.BigIntegerField(default=0)
    soot = models.FloatField(default=0)
    price = models.BigIntegerField(default=0)
    main_price = models.BigIntegerField(default=0)
    user_debt_amount = models.BigIntegerField(default=0)
    user_credit_amount = models.BigIntegerField(default=0)
    buy_date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_date = models.DateField(null=True, blank=True)
    payment_status = models.CharField(choices=TYPE_CHOICES3, max_length=100, null=True, blank=True)
    delivery_status = models.CharField(choices=TYPE_CHOICES4, max_length=100, null=True, blank=True)
    deal_status = models.CharField(max_length=200, choices=TYPE_CHOICES2, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    factor_number = models.IntegerField(default=0)
    ok_responde = models.PositiveBigIntegerField(default=0)


    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='orders' # نام معکوس برای دسترسی از Product به Orderها
    )
    source_order = models.CharField(max_length=200, choices=TYPE_CHOICES5)
    def get_jalali_date(self):
        jalali_date = jdatetime.datetime.fromgregorian(datetime=self.created_at)

        # Define Persian month and weekday names
        persian_months = {
            "Farvardin": "فروردین", "Ordibehesht": "اردیبهشت", "Khordad": "خرداد",
            "Tir": "تیر", "Mordad": "مرداد", "Shahrivar": "شهریور",
            "Mehr": "مهر", "Aban": "آبان", "Azar": "آذر",
            "Dey": "دی", "Bahman": "بهمن", "Esfand": "اسفند"
        }

        persian_weekdays = {
            "Saturday": "شنبه", "Sunday": "یکشنبه", "Monday": "دوشنبه",
            "Tuesday": "سه‌شنبه", "Wednesday": "چهارشنبه", "Thursday": "پنجشنبه", "Friday": "جمعه"
        }

        # Get English weekday and month
        weekday_en = jalali_date.strftime('%A')
        month_en = jalali_date.strftime('%B')

        # Convert to Persian
        weekday_fa = persian_weekdays.get(weekday_en, weekday_en)
        month_fa = persian_months.get(month_en, month_en)

        # Return formatted Persian date
        return f"{weekday_fa} {jalali_date.day} {month_fa} {jalali_date.year}"

    def __str__(self):
        return self.type_of_deal
