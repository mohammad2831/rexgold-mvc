import requests
import json

url = "https://api.khakpourgold.com/order"
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:143.0) Gecko/20100101 Firefox/143.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Cache-Control": "no-cache",
    "X-Verify": "YOUR_VALID_X_VERIFY_CODE",
    "Content-Type": "application/json",
    "Authorization": "Bearer YOUR_VALID_BEARER_TOKEN",
    "Origin": "https://panel.khakpourgold.com",
    "Referer": "https://panel.khakpourgold.com/",
    "Cookie": "access_token_web=eyJpdiI6IjNHSS9OTmlJK3B5SkJ5Q0JKVnFCa0E9PSIsInZhbHVlIjoiT01FdDBTNW00SHQ3OXU1REUxSVBVZHNhSTcyTElHTXY5R3Azc3FnM0RNeWJmYkRHVitxMEhMYUJpYllxT2EwVVdaNFVFOTZtTGRSaXA0ZWVzZkdtN21GaDNGTWxiVG1CMmhyL2NwTUhrT0JmL3RmQ05zQTZnV2oxLzdSQ2FobFdKOElUY0ZCV25WbjZuQ0NrTFYySENWWlhjOCtOTGVybTRpSyt4RElKTEVGbGlJQWM3ZXd0VGIvb3lKV29VWVJjUFJPaWFncjdtOGlCNTFzY3hUeS91Yjh0OURaN1MvN2xWTjdJWXQ3MTU2Ykh1S09oczlXYmVDdkNSWjMvbGlkS0FRVXU5NEdES0NkOFJ4ald4QlQwOVEyckJCTC9aSmRZNGFUcXRLcExoMGJ6WUI0aG81YUhWYVdJZ1FWbk90dnMiLCJtYWMiOiJiYjdmY2QzNThlN2UzM2I5ZDViYjVjNDJmNTYwOWZlOTFhMGI3ZmU2ZWFiYjJkMDA2OGVkN2UzZWZkOGYwYmE4IiwidGFnIjoiIn0%3D",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "Priority": "u=0"
}
data = {
  "side": "buy",
  "type": "market_price",
  "price": "40760000",
  "quantity": 0.01,
  "product_id": "aa96c755-c862-4464-bf80-04654b71cd58",
  "note": "",
  "total_price": 94100,
  "input": "unit"
}

# اگر از پروکسی استفاده می‌کنی
proxies = {
    "https": "http://127.0.0.1:10808"
}

response = requests.post(url, headers=headers, json=data, proxies=proxies)
#response = requests.get("https://api.khakpourgold.com/products", headers=headers, proxies=proxies)
print(response.json())
print("Status Code:", response.status_code)
print("Response:", response.text)









#payload درخواست های ارسالی
'''{"side":"buy","type":"market_price","price":"40760000","quantity":0.01,"product_id":"aa96c755-c862-4464-bf80-04654b71cd58","note":"","total_price":94100,"input":"unit"}

	
input	"unit"
note	""
price	"40760000"
product_id	"aa96c755-c862-4464-bf80-04654b71cd58"
quantity	0.01
side	"buy"
total_price	94100
type	"market_price"'''



















