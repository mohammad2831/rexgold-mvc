# serializers.py
from rest_framework import serializers
from Product_Data_Module.models import Product

class UserAddOrderViewSerializer(serializers.Serializer):
    type_of_deal = serializers.ChoiceField(choices=['buy', 'sell'])
    weight = serializers.IntegerField(min_value=1)
    soot = serializers.FloatField(min_value=0, max_value=100, required=False, allow_null=True)
    price = serializers.IntegerField(min_value=1)
    main_price = serializers.IntegerField(min_value=0, required=False)
    delivery_date = serializers.DateField(required=False, allow_null=True)
    description = serializers.CharField(max_length=1000, required=False, allow_blank=True)
    
    
    product_id = serializers.PrimaryKeyRelatedField(
    queryset=Product.objects.all(),
    source='product',  # این مهمه!
    write_only=True
    )
    source_order = serializers.ChoiceField(choices=['user_pannel', 'admin_pannel'])

    def validate_source_order(self, value):
        if value != 'user_pannel':
            raise serializers.ValidationError("فقط از طریق پنل کاربری می‌توانید سفارش ثبت کنید.")
        return value
'''
    def validate(self, attrs):
        # بررسی اینکه محصول فعال باشد (در کوئری‌ست بالا هم هست، ولی دوبار چک امن‌تره)
        product = attrs['product_id']
        if not product.is_active:
            raise serializers.ValidationError("محصول انتخاب‌شده در دسترس نیست.")
        return attrs

        '''