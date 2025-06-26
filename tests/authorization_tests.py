import json

import requests
from jsonschema import validate

from schemas import post_sendVerifCode

url = "https://dev-mobile.xfit.ru/authorization/sendVerificationCode"

payload = {"phone": {"countryCode": "7", "number": "9009009094"}}

response = requests.request("POST", url, data=payload)

print(response.text)


def test():
    response = requests.request("https://dev-mobile.xfit.ru/authorization/sendVerificationCode", url,
                                data={"phone": {"countryCode": "7", "number": "9009009094"}})
    assert status_code == 200
    with open('post_sendVerifCode.json') as file:
        validate(body, schema=file.read())
