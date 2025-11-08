import datetime
import redis
import requests
import logging
from django.utils import timezone
import json


'''

        # Connect to Redis
redis_instance = redis.StrictRedis(host='127.0.0.1',
                                        port=6379
                                        )

        # Set a key-value pair
redis_instance.set('my_key', 'my_value')

        # Set a key-value pair with an expiry time (e.g., 300 seconds)
redis_instance.setex('another_key', 300, 'another_value')

        # Store a dictionary (requires serialization, e.g., JSON)
import json
data = {'name': 'John Doe', 'age': 30}
redis_instance.set('user_data', json.dumps(data))
'''









API_TITLE_TO_PRODUCT = {
    "نقد فردا": "1",  # abshode_naghd_farda
    "پس فردایی": "2",  # abshode_with_gateway
    "تمام سکه 86": "8",  # seke_tamam_1386
    "نیم سکه 86": "3",   # seke_nim_1386
    "ربع سکه 86": "5",   # seke_rob_1386
    "تمام سکه تاریخ پایین": "9",  # seke_tamam_1403
    "نیم تاریخ پایین":"4",
    "ربع تاریخ پایین":"7",
}

# نگاشت product_id به نام محصول (برای Redis)
PRODUCT_ID_TO_NAME = {
    '1': 'abshode_naghd_farda',
    '2': 'abshode_with_gateway',
    '3': 'seke_nim_1386',
    '4': 'seke_nim_sal_payeen_ta_80',
    '5': 'seke_rob_1386',
    '6': 'seke_rob_1403',
    '7': 'seke_rob_sal_payeen_ta_80',
    '8': 'seke_tamam_1386',
    '9': 'seke_tamam_1403',
    '10': 'seke_tamam_sal_payeen',
}

# نگاشت shop_id به نام منبع
SHOP_ID_TO_NAME = {
    '1': 'hanzaei',
    '2': 'example_shop_1',
    '3': 'example_shop_2',
}

def get_prices_hanzaei():

    api_source = "hanzaei_api"
    url = "https://api.mohammadhanzaei.ir/products"
    headers = {
        "Host": "api.mohammadhanzaei.ir",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Cache-Control": "no-cache",
        "X-Verify": "964503326",
        "Origin": "https://panel.mohammadhanzaei.ir",
        "Connection": "keep-alive",
        "Referer": "https://panel.mohammadhanzaei.ir/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "TE": "trailers",
    }
    cookies = {
        "access_token_web": "eyJpdiI6Im9rWDNtcFkyM0R3QlB6Y09jZDByZ1E9PSIsInZhbHVlIjoiMXMxSkxIMUhCdVU0V091a01veUtLMmVCZzcxMHZYNTBhYTZ1djU0cHNwQmdaVHU3VDNNQjZkd1NUUExqNlU4ZkN3eFR5NlFuK29pOVRtc1BFT3psL1FMZDJhNERkSXNLbG9nOGZxZnZhbVZ3c08zSUNqSk9mSDNZYSt5cXJLUkxENmRRYmlaSnhsMHFpOXdGSHQvaTFmWUFPRUQrUDMyN2hJUXk4SzgyNlppbGdhNEpiS2ZQMFlQQUxtOXlIY05WTk15VWpxMWJRVTVpYlNOUGdRdHlTcXordkJ1VmlIdlFsYUh0Uld4RFVFVmFEblo2MHB6d0YyMGpzdytkeCt1Q3picUphSStYSHRrNnhwa0JFWE1NeXhPUmgyeXI3MmNnV0tVVEszNGxJakU9IiwibWFjIjoiMzUzYTNiOTgxZjI4OWUyZTVhZDY3YzIzMWQzYzJmZGVlNjA1NmU3MjNjOTcxZTQ2NWI5Y2JiN2MwZjBiYWUxNiIsInRhZyI6IiJ9"
    }

    try:
        # The data MUST be a dictionary containing keys like "data"
        simulated_api_response = {
    "status": "warning",
    "message": "Some products have invalid prices (-1).",
    "invalid_products": [
        {
            "category": "مسکوکات",
            "product": "نیم سکه 86",
            "buy_price": "48470000",
            "sell_price": -1
        },
        {
            "category": "مسکوکات",
            "product": "ربع سکه 86",
            "buy_price": "28170000",
            "sell_price": -1
        },
        {
            "category": "مسکوکات",
            "product": "تمام سکه تاریخ پایین",
            "buy_price": "86680000",
            "sell_price": -1
        },
        {
            "category": "مسکوکات",
            "product": "نیم تاریخ پایین",
            "buy_price": "43700000",
            "sell_price": -1
        },
        {
            "category": "مسکوکات",
            "product": "ربع تاریخ پایین",
            "buy_price": "22300000",
            "sell_price": -1
        }
    ],
    "data": [
        {
            "category": "آبشده",
            "products": [
                {
                    "title": "نقد فردا",
                    "buy_price": "37705000",
                    "sell_price": "37640000"
                },
                {
                    "title": "پس فردایی",
                    "buy_price": "38205000",
                    "sell_price": "38140000"
                }
            ]
        },
        {
            "category": "مسکوکات",
            "products": [
                {
                    "title": "تمام سکه 86",
                    "buy_price": "92680000",
                    "sell_price": "92310000"
                },
                {
                    "title": "نیم سکه 86",
                    "buy_price": "48470000",
                    "sell_price": -1
                },
                {
                    "title": "ربع سکه 86",
                    "buy_price": "28170000",
                    "sell_price": -1
                },
                {
                    "title": "تمام سکه تاریخ پایین",
                    "buy_price": "86680000",
                    "sell_price": -1
                },
                {
                    "title": "نیم تاریخ پایین",
                    "buy_price": "43700000",
                    "sell_price": -1
                },
                {
                    "title": "ربع تاریخ پایین",
                    "buy_price": "22300000",
                    "sell_price": -1
                }
            ]
        }
    ]
}


        # Now this will work correctly because simulated_api_response is a dictionary
        raw_data = simulated_api_response.get('data', [])
        invalid_products = simulated_api_response.get('invalid_products', [])
        categories_count = len(raw_data)
        
        return {
            'status': 'success',
            'message': f'Data fetched successfully: {categories_count} categories received',
            'invalid_products': invalid_products,
            'raw_data': raw_data
        }

    except Exception as e:
        # This block will now only catch unexpected errors
        return {
            'status': 'error',
            'message': f'Error processing API response: {str(e)}',
            'invalid_products': [],
            'raw_data': []
        }

def process_data_hanzaei():
    try:
        redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        redis_client.ping()
        print("Successfully connected to Redis!")
    except redis.exceptions.ConnectionError as e:
        print(f"Could not connect to Redis: {e}")
        redis_client = None


    api_response = get_prices_hanzaei()
    
    if api_response['status'] == 'error':
        print(f"Failed to get data: {api_response['message']}")
        return

    main_data = api_response.get('raw_data', [])
    invalid_products_list = api_response.get('invalid_products', [])
    
    print("--- Invalid Products Reported by API ---")
    print(invalid_products_list)
    print("\n--- Processing Valid Data ---")

    api_source = "hanzaei_api"
    processed_result = []
    current_time = datetime.datetime.now(datetime.timezone.utc).isoformat()

    for category in main_data:
        for product in category.get('products', []):
            product_title = product.get('title')
            buy_price = product.get('buy_price', '0')
            sell_price = product.get('sell_price', '0')
            
            # 1. Find the product ID
            product_id = API_TITLE_TO_PRODUCT.get(product_title)
            print(product_id)

            # 2. Skip if the product is not in our mapping or has invalid prices
            if not product_id or sell_price == -1 or buy_price == -1:
                continue

            # --- THIS IS THE FIX ---
            # 3. Create a new, processed dictionary with all the required keys
            processed_product = {
                'id': product_id,
                'title': product_title,
                'buy': buy_price,
                'sell': sell_price
                # You can add category_name or other fields here if needed
            }

            # 4. Pass the NEW 'processed_product' dictionary to your save functions
            save_to_redis(redis_client, processed_product, current_time)





            print(f"  -> Product: {product_title}, Buy: {buy_price}, Sell: {sell_price}, ID: {product_id}")


def save_to_redis(redis_client, product, current_time):
    """Saves a single processed product to Redis."""
    try:
        redis_key = f"hanzaei-{product['product_id']-{current_time}}" # This will now work correctly
        
        product_data = {
            'title': product['title'],
            'buy_price': product['buy'],   # Use the key from processed_product
            'sell_price': product['sell'], # Use the key from processed_product
            'last_update': datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
        
        redis_client.hset(redis_key, mapping=product_data)
    except KeyError as e:
        print(f"Error saving to Redis: Missing key {e} in product data.")
    except Exception as e:
        print(f"An unexpected error occurred while saving to Redis: {e}")


process_data_hanzaei()
         














































'''
            if not product_id or not shop_id:
                invalid_products.append({
                    'api_title': product_title,
                    'api_source': api_source,
                    'buy_price': buy_price,
                    'sell_price': sell_price,
                    'reason': 'Invalid product_id or shop_id'
                })
                logger.warning(f"Skipping product '{product_title}' - Invalid product_id or shop_id")
                continue

            try:
                buy_price_int = int(buy_price) if buy_price and buy_price != '-1' else 0
                sell_price_int = int(sell_price) if sell_price and sell_price != '-1' else 0
            except (ValueError, TypeError) as e:
                invalid_products.append({
                    'api_title': product_title,
                    'api_source': api_source,
                    'buy_price': buy_price,
                    'sell_price': sell_price,
                    'reason': f'Price conversion error: {str(e)}'
                })
                logger.warning(f"Invalid price for '{product_title}': buy={buy_price}, sell={sell_price}, error={e}")
                continue

            if buy_price_int == 0 or sell_price_int == 0:
                invalid_products.append({
                    'api_title': product_title,
                    'api_source': api_source,
                    'buy_price': buy_price_int,
                    'sell_price': sell_price_int,
                    'reason': 'Invalid price (0 or -1)'
                })
                logger.warning(f"Invalid price for '{product_title}': buy={buy_price_int}, sell={sell_price_int}")
                continue

            is_exist = is_active and (is_buy_active or is_sell_active)

            result.append({
                'product_id': product_id,
                'shop_id': shop_id,
                'base_price_buy': buy_price_int,
                'base_price_sell': sell_price_int,
                'is_exist': is_exist,
                'timestamp': current_time,
                'api_title': product_title,
                'api_source': api_source
            })

    if not result:
        logger.error("No valid products to store in Redis")
        return {
            'status': 'error',
            'message': 'No valid products to store',
            'invalid_products': invalid_products,
            'buy_key': None,
            'sell_key': None
        }

    # استخراج تاریخ و زمان برای کلیدهای Redis
    try:
        date_obj = datetime.datetime.fromisoformat(current_time.replace('Z', '+00:00'))
        date_time_str = date_obj.strftime('%Y_%m_%d_20_00_05')  # ثابت کردن زمان به 20:00:05
        logger.info(f"Using timestamp: {current_time}, formatted as: {date_time_str}")
    except (ValueError, TypeError):
        date_obj = timezone.now()
        date_time_str = date_obj.strftime('%Y_%m_%d_20_00_05')
        logger.warning(f"Invalid timestamp, using current time: {date_time_str}")

    # کلیدهای اصلی برای خرید و فروش
    shop_name = SHOP_ID_TO_NAME.get(result[0].get('shop_id'), 'hanzaei')
    buy_key = f"{shop_name}-buy-{date_time_str}"
    sell_key = f"{shop_name}-sell-{date_time_str}"
    logger.info(f"Generated keys: buy_key={buy_key}, sell_key={sell_key}")

    saved_buy_count = 0
    saved_sell_count = 0

    # ذخیره در Redis با pipeline
    with redis_client.pipeline() as pipe:
        for product in result:
            product_id = product.get('product_id')
            base_price_buy = product.get('base_price_buy')
            base_price_sell = product.get('base_price_sell')
            is_exist = product.get('is_exist')
            api_title = product.get('api_title')

            if not is_exist:
                invalid_products.append({
                    'api_title': api_title,
                    'api_source': product.get('api_source'),
                    'buy_price': base_price_buy,
                    'sell_price': base_price_sell,
                    'reason': 'Product not exist'
                })
                logger.warning(f"Skipping product '{api_title}' - is_exist=False")
                continue

            product_name = PRODUCT_ID_TO_NAME.get(product_id, 'unknown_product')

            if base_price_buy > 0:
                pipe.hset(buy_key, product_name, base_price_buy)
                saved_buy_count += 1
                logger.info(f"Saving buy price for {product_name}: {base_price_buy}")
            else:
                invalid_products.append({
                    'api_title': api_title,
                    'api_source': product.get('api_source'),
                    'buy_price': base_price_buy,
                    'sell_price': base_price_sell,
                    'reason': 'Invalid buy price'
                })
                logger.warning(f"Invalid buy price for {api_title}: {base_price_buy}")

            if base_price_sell > 0:
                pipe.hset(sell_key, product_name, base_price_sell)
                saved_sell_count += 1
                logger.info(f"Saving sell price for {product_name}: {base_price_sell}")
            else:
                invalid_products.append({
                    'api_title': api_title,
                    'api_source': product.get('api_source'),
                    'buy_price': base_price_buy,
                    'sell_price': base_price_sell,
                    'reason': 'Invalid sell price'
                })
                logger.warning(f"Invalid sell price for {api_title}: {base_price_sell}")

        try:
            pipe.execute()
            logger.info(f"Pipeline executed: {saved_buy_count} buy prices, {saved_sell_count} sell prices")
        except redis.RedisError as e:
            logger.error(f"Failed to execute Redis pipeline: {e}")
            return {
                'status': 'error',
                'message': f'Failed to save to Redis: {str(e)}',
                'invalid_products': invalid_products,
                'buy_key': buy_key,
                'sell_key': sell_key
            }

    # تنظیم TTL برای کلیدها
    if saved_buy_count > 0:
        redis_client.expire(buy_key, ttl)
        logger.info(f"Set TTL {ttl} seconds for {buy_key}")
    if saved_sell_count > 0:
        redis_client.expire(sell_key, ttl)
        logger.info(f"Set TTL {ttl} seconds for {sell_key}")

    return {
        'status': 'success' if not invalid_products else 'warning',
        'message': f'Saved {saved_buy_count} buy prices and {saved_sell_count} sell prices in Redis',
        'invalid_products': invalid_products,
        'buy_key': buy_key,
        'sell_key': sell_key
    }

def retrieve_prices_from_block(redis_host='localhost', redis_port=6379, redis_db=0, key=None):
    """
    واکشی تمام قیمت‌ها از یک کلید (خرید یا فروش) در یک بلاک زمانی.
    
    Args:
        redis_host, redis_port, redis_db: تنظیمات اتصال Redis.
        key (str): کلید (مثل hanzaei-buy-2025_09_06_20_00_05).
    
    Returns:
        dict: تمام فیلدهای hash (محصولات و قیمت‌ها).
    """
    redis_client = redis.Redis(host=redis_host, port=redis_port, db=redis_db, decode_responses=True)
    if not key:
        logger.error("No key provided for retrieval")
        return {}
    try:
        prices = redis_client.hgetall(key)
        logger.info(f"Retrieved {len(prices)} prices from {key}")
        return prices
    except redis.RedisError as e:
        logger.error(f"Failed to retrieve prices from {key}: {e}")
        return {}

'''