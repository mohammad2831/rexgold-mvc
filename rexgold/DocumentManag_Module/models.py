from django.db import models
from jalali_date import datetime2jalali
from Account_Module.models import User

class ImportExportMelt(models.Model):
    TYPE_CHOICES = (
        ('permanent','ثبت کل'),
        ('temporary','موقت'),
    )

    TYPE_CHOICES2 = (
        ('import','ورود '),
        ('export','خروج'),
    )

    TYPE_CHOICES3 = (
        ('melt', 'آبشده '),
        ('ect', 'متفرقه '),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    SabtKolORMovaghat = models.CharField(max_length=200, choices=TYPE_CHOICES)
    customer_kode = models.IntegerField()
    factor_number = models.PositiveBigIntegerField()
    row_number = models.IntegerField()
    weight = models.IntegerField()
    ayar = models.IntegerField()
    ang_number = models.IntegerField()
    lab_name = models.CharField(max_length=200)
    export_or_import = models.CharField(max_length=200, choices=TYPE_CHOICES2)
    melt_ot_etc = models.CharField(max_length=200, choices=TYPE_CHOICES3)
    description = models.TextField(max_length=700)

    def get_jalali_date(self):
        # Convert the datetime object to Jalali and return the formatted string
        jalali_date = datetime2jalali(self.date)
        return jalali_date.strftime('%Y/%m/%d %H:%M:%S')  # Including date and time

    get_jalali_date.admin_order_field = 'date'
    get_jalali_date.short_description = 'Jalali Date and Time'

    def __str__(self):
        return self.user.phone_number
class ImportExportMeltAllChash(models.Model):
    TYPE_CHOICES = (
        ('import', 'ورود '),
        ('export', 'خروج'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    customer_kode = models.IntegerField()
    factor_number = models.PositiveBigIntegerField()
    row_number = models.IntegerField()
    date = models.DateTimeField()  # Changed to DateTimeField
    import_or_export = models.CharField(max_length=200, choices=TYPE_CHOICES)
    price = models.BigIntegerField()
    description = models.TextField(max_length=700)

    def get_jalali_date(self):
        # Convert the datetime object to Jalali and return the formatted string
        jalali_date = datetime2jalali(self.created_date)
        return jalali_date.strftime('%Y/%m/%d %H:%M:%S')  # Including date and time

    get_jalali_date.admin_order_field = 'created_date'
    get_jalali_date.short_description = 'Jalali Date and Time'

    def __str__(self):
        return self.user.phone_number
class GetMoneyFromBank(models.Model):
    TYPE_CHOICES = (
        ('get_money','دریافت از مشتری'),
        ('pay_money','پرداخت به مشتری'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    customer_kode = models.IntegerField()
    factor_number = models.PositiveBigIntegerField()
    row_number = models.IntegerField()
    date = models.DateTimeField()  # Changed to DateTimeField
    get_or_pay_money = models.CharField(max_length=200, choices=TYPE_CHOICES)
    bank_name = models.CharField(max_length=200)
    price = models.BigIntegerField()
    cod_rahgiry = models.BigIntegerField()
    description = models.TextField(max_length=700)

    def get_jalali_date(self):
        # Convert the datetime object to Jalali and return the formatted string
        jalali_date = datetime2jalali(self.created_date)
        return jalali_date.strftime('%Y/%m/%d %H:%M:%S')  # Including date and time

    get_jalali_date.admin_order_field = 'created_date'
    get_jalali_date.short_description = 'Jalali Date and Time'

    def __str__(self):
        return self.user.phone_number
class DebtorCreditor(models.Model):
    TYPE_CHOICES = (
        ('creditor','طلب ما'),
        ('debt','بدهی ما'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    customer_kode = models.IntegerField()
    factor_number = models.PositiveBigIntegerField()
    row_number = models.IntegerField()
    date = models.DateTimeField()  # Changed to DateTimeField
    document_type = models.CharField(max_length=200, choices=TYPE_CHOICES)
    price = models.BigIntegerField()
    for_about = models.CharField(max_length=300)
    weight = models.BigIntegerField()
    description = models.TextField(max_length=700)

    def get_jalali_date(self):
        # Convert the datetime object to Jalali and return the formatted string
        jalali_date = datetime2jalali(self.created_date)
        return jalali_date.strftime('%Y/%m/%d %H:%M:%S')  # Including date and time

    get_jalali_date.admin_order_field = 'created_date'
    get_jalali_date.short_description = 'Jalali Date and Time'

    def __str__(self):
        return self.user.phone_number