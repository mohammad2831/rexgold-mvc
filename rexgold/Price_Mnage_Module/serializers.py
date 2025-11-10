from rest_framework import serializers
from Price_Mnage_Module.models import Access_All,Access_By_User,Access_By_UserGroup



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




