"""Тест разных префиксов пути"""

import requests
from dotenv import load_dotenv
import os

# Загружаем переменные окружения
load_dotenv()

token = os.getenv("AMVERA_LLM_TOKEN")

if not token:
    print("Ошибка: AMVERA_LLM_TOKEN не найден в .env файле")
    exit(1)

base_url = "https://kong-proxy.yc.amvera.ru"

# Разные варианты путей
paths = [
    "/models/gpt",
    "/api/models/gpt",
    "/v1/models/gpt",
    "/llm/models/gpt",
    "/lllm/models/gpt",
    "/inference/models/gpt",
    "/chat/models/gpt",
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

print("Тестирование разных префиксов пути...")
print()

for path in paths:
    url = f"{base_url}{path}"
    print(f"Тестирование: {url}")
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
        print(f"  Статус: {response.status_code}")
        if response.status_code == 200:
            print(f"  ✓ УСПЕХ!")
            print(f"  Ответ: {response.text[:300]}")
        else:
            print(f"  Ответ: {response.text[:150]}")
        print()
    except Exception as e:
        print(f"  Ошибка: {e}")
        print()
