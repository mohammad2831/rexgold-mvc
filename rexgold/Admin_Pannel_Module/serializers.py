from rest_framework import serializers
#from GoldData_Module.models import SellGoldToUs, BuyGoldFromUs
from Account_Module.models import User, UserGroup 
from Product_Data_Module.models import Product, Category
from Price_Mnage_Module.models import Access_All,Access_By_User,Access_By_UserGroup
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from django.utils import timezone
from datetime import timedelta
from django.core.cache import cache
USER_ONLINE_KEY_PREFIX = "online_user_"
KEY_PREFIX = "mykey::1:"


ONLINE_USERS_SET_KEY = "online:users:set"


class AdminGetProfitUserViewSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='product.id', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)

    class Meta:
        model = Access_By_UserGroup
        fields = [
            'product_id', 'user_id',
            'profit_sell', 'profit_buy',
            'active_for_sell', 'active_for_buy',
            'max_weight_buy', 'min_weight_buy',
            'max_weight_sell', 'min_weight_sell',
        
        ]



class AdminAddProfitUserViewSerializer(serializers.ModelSerializer):
     # --- ورودی (write_only) ---
    product_id = serializers.IntegerField(write_only=True, required=True)
    user_id = serializers.IntegerField(write_only=True, required=True)

    # --- خروجی (read_only) ---
    product_display_id = serializers.IntegerField(source='product.id', read_only=True)
    user_display_id = serializers.IntegerField(source='group.id', read_only=True)

    class Meta:
        model = Access_By_UserGroup
        fields = [
            # ورودی
            'product_id', 'user_id',
            # خروجی
            'product_display_id', 'user_display_id',
            # فیلدهای اصلی
            'profit_sell', 'profit_buy',
            'active_for_sell', 'active_for_buy',
            'max_weight_buy', 'min_weight_buy',
            'max_weight_sell', 'min_weight_sell',
        ]
        extra_kwargs = {
            'profit_sell': {'required': False, },
            'profit_buy': {'required': False, },
            'active_for_sell': {'required': False, },
            'active_for_buy': {'required': False, },
            'max_weight_buy': {'required': False, },
            'min_weight_buy': {'required': False, },
            'max_weight_sell': {'required': False, },
            'min_weight_sell': {'required': False, },
        }

class AdminGetProfitUserGroupViewSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='product.id', read_only=True)
    group_id = serializers.IntegerField(source='group.id', read_only=True)

    class Meta:
        model = Access_By_UserGroup
        fields = [
            'product_id', 'group_id',
            'profit_sell', 'profit_buy',
            'active_for_sell', 'active_for_buy',
            'max_weight_buy', 'min_weight_buy',
            'max_weight_sell', 'min_weight_sell',

        ]



class AdminAddProfitUserGroupViewSerializer(serializers.ModelSerializer):
    # --- ورودی (write_only) ---
    product_id = serializers.IntegerField(write_only=True, required=True)
    group_id = serializers.IntegerField(write_only=True, required=True)

    # --- خروجی (read_only) ---
    product_display_id = serializers.IntegerField(source='product.id', read_only=True)
    group_display_id = serializers.IntegerField(source='group.id', read_only=True)

    class Meta:
        model = Access_By_UserGroup
        fields = [
            # ورودی
            'product_id', 'group_id',
            # خروجی
            'product_display_id', 'group_display_id',
            # فیلدهای اصلی
            'profit_sell', 'profit_buy',
            'active_for_sell', 'active_for_buy',
            'max_weight_buy', 'min_weight_buy',
            'max_weight_sell', 'min_weight_sell',
        ]
        extra_kwargs = {
            'profit_sell': {'required': False, },
            'profit_buy': {'required': False, },
            'active_for_sell': {'required': False, },
            'active_for_buy': {'required': False, },
            'max_weight_buy': {'required': False, },
            'min_weight_buy': {'required': False, },
            'max_weight_sell': {'required': False, },
            'min_weight_sell': {'required': False, },
        }

class AdminGetLastProfitAllViewSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='product.id', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)  # یا str(product)

    class Meta:
        model = Access_All
        fields = [
            'product_id', 'product_name',
            'profit_sell', 'profit_buy',
            'active_for_sell', 'active_for_buy',
            'max_weight_buy', 'min_weight_buy',
            'max_weight_sell', 'min_weight_sell'
        ]
        extra_kwargs = {
            'profit_sell': {'required': False, },
            'profit_buy': {'required': False, },
            'active_for_sell': {'required': False, },
            'active_for_buy': {'required': False, },
            'max_weight_buy': {'required': False, },
            'min_weight_buy': {'required': False, },
            'max_weight_sell': {'required': False, },
            'min_weight_sell': {'required': False, },
        }


class AdminAddProfitAllViewSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)


    class Meta:
        model = Access_All
        fields = ['product_id', 'profit_sell', 'profit_buy', 'active_for_sell', 'active_for_buy']
        extra_kwargs = {
            'product_id':{'required': True},
            'profit_sell': {'required': True},
            'profit_buy': {'required': True},
            'active_for_sell': {'required': True},
            'active_for_buy': {'required': True},
        }





class AdminDetailUserGroupViewSerializer(serializers.ModelSerializer):
    pass



class AdminListUserGroupViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGroup
        fields = ['id', 'name']
class AdminAddUserGroupViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGroup 
        fields = ['id','name'] 
        
'''
# serializer for add productclass 
class AdminAddProductViewSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = Product
        fields = ['name', 'weight', 'fee_percent', 'price', 'user', 'image', 'type']
        extra_kwargs = {
            'name': {'required': True},
            'user': {'required': True},
            'price': {'required': True},
            'type': {'required': True},
        }

    def validate(self, data):
        if data.get('type') == 'by_weight' and not data.get('weight'):
            raise serializers.ValidationError("وزن برای فروش بر اساس وزن اجباری است.")
        
        if data.get('price') and data['price'] < 0:
            raise serializers.ValidationError("قیمت نمی‌تواند منفی باشد.")
        
        
        if data.get('user') and not User.objects.filter(id=data['user'].id).exists():
            raise serializers.ValidationError("کاربر معتبر نیست.")
        
        return data
'''











class UpdateCommissionAPISerializer(serializers.ModelSerializer):
    pass


class AdminLoginViewSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)



class AdminVerifyLoginViewSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    otp = serializers.CharField(max_length=6)

















        
































































#user 
class AdminAddUserViewSerializer(serializers.ModelSerializer):
    shomare_shaba = serializers.IntegerField(required=False)
    shomare_hesab = serializers.IntegerField(required=False)

    class Meta:
        model = User
        fields = ['id','username', 'phone_number', 'shomare_shaba','shomare_hesab','user_status','user_type','group','tah_hesab_user_id','is_active','max_gold_debt_amount']
        extra_kwargs = {
            'username': {'required': True},
            'phone_number': {'required': True},
            'user_status': {'required': True},
            'user_type': {'required': True},
            'group': {'required': False},
            
        }


class AdminDetailUserViewSerializer(serializers.ModelSerializer):
    request_status = serializers.CharField(source='get_request_status_display', read_only=True)
    class Meta:
        model = User
        fields = [
            'phone_number','request_status',
            'invited_by','image_profile',
            'guarantee_amount','user_type',
            'cod_meli','invite_code',
            'user_status','address',
            'shomare_shaba','shomare_hesab',
            'tah_hesab_user_id','can_invite',
            'city','birth_date'
            ,'is_active','max_gold_debt_amount',
            'group'
                  
                  ]



class AdminListUserViewSerializer(serializers.ModelSerializer):
    is_online = serializers.SerializerMethodField()
    group_name = serializers.CharField(source='group.name', read_only=True, default='-')

    class Meta:
        model = User  # <-- باید این خط را اضافه کنید
        fields = [
            'id', 'username', 'phone_number', 'user_type',
            'group', 'group_name', 'is_online',
            'request_status', 'is_active'
        ]
    # --- ۱. واکشی کلیدها قبل از شروع سریالایزر ---
    def to_representation(self, instance):
        
        # اگر این لیست هنوز در 'context' نباشد، آن را واکشی می‌کنیم
        if 'online_user_ids_set' not in self.context:
            
            # دسترسی به کلاینت Redis خام (برای استفاده از دستور KEYS)
            redis_client = cache.client.get_client(None) 
            
            # ساخت الگوی جستجوی کامل با پیشوند ثابت شما
            # نکته: ما از 'mykey::1:' در اینجا فرض کردیم که در تنظیمات KEY_PREFIX استفاده شده
            search_pattern = f"{self.context.get('KEY_PREFIX', 'mykey::1:')}{USER_ONLINE_KEY_PREFIX}*"

            # اجرای دستور KEYS
            # خروجی: لیستی از بایت‌ها (مثلاً [b'mykey::1:online_user_123', ...])
            full_keys = redis_client.keys(search_pattern) 
            
            online_ids = set()
            
            # استخراج ID کاربر
            online_prefix = f"{self.context.get('KEY_PREFIX', 'mykey::1:')}{USER_ONLINE_KEY_PREFIX}"

            for full_key_bytes in full_keys:
                full_key_str = full_key_bytes.decode('utf-8')
                
                # حذف پیشوند کامل برای استخراج ID
                if full_key_str.startswith(online_prefix):
                    user_id = full_key_str[len(online_prefix):]
                    online_ids.add(user_id)

            # ذخیره Set آیدی‌ها در Context برای استفاده‌های بعدی (cache کردن در حین سریالایز کردن)
            self.context['online_user_ids_set'] = online_ids
            
        return super().to_representation(instance)

    # --- ۲. استفاده از لیست واکشی شده ---
    def get_is_online(self, obj):
        """
        بررسی آنلاین بودن کاربر با استفاده از لیست ذخیره شده در Context
        """
        # آیدی‌های واکشی شده از Redis را از Context می‌خوانیم.
        online_user_ids_set = self.context.get('online_user_ids_set', set())
        
        # بررسی می‌کنیم که آیا ID کاربر فعلی در آن Set وجود دارد یا خیر.
        return str(obj.id) in online_user_ids_set


class AdminUpdateUserViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number','request_status','invited_by','image_profile','guarantee_amount','user_type','cod_meli','user_status','address','shomare_shaba','shomare_hesab','tah_hesab_user_id','can_invite','city','is_active','max_gold_debt_amount','group']





#product
class AdminListViewProductserializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)  

    class Meta:
        model = Product
        fields = ['id', 'name', 'weight', 'fee_percent', 'price', 'user_creator', 'date', 'image', 'type']
        read_only_fields = ['id', 'date', 'user_creator'] 


class AdminDetailProductViewSerializer(serializers.ModelSerializer): 
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    
    class Meta:
        model = Product
        fields = [
             'id','name','weight','fee_percent','price','user_creator','date','image','type','category', 'type_display'
         ]


class AdminAddProductViewSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    user_creator = serializers.CharField(required=False)

    class Meta:
        model = Product
        fields = ['id','name', 'weight', 'fee_percent', 'price', 'user_creator', 'image', 'type']
        extra_kwargs = {
            'name': {'required': True},
            'price': {'required': True},
            'type': {'required': True},
        }

    def validate(self, data):
        if data.get('type') == 'by_weight' and not data.get('weight'):
            raise serializers.ValidationError("وزن برای فروش بر اساس وزن اجباری است.")
        
        if data.get('price') and data['price'] < 0:
            raise serializers.ValidationError("قیمت نمی‌تواند منفی باشد.")
        
        
        if data.get('user') and not User.objects.filter(id=data['user'].id).exists():
            raise serializers.ValidationError("کاربر معتبر نیست.")
        
        return data
    

class AdminUpdateProductViewSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = Product
        # ID برای نمایش خروجی اضافه شد
        fields = ['id', 'name', 'weight', 'fee_percent', 'price', 'user_creator', 'image', 'type'] 
        extra_kwargs = {
            'id': {'read_only': True}, # <--- اطمینان از خواندنی بودن ID
            'name': {'required': False}, 
            'user_creator': {'required': False},  
            'price': {'required': False}, 
            'type': {'required': False},  
        }

    def validate(self, data):
        # 1. اعتبارسنجی وابستگی weight به type
        # اگر فیلد 'type' در داده‌های به‌روزرسانی وجود نداشته باشد، باید از شیء موجود (instance) خوانده شود
        current_type = data.get('type', self.instance.type if self.instance else None)
        
        if current_type == 'by_weight' and not data.get('weight') and (self.instance and self.instance.weight is None):
            raise serializers.ValidationError("وزن برای فروش بر اساس وزن اجباری است.")
        
        # 2. بررسی قیمت منفی
        if data.get('price') and data['price'] < 0:
            raise serializers.ValidationError("قیمت نمی‌تواند منفی باشد.")
        
        # 3. اعتبارسنجی وجود کاربر (اصلاح شده برای پذیرش ID یا Instance)
        if 'user_creator' in data:
            user_input = data['user_creator']
            user_id = user_input.id if hasattr(user_input, 'id') else user_input # تلاش برای استخراج ID
            
            if isinstance(user_id, int) and not User.objects.filter(id=user_id).exists():
                raise serializers.ValidationError({'user_creator': "کاربر معتبر نیست."})

  
        
        return data
    

class AdminDeleteProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name'] 
        read_only_fields = ['id', 'name']







#category

class AdminListCategoryViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category 
        fields = ['id', 'name'] 
        read_only_fields = ['id', 'name']


class AdminAddCategoryViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category 
        fields = ['id','name'] 
        


class AdminDetailCategoryViewSerializer(serializers.ModelSerializer):
    products = AdminDeleteProductSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'name', 'products']
