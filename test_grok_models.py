"""Тест разных моделей Grok"""

import requests
from dotenv import load_dotenv
import os

# Загружаем переменные окружения
load_dotenv()

token = os.getenv("AMVERA_LLM_TOKEN")

if not token:
    print("Ошибка: AMVERA_LLM_TOKEN не найден в .env файле")
    exit(1)

url = "https://api.x.ai/v1/chat/completions"

# Разные названия моделей Grok
models = [
    "grok-2",
    "grok-2-1212",
    "grok-1",
    "grok",
    "grok-vision-beta",
]

payload_template = {
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

print("Тестирование разных моделей Grok...")
print()

for model in models:
    payload = {**payload_template, "model": model}
    print(f"Модель: {model}")
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10, verify=True)
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
