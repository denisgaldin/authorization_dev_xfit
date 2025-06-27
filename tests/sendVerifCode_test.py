import requests
from jsonschema import validate, ValidationError
from dotenv import load_dotenv
import os
import json

load_dotenv()

BASE_URL = os.getenv("BASE_URL")

url = f"{BASE_URL}/authorization/sendVerificationCode"

payload = {
    "phone": {
        "countryCode": "7",
        "number": "9009009094"
    }
}

headers = {
    "Content-Type": "application/json",
    "User-Agent": "okhttp/4.9.1",
    "Platform": "android",
    "App-Version": "3.12.1"
}

schema_path = os.path.join(os.path.dirname(__file__), "../schemas/post_sendVerifCode.json")
with open(schema_path, encoding="utf-8") as f:
    response_schema = json.load(f)


def test_send_verification_code():
    response = requests.post(url, headers=headers, json=payload)

    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")

    assert response.status_code == 200, f"Получаем 200, статус код {response.status_code}"

    try:
        data = response.json()
        validate(instance=data, schema=response_schema)
    except ValidationError as e:
        raise AssertionError(f"Ответ не соответствует схеме — нет токена: {e.message}")
