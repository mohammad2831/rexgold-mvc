from django_filters import rest_framework as filters
from django.db.models import Q
from Admin_Module.models import User, Product, Category

class UserFilter(filters.FilterSet):
    # جستجوی ترکیبی
    search = filters.CharFilter(method='filter_search')
    
    # فیلتر نوع کاربر (دسته‌بندی)
    user_type = filters.ChoiceFilter(choices=User.TYPE_CHOICES2, label='دسته‌بندی')
    
    # فیلتر وضعیت درخواست (فعال/غیرفعال)
    request_status = filters.ChoiceFilter(choices=User.TYPE_CHOICES, label='وضعیت')
    
    # فیلتر آنلاین/آفلاین
    is_online = filters.BooleanFilter(method='filter_is_online', label='آنلاین؟')

    # فیلتر فعال/غیرفعال (is_active)
    status = filters.BooleanFilter(field_name='is_active', label='فعال/غیرفعال')

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(username__icontains=value) |
            Q(phone_number__icontains=value)
        )

    def filter_is_online(self, queryset, name, value):
        if value is True:
            return queryset.filter(active_session_key__isnull=False)
        elif value is False:
            return queryset.filter(active_session_key__isnull=True)
        return queryset

    class Meta:
        model = User
        fields = ['search', 'user_type', 'request_status', 'status', 'is_online']