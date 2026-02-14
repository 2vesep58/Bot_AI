"""Скрипт для получения информации из Swagger"""

import requests
from dotenv import load_dotenv
import os
import json

# Загружаем переменные окружения
load_dotenv()

token = os.getenv("AMVERA_LLM_TOKEN")

# Пытаемся получить swagger.json
urls = [
    "https://lllm-swagger-amvera-services.amvera.io/swagger.json",
    "https://lllm-swagger-amvera-services.amvera.io/openapi.json",
    "https://lllm-swagger-amvera-services.amvera.io/openapi.yaml",
    "https://lllm-swagger-amvera-services.amvera.io/v1/swagger.json",
]

print("Поиск Swagger/OpenAPI документации...")
print()

for url in urls:
    print(f"Попытка: {url}")
    try:
        response = requests.get(url, timeout=5, verify=False)
        print(f"  Статус: {response.status_code}")
        if response.status_code == 200:
            print(f"  ✓ НАЙДЕНО!")
            if url.endswith('.json'):
                data = response.json()
                print(f"  Servers: {data.get('servers', 'N/A')}")
                print(f"  BasePath: {data.get('basePath', 'N/A')}")
                print(f"  Paths: {list(data.get('paths', {}).keys())[:5]}")
            else:
                print(f"  Ответ: {response.text[:500]}")
        print()
    except Exception as e:
        print(f"  Ошибка: {e}")
        print()
