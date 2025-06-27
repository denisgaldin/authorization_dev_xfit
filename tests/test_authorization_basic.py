import os
import json
import pytest
import requests
from dotenv import load_dotenv
from jsonschema import validate, ValidationError

load_dotenv()

BASE_URL = os.getenv("BASE_URL")

HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "okhttp/4.9.1",
    "Platform": "android",
    "App-Version": "3.12.1"
}

PHONE_PAYLOAD = {
    "phone": {
        "countryCode": "7",
        "number": "9009009094"  # Зарегистрированный пользователь
    }
}


def check_error_response(data):
    assert "error" in data, "Ожидается поле 'error'"
    error = data["error"]
    assert error["type"] == "VERIFICATION_CODE_ALREADY_SEND_PORTAL"
    assert isinstance(error["message"], str)
    assert isinstance(error["debugMessage"], str)


def check_user_not_found(data):
    assert "error" in data
    error = data["error"]
    assert error["type"] == "USER_NOT_FOUND"
    assert isinstance(error["message"], str)
    assert isinstance(error["debugMessage"], str)


@pytest.mark.order(1)
def test_send_verification_code_twice():
    """Негативный тест: повторная отправка SMS-кода"""
    first_response = requests.post(
        f"{BASE_URL}/authorization/sendVerificationCode",
        headers=HEADERS,
        json=PHONE_PAYLOAD
    )
    assert first_response.status_code == 200, (
        f"Первый запрос должен вернуть 200, но был {first_response.status_code}"
    )

    second_response = requests.post(
        f"{BASE_URL}/authorization/sendVerificationCode",
        headers=HEADERS,
        json=PHONE_PAYLOAD
    )
    assert second_response.status_code == 403, (
        f"Повторный запрос должен вернуть 403, но был {second_response.status_code}"
    )
    check_error_response(second_response.json())


@pytest.mark.order(2)
def test_authorization_schema_validation(known_user_token):
    """Позитивный тест: валидация схемы JSON-ответа /authorization/basic"""
    payload = {
        "token": known_user_token,
        "verificationCode": "1234"  # актуальный код, предварительно введённый
    }

    response = requests.post(
        f"{BASE_URL}/authorization/basic",
        headers=HEADERS,
        json=payload
    )
    assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}"

    data = response.json()
    schema_path = os.path.join(os.path.dirname(__file__), "../schemas/post_authorization_basic.json")
    with open(schema_path, encoding="utf-8") as f:
        schema = json.load(f)

    try:
        validate(instance=data, schema=schema)
    except ValidationError as e:
        pytest.fail(f"Ответ не соответствует JSON-схеме: {e.message}")


@pytest.mark.order(3)
def test_authorize_user_not_found(unregistered_sms_token):
    """Негативный тест: пользователь не найден (незарегистрированный номер)"""
    payload = {
        "token": unregistered_sms_token,
        "verificationCode": "1234"
    }
    response = requests.post(
        f"{BASE_URL}/authorization/basic",
        headers=HEADERS,
        json=payload
    )
    assert response.status_code == 404, f"Ожидали 404, получили {response.status_code}"
    check_user_not_found(response.json())


@pytest.mark.order(4)
def test_authorize_with_invalid_code(known_user_token):
    """Негативный тест: неверный код подтверждения"""
    payload = {
        "token": known_user_token,
        "verificationCode": "0000"  # гарантированно неверный
    }

    response = requests.post(
        f"{BASE_URL}/authorization/basic",
        headers=HEADERS,
        json=payload
    )

    assert response.status_code == 403, f"Ожидали 403, получили {response.status_code}"

    data = response.json()
    assert "error" in data, "Ожидалось поле 'error'"
    assert data["error"]["type"] == "VERIFICATION_CODE_FAILED", "Ожидали тип ошибки VERIFICATION_CODE_FAILED"
    assert isinstance(data["error"]["message"], str)
    assert isinstance(data["error"]["debugMessage"], str)
