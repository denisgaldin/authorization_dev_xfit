import pytest
import requests
import os
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
    """Получение SMS токена для зарегистрированного пользователя"""
    phone = {
        "phone": {
            "countryCode": "7",
            "number": "9009009094"
        }
    }
    response = requests.post(f"{BASE_URL}/authorization/sendVerificationCode",
                             headers=HEADERS, json=phone)

    if response.status_code != 200:
        pytest.skip(f"❌ Не удалось получить SMS токен. Статус: {response.status_code}, тело: {response.text}")

    return response.json()["result"]["token"]


@pytest.fixture
def unregistered_sms_token():
    """Получение SMS токена на несуществующий номер (ожидается 404 при авторизации)"""
    phone = {
        "phone": {
            "countryCode": "7",
            "number": "9108009091"
        }
    }
    response = requests.post(f"{BASE_URL}/authorization/sendVerificationCode",
                             headers=HEADERS, json=phone)

    if response.status_code != 200:
        pytest.skip(f"❌ Не удалось получить SMS токен для несуществующего пользователя. Статус: {response.status_code}")

    return response.json()["result"]["token"]
