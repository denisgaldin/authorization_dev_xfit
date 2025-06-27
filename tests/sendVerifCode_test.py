import requests
from jsonschema import validate, ValidationError
from dotenv import load_dotenv
import os
import json
import random

load_dotenv()
BASE_URL = os.getenv("BASE_URL")


def generate_unique_phone():
    return {
        "countryCode": "7",
        "number": f"900{random.randint(1000000, 9999999)}"
    }


url = f"{BASE_URL}/authorization/sendVerificationCode"

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
    payload = {"phone": generate_unique_phone()}

    response = requests.post(url, headers=headers, json=payload)

    print(f"📡 Status Code: {response.status_code}")
    print(f"📨 Response Body: {response.text}")

    assert response.status_code == 200, f"❌ Ожидали 200, получили {response.status_code}"

    try:
        data = response.json()
        validate(instance=data, schema=response_schema)
        print("✅ Ответ соответствует JSON-схеме")
    except ValidationError as e:
        raise AssertionError(f"❌ Ответ не соответствует схеме: {e.message}")
    except json.JSONDecodeError:
        raise AssertionError("❌ Ответ не является валидным JSON")
