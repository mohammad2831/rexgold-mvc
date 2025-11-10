from rest_framework import serializers
from . models import Order
from Account_Module.models import User
from Product_Data_Module.models import Product


class AdminAddOrderViewSerializer(serializers.ModelSerializer):
    # تعیین صریح نوع فیلد برای تضمین دریافت ID (عدد صحیح)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = Order
        fields = (
            'id',  
            'type_of_deal',
            'weight',
            'price',
            'main_price',
            'user',      
            'product',   
        )
        read_only_fields = ('id',)



class AdminListOrderViewSerializer(serializers.ModelSerializer):


    class Meta:
        model = Order
        fields = (
'id','user','type_of_deal','weight','product','main_price','price','factor_number','created_at','deal_status'  
        )
        read_only_fields = ('id',)









      
