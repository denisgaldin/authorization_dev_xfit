import requests
from jsonschema import validate
from dotenv import load_dotenv
import os

load_dotenv()

# Получаем базовый URL из .env
base_url = os.getenv("BASE_URL")

url = f"{base_url}/authorization/sendVerificationCode"

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

response_schema = {
    "type": "object",
    "properties": {
        "result": {
            "type": "object",
            "properties": {
                "token": {"type": "string"}
            },
            "required": ["token"]
        }
    },
    "required": ["result"]
}


def test_send_verification_code():
    response = requests.post(url, headers=headers, json=payload)

    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")

    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"

    data = response.json()
    validate(instance=data, schema=response_schema)
