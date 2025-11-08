import requests
from rest_framework import status

def fetch_product_prices():

    # Your request details
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


    cookies = {"access_token_web":"eyJpdiI6Imt3aE5OMVQxSDFmRG12SEQvbDVPWUE9PSIsInZhbHVlIjoiOUVNMmNWb0xZQmgwQ1VNcnBLMS9TZmFlYzZnejBnbk5CS0pPa0NsMEFyeG9iMTdtTGFIS2dRQXovbXdBcjlkNldEUTNicGpBYVFrRjZWQ1dMVkdPT1lJZ0pOcFB2OWhJMnlVT1BKTDlBUTR4cDNQdFJEeE5CNnpucGx5SDZPQ2ZZVk5mNW5CaW9YSDhZWCsyQzYxeWEzU3RqUGZlbXlNRHJGMnlVNUxubng1YzhlbmFvWWZIS1poZDVkc0tML1UxcWp0ZERlMHVBeEIvOUQvY0FoRlpoRmdjVnFndFZNd2tzaFF0Um81L1lTcUViUm0vdnJON0RTT3B1bVB6TlA0QXBQRzNzcUZJYzJnVmZRMHhIV2ZtRXhzdUR1ajl1dG8zSFNwQ0dnNmlaWkNiVGU4UStsOWxmTGpHWUo1YVBHMksiLCJtYWMiOiJmYzI3MjllYTJhZDQ2YjYxNjhjOTNjMmMyODYyNjU4MjZiZTRkNTY5NTQwZDg2MWQ0OGViNDQ1ZTQwYTVkYjRiIiwidGFnIjoiIn0%3D"}
   # Send the request
    try:
        response = requests.get(url, headers=headers, cookies=cookies)
    except requests.exceptions.RequestException as e:
        # Handle network errors (e.g., DNS failure, refused connection, etc).
        return {
            'status': 'error',
            'message': f'A network error occurred: {e}'
        }, status.HTTP_503_SERVICE_UNAVAILABLE

    # 1. Handle 401 Unauthorized Error
    if response.status_code == status.HTTP_401_UNAUTHORIZED:
        return {
            'status': 'error',
            'message': 'مشکلی پیش امده است'
        }, status.HTTP_401_UNAUTHORIZED

    # Handle successful request
    if response.status_code == status.HTTP_200_OK:
        data = response.json()
        categories = data.get('data', [])

        # 2. Handle empty data list
        if not categories:
            return {
                'status': 'error',
                'message': 'فروشگاه در دسترس نیست'
            }, status.HTTP_404_NOT_FOUND
        
        result = []
        invalid_prices = []

        for category in categories:
            category_title = category.get('title', 'Unknown Category')
            products = []
            for product in category.get('products', []):
                buy_price = product.get('buy_price', 0)
                sell_price = product.get('sell_price', 0)

                if buy_price == -1 or sell_price == -1:
                    invalid_prices.append({
                        'category': category_title,
                        'product': product.get('title', 'Unknown Product'),
                        'buy_price': buy_price,
                        'sell_price': sell_price
                    })

                products.append({
                    'title': product.get('title', 'Unknown Product'),
                    'buy_price': buy_price,
                    'sell_price': sell_price
                })
            result.append({
                'category': category_title,
                'products': products
            })

        if invalid_prices:
            return {
                'status': 'warning',
                'message': 'Some products have invalid prices (-1).',
                'invalid_products': invalid_prices,
                'data': result
            }, status.HTTP_206_PARTIAL_CONTENT
        
        return {'status': 'success', 'data': result}, status.HTTP_200_OK

    # Handle all other non-successful status codes
    else:
        return {
            'status': 'error',
            'message': f'Failed to get data. Status code: {response.status_code}',
            'response_text': response.text
        }, status.HTTP_500_INTERNAL_SERVER_ERROR

print(fetch_product_prices())