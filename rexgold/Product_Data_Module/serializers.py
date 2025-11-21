from rest_framework import serializers
from . models import Category, Product
from Account_Module.models import User








#product
class AdminListViewProductserializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)  

    class Meta:
        model = Product
        fields = ['id', 'name', 'weight', 'fee_percent', 'price', 'image', 'type']
        read_only_fields = ['id', 'date', 'user_creator'] 


class AdminDetailProductViewSerializer(serializers.ModelSerializer): 
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    
    class Meta:
        model = Product
        fields = [
             'id','name','weight','fee_percent','price','user_creator','date','image','type','category', 'type_display', 'max_weight_sellbuy_order', 'min_weight_sellbuy_order', 'max_wheight_automate_order'
         ]


class AdminAddProductViewSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    user_creator = serializers.CharField(required=False)

    class Meta:
        model = Product
        fields = ['id','name', 'weight', 'fee_percent', 'price', 'user_creator', 'image', 'type', 'category', 'max_weight_sellbuy_order', 'min_weight_sellbuy_order', 'max_wheight_automate_order']
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
        fields = ['id', 'name', 'weight', 'fee_percent', 'price', 'user_creator', 'image', 'type', 'category', 'max_weight_sellbuy_order', 'min_weight_sellbuy_order', 'max_wheight_automate_order'] 
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

