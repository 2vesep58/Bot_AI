"""Получение информации из OpenAPI"""

import requests
import yaml

url = "https://lllm-swagger-amvera-services.amvera.io/openapi.yaml"

print("Получение OpenAPI документации...")
print()

try:
    response = requests.get(url, timeout=10, verify=False)
    if response.status_code == 200:
        data = yaml.safe_load(response.text)
        
        print("Servers:")
        for server in data.get('servers', []):
            print(f"  - {server}")
        print()
        
        print("Paths:")
        for path in data.get('paths', {}).keys():
            print(f"  - {path}")
        print()
        
        print("Components/Schemas:")
        for schema in list(data.get('components', {}).get('schemas', {}).keys())[:10]:
            print(f"  - {schema}")
        print()
        
        # Ищем GPT-5 endpoint
        print("Поиск GPT-5 endpoints:")
        for path, methods in data.get('paths', {}).items():
            if 'gpt' in path.lower():
                print(f"  Path: {path}")
                for method, details in methods.items():
                    print(f"    Method: {method.upper()}")
                    if 'operationId' in details:
                        print(f"    OperationId: {details['operationId']}")
        
except Exception as e:
    print(f"Ошибка: {e}")
