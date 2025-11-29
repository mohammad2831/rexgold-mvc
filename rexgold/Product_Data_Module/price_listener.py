# order_module/utils/price_listener.py
import json
import threading
from django.conf import settings
from django.core.cache import cache
from .price_cache import update_price_cache


# استفاده از REDIS_PRICE که در settings.py تعریف کردیم
# فقط این یه خط کافیه!
redis_price = settings.REDIS_PRICE

# چنل قیمت — حتماً با پروژه اول یکسان باشه!
CHANNEL_PRICE_LIVE = settings.CHANNEL_PRICE_LIVE  # "prices:livedata"


def handle_price_message(message):
    """
    وقتی پروژه اول قیمت رو publish کرد، این اجرا میشه
    """
    try:
        data = json.loads(message['data'])
        # ساختار پیام رو با پروژه اول هماهنگ کن (مثلاً این شکلی باشه)
        symbol = data.get('symbol')
        price = data.get('price')
        timestamp = data.get('timestamp')

        if not symbol or price is None:
            return

        # آپدیت کش برای ماژول سفارشات (در redis-cache)
        cache.set(f"price_buy_{symbol}", price, timeout=None)
        cache.set(f"price_sell_{symbol}", price, timeout=None)

        print(f"Cache updated: {symbol} → {price:,} تومان")

        # اینجا می‌تونی وب‌سوکت بفرستی
        # from channels.layers import get_channel_layer
        # from asgiref.sync import async_to_sync
        # channel_layer = get_channel_layer()
        # async_to_sync(channel_layer.group_send)("prices", {"type": "price.update", "data": data})

    except Exception as e:
        print("Error in handle_price_message:", e)


def start_price_listener():
    """
    توی یه ترد جداگانه اجرا میشه و همیشه گوش میده
    """
    try:
        pubsub = redis_price.pubsub()
        pubsub.subscribe(CHANNEL_PRICE_LIVE)
        print(f"[Price Listener] Subscribed to channel: {CHANNEL_PRICE_LIVE}")

        for message in pubsub.listen():
            if message.get('type') == 'message':
                threading.Thread(target=handle_price_message, args=(message,), daemon=True).start()

    except Exception as e:
        print(f"[Price Listener] FATAL ERROR: {e}")
        # دوباره تلاش کن بعد از ۵ ثانیه
        import time
        time.sleep(5)
        threading.Thread(target=start_price_listener, daemon=True).start()


# شروع خودکار وقتی فایل لود میشه
threading.Thread(target=start_price_listener, daemon=True).start()