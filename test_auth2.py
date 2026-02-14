"""Тест авторизации с правильным URL"""

import requests
from dotenv import load_dotenv
import os

# Загружаем переменные окружения
load_dotenv()

token = os.getenv("AMVERA_LLM_TOKEN")

if not token:
    print("Ошибка: AMVERA_LLM_TOKEN не найден в .env файле")
    exit(1)

url = "https://kong-proxy.yc.amvera.ru/api/v1/models/gpt"

payload = {
    "model": "gpt-5",
    "messages": [
        {
            "role": "user",
            "content": "Hello"
        }
    ]
}

# Разные варианты заголовков
auth_variants = [
    ("X-Auth-Token", token),
    ("Authorization", f"Bearer {token}"),
    ("Authorization", token),
    ("X-API-Key", token),
]

print("Тестирование авторизации...")
print()

for header_name, header_value in auth_variants:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        header_name: header_value
    }
    
    print(f"Заголовок: {header_name}")
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
        print(f"  Статус: {response.status_code}")
        if response.status_code == 200:
            print(f"  ✓ УСПЕХ!")
            print(f"  Ответ: {response.text[:300]}")
        else:
            print(f"  Ответ: {response.text[:200]}")
        print()
    except Exception as e:
        print(f"  Ошибка: {e}")
        print()
