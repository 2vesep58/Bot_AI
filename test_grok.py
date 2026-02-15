"""Тест API Grok"""

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

payload = {
    "model": "grok-2",
    "messages": [
        {
            "role": "user",
            "content": "Hello! What is 2+2?"
        }
    ]
}

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": f"Bearer {token}"
}

print("Тестирование API Grok...")
print(f"URL: {url}")
print(f"Токен: {token[:20]}...")
print()

try:
    response = requests.post(url, json=payload, headers=headers, timeout=30, verify=True)
    print(f"Статус: {response.status_code}")
    print(f"Ответ:")
    print(response.text)
    
    if response.status_code == 200:
        print("\n✓ УСПЕХ! API Grok работает!")
    else:
        print(f"\n✗ Ошибка {response.status_code}")
except Exception as e:
    print(f"Ошибка: {e}")
