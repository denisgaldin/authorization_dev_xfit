import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")

HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "okhttp/4.9.1",
    "Platform": "android",
    "App-Version": "3.12.1"
}


def test_authorize_with_code(sms_token):
    payload = {
        "token": sms_token,
        "verificationCode": "1234"
    }

    response = requests.post(f"{BASE_URL}/authorization/basic",
                             headers=HEADERS, json=payload)

    print("Status:", response.status_code)
    print("Body:", response.text)

    assert response.status_code == 200
    assert "result" in response.json()
