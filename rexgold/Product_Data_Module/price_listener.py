# order_module/utils/price_listener.py
import json
import redis
import threading
from django.core.cache import cache
from .price_cache import update_price_cache
import os
redis_host = 'redis' if os.getenv('DOCKER_ENV') else 'localhost'

redis_sub = redis.Redis(
    host=redis_host,
    port=6379,
    db=0,
    decode_responses=True
)

def handle_price_message(message):
    try:
        data = json.loads(message['data'])
        if data.get('event') == 'price_updated':
            product = data['product']
            label = product['label']
            new_buy = product['new_buy']
            new_sell = product['new_sell']

            # آپدیت کش ماژول سفارشات
            cache.set(f"price_buy_{label}", new_buy, timeout=None)
            cache.set(f"price_sell_{label}", new_sell, timeout=None)

            print(f"Cache updated in orders: {product['title']} → خرید: {new_buy}, فروش: {new_sell}")

            # اینجا می‌تونی WebSocket بفرستی
            # from channels.layers import get_channel_layer
            # channel_layer = get_channel_layer()
            # async_to_sync(channel_layer.group_send)("price_alerts", {...})

    except Exception as e:
        print("Error in price listener:", e)






def start_price_listener():
    host = os.getenv('REDIS_HOST', 'localhost')
    try:
        r = redis.Redis(host=host, port=6379, db=0, decode_responses=True)
        pubsub = r.pubsub()
        pubsub.subscribe("price_updates")
        print(f"[Listener] Subscribed to price_updates on {host}")

        for message in pubsub.listen():
            if message['type'] == 'message':
                data = json.loads(message['data'])
                if data.get('event') == 'price_updated':
                    p = data['product']
                    update_price_cache(p['label'], p['title'], p['new_buy'], p['new_sell'])
    except Exception as e:
        print(f"[Listener] ERROR: {e}")