from django_filters import rest_framework as filters
from django.db.models import Q
from Account_Module.models import User
from django.core.cache import cache

USER_ONLINE_KEY_PREFIX = "online_user_"
KEY_PREFIX = "mykey::1:"  # پیشوند کامل جنگو/ردیس
# --- کلیدهای Redis ---
ONLINE_USERS_SET_KEY = "online:users:set"

def get_online_user_ids_from_redis():
    """
    ID کاربران آنلاین را با جستجوی کلیدها در Redis واکشی می‌کند.
    """
    try:
        redis_client = cache.client.get_client(None)
    except AttributeError:
        # در صورتی که تست‌ها بدون تنظیمات Redis اجرا شوند
        return set()

    # ساخت الگوی جستجوی کامل (باید دقیقاً پیشوند جنگو را شامل شود)
    # شما باید این پیشوند را از تنظیمات خود بخوانید یا ثابت نگه دارید.
    # مثال: "mykey::1:online_user_*"
    # در اینجا از یک راه حل کلی‌تر استفاده می‌کنم و فرض می‌کنم KEY_PREFIX درست است:
    # ما باید بخش 'mykey::1:' را به صورت ثابت در کد بیاوریم، زیرا تنظیمات FilterSet اجازه نمی‌دهد Context را پاس دهید.
    
    # هشدار: لطفا MY_FULL_PREFIX را با پیشوند دقیق پروژه خود جایگزین کنید (مثلاً "mykey::1:").
    MY_FULL_PREFIX = "mykey::1:"
    
    search_pattern = f"{MY_FULL_PREFIX}{USER_ONLINE_KEY_PREFIX}*"
    
    # اجرای دستور KEYS
    full_keys = redis_client.keys(search_pattern)
    
    online_ids = set()
    # محاسبه طول پیشوند برای استخراج ID
    prefix_len = len(f"{MY_FULL_PREFIX}{USER_ONLINE_KEY_PREFIX}") 

    for full_key_bytes in full_keys:
        full_key_str = full_key_bytes.decode('utf-8')
        # استخراج ID از انتهای کلید
        user_id = full_key_str[prefix_len:]
        
        try:
            # ID را به integer تبدیل می‌کنیم تا در کوئری جنگو استفاده شود
            online_ids.add(int(user_id))
        except ValueError:
            # اگر ID عدد نبود، آن را نادیده می‌گیریم
            continue

    return online_ids


class UserFilter(filters.FilterSet):
    search = filters.CharFilter(method='filter_search')
    user_type = filters.ChoiceFilter(choices=User.TYPE_CHOICES2, label='دسته‌بندی')
    request_status = filters.ChoiceFilter(choices=User.TYPE_CHOICES, label='وضعیت')
    is_online = filters.BooleanFilter(method='filter_is_online', label='آنلاین؟')
    status = filters.BooleanFilter(field_name='is_active', label='فعال/غیرفعال')

    def filter_search(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(
            Q(username__icontains=value) |
            Q(phone_number__icontains=value)
        )

    def filter_is_online(self, queryset, name, value):
        # ۱. واکشی IDهای آنلاین از Redis
        # از تابع کمکی که در بالا تعریف شد استفاده می‌کنیم.
        online_ids = get_online_user_ids_from_redis()
        
        # نکته: نیازی به تبدیل دوباره به int نیست، زیرا تابع کمکی آن را انجام می‌دهد.

        if value is True:
            # فقط کاربرانی که ID آنها در لیست آنلاین‌ها است
            return queryset.filter(id__in=online_ids)
        elif value is False:
            # فقط کاربرانی که ID آنها در لیست آنلاین‌ها نیست (آفلاین هستند)
            return queryset.exclude(id__in=online_ids)
        else:
            # اگر فیلتر اعمال نشده یا مقدار None داشت (رفتار پیش‌فرض BooleanFilter)
            return queryset

    class Meta:
        model = User
        fields = ['search', 'user_type', 'request_status', 'status', 'is_online']