# API Reference

## AmveraLLMService

Сервис для работы с Amvera LLM API.

### Класс: AmveraLLMService

```python
from src.bot.services.amvera_llm import AmveraLLMService
from src.bot.config import Config

config = Config()
service = AmveraLLMService(config)
```

### Методы

#### __init__(config: Config)

Инициализация сервиса.

**Параметры:**
- `config` (Config) - конфигурация бота

**Пример:**
```python
service = AmveraLLMService(config)
```

#### get_response(user_message: str) -> Optional[str]

Получить ответ от Amvera LLM.

**Параметры:**
- `user_message` (str) - сообщение пользователя

**Возвращает:**
- `str` - ответ от LLM
- `None` - в случае ошибки

**Пример:**
```python
response = await service.get_response("Что такое Python?")
if response:
    print(response)
else:
    print("Ошибка при обращении к LLM")
```

### Атрибуты

#### AMVERA_LLM_URL

URL API Amvera LLM.

```python
AMVERA_LLM_URL = "https://lllm.amvera.io/v1/chat/completions"
```

#### MODEL

Модель LLM.

```python
MODEL = "gpt-5"
```

### Обработка ошибок

Сервис обрабатывает следующие типы ошибок:

1. **HTTP ошибки** - если API вернул статус != 200
2. **Timeout** - если запрос превысил 30 секунд
3. **Исключения** - любые другие ошибки при обращении к API

В случае ошибки сервис возвращает `None`.

**Пример:**
```python
response = await service.get_response("Привет")
if response is None:
    # Обработка ошибки
    print("Ошибка при обращении к LLM")
```

### Логирование

Все операции логируются в файл `logs/bot.log`.

**Примеры логов:**
```
INFO: Отправка запроса к Amvera LLM
INFO: Статус ответа от Amvera LLM: 200
INFO: Успешный ответ от Amvera LLM
ERROR: Ошибка от Amvera LLM: 500 - Internal Server Error
ERROR: Timeout при обращении к Amvera LLM
ERROR: Исключение при обращении к Amvera LLM: Network error
```

## Routers

### chatgpt_router

Роутер для обработки команд `/chatgpt` и `/stop`.

#### Команда: /chatgpt

Активирует режим ИИ.

**Обработчик:** `chatgpt_start_handler`

**Ответ:**
```
Отправьте мне сообщение, и я отвечу с помощью ИИ. Чтобы выйти из режима ИИ, отправьте /stop.
```

#### Команда: /stop

Деактивирует режим ИИ.

**Обработчик:** `chatgpt_stop_handler`

**Ответ:**
```
Вы вышли из режима общения с ИИ. Теперь я буду работать как эхо-бот.
```

#### Обработка текстовых сообщений

Если пользователь находится в режиме ИИ, сообщение отправляется в AmveraLLMService.

**Обработчик:** `chatgpt_handler`

**Параметры:**
- `message` (Message) - сообщение от пользователя
- `config` (Config) - конфигурация бота

**Ответ:**
```
⏳ Обрабатываю ваш запрос...
[Ответ от LLM]
```

или в случае ошибки:

```
Произошла ошибка при обращении к ИИ. Пожалуйста, попробуйте позже.
```

### Состояние пользователя

Состояние активации режима ИИ хранится в словаре `chatgpt_active`.

```python
chatgpt_active = {
    user_id: True,  # Пользователь в режиме ИИ
    ...
}
```

## Config

### Класс: Config

Конфигурация приложения.

```python
from src.bot.config import Config

config = Config()
```

### Атрибуты

#### bot_token

Токен Telegram бота.

```python
bot_token: SecretStr
```

#### amvera_llm_token

Токен Amvera LLM.

```python
amvera_llm_token: SecretStr
```

#### context7_api_key

Ключ Context7.

```python
context7_api_key: SecretStr
```

### Свойства

#### bot

Конфигурация бота.

```python
bot_config = config.bot
```

#### amvera

Конфигурация Amvera LLM.

```python
amvera_config = config.amvera
```

#### mcp

Конфигурация MCP серверов.

```python
mcp_config = config.mcp
```

### Функция: load_config()

Загрузить конфигурацию из переменных окружения.

```python
from src.bot.config import load_config

config = load_config()
```

## Переменные окружения

### BOT_TOKEN

Токен Telegram бота.

```env
BOT_TOKEN=123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefgh
```

### AMVERA_LLM_TOKEN

Токен Amvera LLM.

```env
AMVERA_LLM_TOKEN=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
```

### CONTEXT7_API_KEY

Ключ Context7.

```env
CONTEXT7_API_KEY=ctx7sk-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

## Примеры использования

### Пример 1: Получить ответ от LLM

```python
import asyncio
from src.bot.config import Config
from src.bot.services.amvera_llm import AmveraLLMService

async def main():
    config = Config()
    service = AmveraLLMService(config)
    
    response = await service.get_response("Что такое Python?")
    if response:
        print(response)
    else:
        print("Ошибка при обращении к LLM")

asyncio.run(main())
```

### Пример 2: Использование в роутере

```python
from aiogram import Router, F
from aiogram.types import Message
from src.bot.config import Config
from src.bot.services.amvera_llm import AmveraLLMService

router = Router()

@router.message(F.text)
async def handler(message: Message, config: Config):
    service = AmveraLLMService(config)
    response = await service.get_response(message.text)
    
    if response:
        await message.answer(response)
    else:
        await message.answer("Ошибка при обращении к ИИ")
```

### Пример 3: Обработка ошибок

```python
response = await service.get_response("Привет")

if response is None:
    # Обработка ошибки
    logger.error("Ошибка при обращении к LLM")
    await message.answer("Произошла ошибка. Пожалуйста, попробуйте позже.")
else:
    # Успешный ответ
    await message.answer(response)
```

## Документация Amvera LLM

- **Swagger:** https://lllm-swagger-amvera-services.amvera.io/openapi.yaml
- **Документация:** https://lllm-swagger-amvera-services.amvera.io/#/GPT/post_models_gpt

## Версии

- **Python:** 3.11+
- **aiogram:** 3.3.0
- **aiohttp:** 3.9.5
- **Amvera LLM Model:** gpt-5
