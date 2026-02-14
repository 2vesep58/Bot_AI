"""Скрипт для тестирования API Amvera LLM"""

import requests
import json
from dotenv import load_dotenv
import os

# Загружаем переменные окружения
load_dotenv()

token = os.getenv("AMVERA_LLM_TOKEN")

if not token:
    print("Ошибка: AMVERA_LLM_TOKEN не найден в .env файле")
    exit(1)

# Список URL для тестирования
urls = [
    "https://lllm-swagger-amvera-services.amvera.io/models/gpt-5",
    "https://lllm-swagger-amvera-services.amvera.io/v1/models/gpt-5",
    "https://lllm-swagger-amvera-services.amvera.io/api/models/gpt-5",
    "https://lllm-swagger-amvera-services.amvera.io/v1/chat/completions",
]

payload = {
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
    "Authorization": f"Bearer {token}"
}

print("Тестирование API Amvera LLM...")
print(f"Токен: {token[:20]}...")
print()

for url in urls:
    print(f"Тестирование: {url}")
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
        print(f"  Статус: {response.status_code}")
        if response.status_code == 200:
            print(f"  ✓ УСПЕХ!")
            print(f"  Ответ: {response.text[:500]}")
        else:
            print(f"  Ответ: {response.text[:200]}")
        print()
    except Exception as e:
        print(f"  Ошибка: {e}")
        print()


