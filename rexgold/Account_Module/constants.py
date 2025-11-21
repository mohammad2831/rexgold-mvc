# your_app/constants.py

USER_TYPE_CHOICES = [
    {"value": "1", "label": "بنکداران (بازار)"},
    {"value": "2", "label": "همکار"},
    {"value": "3", "label": "متفرقه"},
    {"value": "4", "label": "سازنده"},
    {"value": "5", "label": "مخارج"},
    {"value": "6", "label": "کیفی"},
    {"value": "7", "label": "تراشکار"},
    {"value": "8", "label": "ویترین"},
    {"value": "9", "label": "جواهر"},
    {"value": "10", "label": "صندوق"},
    {"value": "11", "label": "سرمایه"},
    {"value": "12", "label": "کارمندان"},
]

# اگر بعداً بخوای بقیه choices ها رو هم اضافه کنی:
USER_REQUEST_STATUS_CHOICES = [
    {"value": "در انتظار بررسی", "label": "در انتظار بررسی"},
    {"value": "معرفی معرف", "label": "معرفی معرف"},
    {"value": "واگذاری وثیقه", "label": "واگذاری وثیقه"},
    {"value": "تأیید شده", "label": "تأیید شده"},
]

USER_STATUS_CHOICES = [
    {"value": "user", "label": "کاربر معمولی"},
    {"value": "employee", "label": "کارمند"},
    {"value": "admin", "label": "ادمین"},
]