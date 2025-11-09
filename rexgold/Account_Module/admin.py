from django.contrib import admin
from . import models
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from django import forms


@admin.register(models.UserGroup)
class UserGroup(admin.ModelAdmin):
    list_display = ('name',)





class UserForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = '__all__'

    def save(self, commit=True):
        user = super().save(commit=False)

        if self.cleaned_data.get('clear_groups', False):
            user.groups.clear()

        if commit:
            user.save()
        return user


class CustomUserAdmin(UserAdmin):
    form = UserForm
    model = models.User
    list_display = ('id','username', 'phone_number', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined',)
    list_editable = ('is_active',)
    #filter_horizontal = ('user_page_permissions',)
    search_fields = ('username', 'phone_number', 'first_name', 'last_name')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Customize',{'fields':('tah_hesab_user_id',
                                'active_session_key','phone_number','request_status','invited_by',
                                'guarantee_amount','user_type','cod_meli','invite_code','can_invite','user_status','address',
                                'shomare_shaba','shomare_hesab',
                                'rasteh','city','birth_date','group','groups')})
    )



    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
            'username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'is_active', 'is_staff',
            'groups'),
        }),
    )


# Register the custom UserAdmin

admin.site.register(models.User, CustomUserAdmin)
