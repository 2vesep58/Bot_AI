# Руководство по использованию Telegram бота с Amvera LLM

## Быстрый старт

### 1. Установка зависимостей

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Настройка переменных окружения

Убедитесь, что в файле `.env` указаны следующие переменные:

```env
BOT_TOKEN=ваш_токен_бота_telegram
AMVERA_LLM_TOKEN=ваш_токен_amvera_llm
CONTEXT7_API_KEY=ваш_ключ_context7
```

### 3. Запуск бота

```bash
python -m src.bot.main
```

## Использование команд

### Команда /chatgpt

Активирует режим взаимодействия с ИИ Amvera (модель gpt-5).

**Пример:**
```
Пользователь: /chatgpt
Бот: Отправьте мне сообщение, и я отвечу с помощью ИИ. Чтобы выйти из режима ИИ, отправьте /stop.

Пользователь: Что такое машинное обучение?
Бот: ⏳ Обрабатываю ваш запрос...
Бот: Машинное обучение - это раздел искусственного интеллекта, который позволяет компьютерам учиться на основе данных...
```

### Команда /stop

Деактивирует режим взаимодействия с ИИ и возвращает бота в режим эхо.

**Пример:**
```
Пользователь: /stop
Бот: Вы вышли из режима общения с ИИ. Теперь я буду работать как эхо-бот.
```

### Команда /start

Приветственное сообщение при запуске бота.

**Пример:**
```
Пользователь: /start
Бот: Привет! Я эхо-бот. Отправь мне любое сообщение, и я его повторю.
```

### Команда /help

Справка по доступным командам.

## Архитектура

### Сервис AmveraLLMService

Сервис `AmveraLLMService` отвечает за взаимодействие с API Amvera LLM.

**Основные методы:**
- `get_response(user_message: str) -> Optional[str]` - получить ответ от LLM

**Пример использования:**
```python
from src.bot.config import Config
from src.bot.services.amvera_llm import AmveraLLMService

config = Config()
service = AmveraLLMService(config)
response = await service.get_response("Привет, ИИ!")
print(response)
```

### Роутер chatgpt

Роутер `chatgpt_router` обрабатывает команды `/chatgpt` и `/stop`, а также сообщения пользователя в режиме ИИ.

**Основные обработчики:**
- `chatgpt_start_handler` - активирует режим ИИ
- `chatgpt_stop_handler` - деактивирует режим ИИ
- `chatgpt_handler` - обрабатывает сообщения в режиме ИИ

## Тестирование

### Запуск всех тестов

```bash
pytest
```

### Запуск тестов с покрытием

```bash
pytest --cov=src
```

### Запуск конкретного теста

```bash
pytest tests/test_chatgpt_router.py::test_chatgpt_start_handler
```

## Обработка ошибок

Сервис `AmveraLLMService` обрабатывает следующие типы ошибок:

1. **Ошибки HTTP** - если API Amvera вернул ошибку (статус != 200)
2. **Timeout** - если запрос превысил время ожидания (30 секунд)
3. **Исключения** - любые другие ошибки при обращении к API

В случае ошибки сервис возвращает `None`, и бот отправляет пользователю сообщение об ошибке.

## Логирование

Все события логируются в файл `logs/bot.log`. Уровень логирования можно настроить в файле `src/bot/utils/logging.py`.

## Безопасность

**Важно:** В текущей реализации отключена проверка SSL-сертификата для тестирования. Для продакшена необходимо включить проверку SSL-сертификата, удалив следующие строки из `src/bot/services/amvera_llm.py`:

```python
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE
```

И использовать стандартный SSL контекст:

```python
async with session.post(
    self.AMVERA_LLM_URL,
    json=payload,
    headers=headers,
    timeout=aiohttp.ClientTimeout(total=30)
) as response:
```

## Документация API Amvera

- **Swagger**: https://lllm-swagger-amvera-services.amvera.io/openapi.yaml
- **Документация**: https://lllm-swagger-amvera-services.amvera.io/#/GPT/post_models_gpt
