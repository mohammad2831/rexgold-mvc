from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
import jdatetime
from datetime import date
import random
from django.utils.timezone import now


class UserPermission(models.Model):
    permission = models.CharField(max_length=255)

    def __str__(self):
        return self.permission




class UserGroup(models.Model):
    name = models.CharField(max_length=50)
   
    def __str__(self):
        return f'{self.name} - {self.id}'


class User(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_groups',  # نام یکتا
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',  # نام یکتا
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    TYPE_CHOICES = (
        ('در انتظار بررسی', 'در انتظار بررسی'),
        ('معرفی معرف', 'معرفی معرف'),
        ('واگذاری وثیقه', 'واگذاری وثیقه'),
        ('تأیید شده', 'تأیید شده'),
    )
    TYPE_CHOICES2 = (
        ('1', 'بنکداران (بازار)'),
        ('2', 'همکار'),
        ('3', 'متفرقه'),
        ('4', 'سازنده'),
        ('5', 'مخارج'),
        ('6', 'کیفی'),
        ('7', 'تراشکار'),
        ('8', 'ویترین'),
        ('9', 'جواهر'),
        ('10', 'صندوق'),
        ('11', 'سرمایه'),
        ('12', 'کارمندان'),
    )
    TYPE_CHOICES3 = (
        ('user', 'کاربر معمولی '),
        ('employee', 'کارمند '),
        ('admin', 'ادمین'),
    )

    active_session_key = models.CharField(max_length=40, null=True, blank=True, db_index=True)
    phone_number = models.CharField(max_length=11, unique=True, blank=True, null=True)
    request_status = models.CharField(choices=TYPE_CHOICES, max_length=100, default=TYPE_CHOICES[0][0])
    invited_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True)
    image_profile = models.ImageField(upload_to='images/', null=True, blank=True)
    guarantee_amount = models.PositiveBigIntegerField(null=True, blank=True)
    user_type = models.CharField(choices=TYPE_CHOICES2, max_length=100, blank=True, null=True)
    cod_meli = models.PositiveBigIntegerField(null=True, blank=True)
    invite_code = models.PositiveBigIntegerField(unique=True, null=True, blank=True)
    user_status = models.CharField(choices=TYPE_CHOICES3, max_length=100, default='user')
    address = models.TextField(null=True, blank=True)
    shomare_shaba = models.PositiveBigIntegerField(null=True, blank=True)
    shomare_hesab = models.PositiveBigIntegerField(null=True, blank=True)
    tah_hesab_user_id = models.PositiveBigIntegerField(null=True, blank=True)
    can_invite = models.BooleanField(default=False)
    #gold_limit = models.PositiveSmallIntegerField(null=True, blank=True)
    #price_limit = models.FloatField(null=True, blank=True)
    #sell_limit = models.FloatField(null=True, blank=True)
    # user_page_permissions = models.ManyToManyField(UserPermission, blank=True)  # اگر دارید
    rasteh = models.PositiveBigIntegerField(null=True, blank=True)
    city = models.TextField(null=True, blank=True)
    birth_date = models.CharField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    max_gold_debt_amount = models.BigIntegerField(default=0)
    group = models.ForeignKey(
        'UserGroup',  # یا Admin_Pannel_Module.UserGroup
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='members'
    )

    # --- مهم: REQUIRED_FIELDS مثل پروژه قبلی ---
    REQUIRED_FIELDS = ['phone_number']

    # --- متد save دقیقاً مثل پروژه قبلی ---
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if is_new and not self.invite_code:
            while True:
                invite_code = random.randint(10000000, 99999999)
                if not User.objects.filter(invite_code=invite_code).exists():
                    self.invite_code = invite_code
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username