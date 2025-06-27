# conftest.py
import requests
import os
import pytest
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://dev-mobile.xfit.ru")

HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "okhttp/4.9.1",
    "Platform": "android",
    "App-Version": "3.12.1"
}


@pytest.fixture
def sms_token():
    phone = {
        "phone": {
            "countryCode": "7",
            "number": "9009009094"
        }
    }
    response = requests.post(f"{BASE_URL}/authorization/sendVerificationCode",
                             headers=HEADERS, json=phone)
    assert response.status_code == 200
    return response.json()["result"]["token"]
