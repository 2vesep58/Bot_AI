"""Финальный тест API Groq"""

import requests
from dotenv import load_dotenv
import os

# Загружаем переменные окружения
load_dotenv()

token = os.getenv("GROQ_API_KEY")

if not token:
    print("Ошибка: GROQ_API_KEY не найден в .env файле")
    exit(1)

url = "https://api.groq.com/openai/v1/chat/completions"

payload = {
    "model": "mixtral-8x7b-32768",
    "messages": [
        {
            "role": "user",
            "content": "Hello! What is 2+2?"
        }
    ],
    "temperature": 0.7,
    "max_tokens": 1024
}

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": f"Bearer {token}"
}

print("Тестирование API Groq...")
print(f"URL: {url}")
print(f"Токен: {token[:20]}...")
print()

try:
    response = requests.post(url, json=payload, headers=headers, timeout=30, verify=True)
    print(f"Статус: {response.status_code}")
    print(f"Ответ:")
    print(response.text)
    
    if response.status_code == 200:
        print("\n✓ УСПЕХ! API Groq работает!")
    else:
        print(f"\n✗ Ошибка {response.status_code}")
except Exception as e:
    print(f"Ошибка: {e}")
