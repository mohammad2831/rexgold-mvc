from django.contrib import admin

from .models import Access_All, Access_By_UserGroup, Access_By_User


# کلاس Admin برای Access_All
class AccessAllAdmin(admin.ModelAdmin):
    list_display = ('product', 'profit_sell', 'profit_buy', 'active_for_sell', 'active_for_buy', 'time')
    list_filter = ('active_for_sell', 'active_for_buy')
    search_fields = ('product__name',) # اگر مدل Product فیلد 'name' دارد

admin.site.register(Access_All, AccessAllAdmin)


# کلاس Admin برای Access_By_UserGroup
class AccessByUserGroupAdmin(admin.ModelAdmin):
    list_display = ('group', 'product', 'profit_sell', 'profit_buy', 'active_for_sell', 'active_for_buy', 'time')
    list_filter = ('group', 'active_for_sell', 'active_for_buy')
    search_fields = ('group__name', 'product__name') 
    # برای جستجو در فیلدهای مربوط به گروه و محصول

admin.site.register(Access_By_UserGroup, AccessByUserGroupAdmin)


# کلاس Admin برای Access_By_User
class AccessByUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'profit_sell', 'profit_buy', 'active_for_sell', 'active_for_buy', 'time')
    list_filter = ('user', 'active_for_sell', 'active_for_buy')
    search_fields = ('user__username', 'product__name') 
    # برای جستجو بر اساس نام کاربری و نام محصول

admin.site.register(Access_By_User, AccessByUserAdmin)