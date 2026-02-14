"""Скрипт для проверки доступности API Amvera LLM"""

import requests
from dotenv import load_dotenv
import os

# Загружаем переменные окружения
load_dotenv()

token = os.getenv("AMVERA_LLM_TOKEN")

if not token:
    print("Ошибка: AMVERA_LLM_TOKEN не найден в .env файле")
    exit(1)

# Проверяем доступность основных URL
urls = [
    "https://lllm.amvera.io",
    "https://lllm-api.amvera.io",
    "https://api.amvera.io",
    "https://lllm-swagger-amvera-services.amvera.io",
]

headers = {
    "Authorization": f"Bearer {token}"
}

print("Проверка доступности API Amvera LLM...")
print()

for url in urls:
    print(f"GET {url}")
    try:
        response = requests.get(url, headers=headers, timeout=5, verify=False)
        print(f"  Статус: {response.status_code}")
        print(f"  Ответ: {response.text[:300]}")
    except Exception as e:
        print(f"  Ошибка: {e}")
    print()

# Попробуем OPTIONS запрос
print("\n" + "="*50)
print("Попытка OPTIONS запроса к https://lllm.amvera.io")
print("="*50)
try:
    response = requests.options("https://lllm.amvera.io", headers=headers, timeout=5, verify=False)
    print(f"Статус: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
except Exception as e:
    print(f"Ошибка: {e}")
