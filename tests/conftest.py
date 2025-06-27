# conftest.py
import pytest
import requests
import os
import random
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "okhttp/4.9.1",
    "Platform": "android",
    "App-Version": "3.12.1"
}


def generate_random_phone_number(prefix="9009009"):
    """Генерирует уникальный номер телефона, чтобы избежать дубликатов"""
    suffix = str(random.randint(100, 999))
    return prefix + suffix


@pytest.fixture
def sms_token():
    """Получение SMS токена на рандомный номер (может быть не зарегистрированным)"""
    phone_number = generate_random_phone_number()
    payload = {
        "phone": {
            "countryCode": "7",
            "number": phone_number
        }
    }

    response = requests.post(
        f"{BASE_URL}/authorization/sendVerificationCode",
        headers=HEADERS,
        json=payload
    )

    if response.status_code != 200:
        pytest.skip(f"❌ Не удалось получить SMS токен. Статус: {response.status_code}, тело: {response.text}")

    return response.json().get("result", {}).get("token")


@pytest.fixture
def unregistered_sms_token():
    """Получение SMS токена на заведомо несуществующий номер"""
    phone_number = "9108009" + str(random.randint(100, 999))
    payload = {
        "phone": {
            "countryCode": "7",
            "number": phone_number
        }
    }

    response = requests.post(
        f"{BASE_URL}/authorization/sendVerificationCode",
        headers=HEADERS,
        json=payload
    )

    if response.status_code != 200:
        pytest.skip(
            f"❌ Не удалось получить SMS токен для незарегистрированного номера. Статус: {response.status_code}, тело: {response.text}")

    return response.json().get("result", {}).get("token")


@pytest.fixture
def known_user_token():
    """Получение SMS токена для зарегистрированного пользователя"""
    payload = {
        "phone": {
            "countryCode": "7",
            "number": "9009009094"  # ⚠️ должен быть зарегистрирован
        }
    }

    response = requests.post(
        f"{BASE_URL}/authorization/sendVerificationCode",
        headers=HEADERS,
        json=payload
    )

    if response.status_code != 200:
        pytest.skip(
            f"❌ Не удалось получить токен для зарегистрированного пользователя. Статус: {response.status_code}, тело: {response.text}"
        )

    return response.json().get("result", {}).get("token")
