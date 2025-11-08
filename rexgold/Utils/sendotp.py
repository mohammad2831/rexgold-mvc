import requests
import json
from decouple import config


def send_otp(pattern, otp, phone):
    url = 'https://edge.ippanel.com/v1/api/send'

    payload = json.dumps({
        "sending_type": "pattern",
        "from_number": "+983000505",
        "code": "69u9der8ondg7dn",
        "recipients": [
            phone,
        ],
        "params": {
            "code":otp
        }
    })
    headers = {
        'Authorization': config('OTPTOKEN2'),
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


def send_buy_or_sell(pattern, phone, factor, status, buy_date, weight, price):

    url = "https://api2.ippanel.com/api/v1/sms/pattern/normal/send"
    payload = json.dumps({
        "code": pattern,
        "sender": "+983000505",
        "recipient": phone,
        "variable": {
            "factor": int(factor),
            "price": int(price),
            "weight": str(weight),
            "buy_date": str(buy_date),
            "status": str(status),

        }
    })
    headers = {
        'apikey': config('OTPTOKEN'),
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.text



def send_active_account(pattern, phone):
    url = "https://api2.ippanel.com/api/v1/sms/pattern/normal/send"

    payload = json.dumps({
        "code": pattern,
        "sender": "+983000505",
        "recipient": phone,
        "variable": {
            "message": 'اکانت'
        }
    })
    headers = {
        'apikey': config('OTPTOKEN'),
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
