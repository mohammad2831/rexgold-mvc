# order_module/utils/price_cache.py
from django.core.cache import cache
from datetime import datetime

# لیست ثابت همه محصولات
ALL_PRODUCTS = [
    {"label": "naghd-farda", "title": "نقد فردا"},
    {"label": "robe-86", "title": "ربع 86"},
    {"label": "naghd-pasfarda", "title": "نقد پسفردا"},
    {"label": "abshode-kart", "title": "آبشده کارتخوان"},
    {"label": "nim-86", "title": "نیم سکه 86"},
    {"label": "tamam-86", "title": "تمام سکه 86"},
]

LATEST_PRICES_KEY = "latest_prices"
LATEST_UPDATE_KEY = "latest_prices_updated_at"
def update_price_cache(label: str, title: str, buy: str, sell: str):
    prices = cache.get(LATEST_PRICES_KEY, {})
    prices[label] = {"title": title, "buy": buy, "sell": sell}
    cache.set(LATEST_PRICES_KEY, prices, timeout=None)
    cache.set(LATEST_UPDATE_KEY, datetime.utcnow().isoformat() + "Z", timeout=None)

def get_all_prices():
    cached = cache.get(LATEST_PRICES_KEY, {})
    updated_at = cache.get(LATEST_UPDATE_KEY, "نامشخص")
    result = []
    for p in ALL_PRODUCTS:
        label = p["label"]
        item = cached.get(label, {})
        result.append({
            "title": p["title"],
            "buy": item.get("buy", "-"),
            "sell": item.get("sell", "-")
        })
    return {
        "updated_at": updated_at,
        "count": len([x for x in result if x["buy"] != "-"]),
        "prices": result
    }