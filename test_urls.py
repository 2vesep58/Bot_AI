"""Тест разных базовых URL"""

import requests
from dotenv import load_dotenv
import os

# Загружаем переменные окружения
load_dotenv()

token = os.getenv("AMVERA_LLM_TOKEN")

if not token:
    print("Ошибка: AMVERA_LLM_TOKEN не найден в .env файле")
    exit(1)

# Список базовых URL для тестирования
base_urls = [
    "https://kong-proxy.yc.amvera.ru",
    "https://lllm.amvera.io",
    "https://lllm-api.amvera.io",
    "https://api.amvera.io",
    "https://lllm-swagger-amvera-services.amvera.io",
]

payload = {
    "model": "gpt-5",
    "messages": [
        {
            "role": "user",
            "content": "Hello"
        }
    ]
}

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "X-Auth-Token": token
}

print("Тестирование разных базовых URL...")
print()

for base_url in base_urls:
    url = f"{base_url}/models/gpt"
    print(f"Тестирование: {url}")
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
