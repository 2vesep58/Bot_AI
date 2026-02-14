# Архитектура проекта

## Общая структура

```
telegram-bot/
├── src/
│   └── bot/
│       ├── __init__.py
│       ├── __main__.py
│       ├── main.py                 # Точка входа
│       ├── config.py               # Конфигурация
│       ├── routers/                # Обработчики команд
│       │   ├── __init__.py
│       │   ├── start.py            # Команда /start
│       │   ├── help.py             # Команда /help
│       │   ├── chatgpt.py          # Команда /chatgpt и /stop
│       │   └── echo.py             # Эхо-функциональность
│       ├── services/               # Бизнес-логика
│       │   ├── __init__.py
│       │   ├── text.py             # Обработка текста
│       │   └── amvera_llm.py       # Интеграция с Amvera LLM
│       ├── keyboards/              # Клавиатуры
│       │   └── __init__.py
│       ├── utils/                  # Утилиты
│       │   ├── __init__.py
│       │   └── logging.py          # Логирование
│       └── mcp_config.json         # Конфигурация MCP
├── tests/                          # Тесты
│   ├── test_chatgpt_router.py
│   ├── test_amvera_llm_service.py
│   └── ...
├── logs/                           # Логи
│   └── bot.log
├── .env                            # Переменные окружения
├── .env.example                    # Пример конфигурации
├── requirements.txt                # Зависимости
├── README.md                       # Основная документация
├── USAGE.md                        # Руководство по использованию
├── INTEGRATION.md                  # Описание интеграции
├── QUICKSTART.md                   # Быстрый старт
├── CHANGES.md                      # Список изменений
└── ARCHITECTURE.md                 # Этот файл
```

## Компоненты

### 1. Config (src/bot/config.py)

Управление конфигурацией приложения.

**Классы:**
- `BotConfig` - конфигурация бота
- `AmveraConfig` - конфигурация Amvera LLM
- `MCPConfig` - конфигурация MCP серверов
- `Config` - главная конфигурация

**Переменные окружения:**
- `BOT_TOKEN` - токен Telegram бота
- `AMVERA_LLM_TOKEN` - токен Amvera LLM
- `CONTEXT7_API_KEY` - ключ Context7

### 2. Routers (src/bot/routers/)

Обработчики команд и сообщений.

#### chatgpt.py
- `/chatgpt` - активирует режим ИИ
- `/stop` - деактивирует режим ИИ
- Обработка текстовых сообщений в режиме ИИ

#### start.py
- `/start` - приветственное сообщение

#### help.py
- `/help` - справка по командам

#### echo.py
- Эхо-функциональность для всех остальных сообщений

### 3. Services (src/bot/services/)

Бизнес-логика приложения.

#### amvera_llm.py
Сервис для работы с Amvera LLM.

**Класс:** `AmveraLLMService`

**Методы:**
- `__init__(config: Config)` - инициализация
- `get_response(user_message: str) -> Optional[str]` - получить ответ от LLM

**Особенности:**
- Обработка ошибок (HTTP, timeout, исключения)
- Логирование всех операций
- Использование aiohttp для асинхронных запросов

#### text.py
Обработка текста.

**Функции:**
- `process_text(text: str) -> str` - обработка текста

### 4. Utils (src/bot/utils/)

Утилиты приложения.

#### logging.py
Настройка логирования.

**Функции:**
- `setup_logging(config: Config)` - настройка логирования

### 5. Main (src/bot/main.py)

Точка входа приложения.

**Функции:**
- `on_startup()` - действия при запуске
- `on_shutdown()` - действия при остановке
- `main()` - главная функция

## Поток данных

```
┌─────────────────────────────────────────────────────────────┐
│                    Telegram User                            │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
                    ┌────────────────┐
                    │  Telegram API  │
                    └────────┬───────┘
                             │
                             ▼
                    ┌────────────────┐
                    │   aiogram      │
                    │  (Bot, DP)     │
                    └────────┬───────┘
                             │
                             ▼
                    ┌────────────────────────────┐
                    │  Routers                   │
                    │  - start_router            │
                    │  - help_router             │
                    │  - chatgpt_router          │
                    │  - echo_router             │
                    └────────┬───────────────────┘
                             │
                    ┌────────▼───────────────────┐
                    │  chatgpt_router            │
                    │  (if /chatgpt or /stop)    │
                    └────────┬───────────────────┘
                             │
                             ▼
                    ┌────────────────────────────┐
                    │  AmveraLLMService          │
                    │  (if user message)         │
                    └────────┬───────────────────┘
                             │
                             ▼
                    ┌────────────────────────────┐
                    │  Amvera LLM API            │
                    │  https://lllm.amvera.io    │
                    └────────┬───────────────────┘
                             │
                             ▼
                    ┌────────────────────────────┐
                    │  Response                  │
                    └────────┬───────────────────┘
                             │
                             ▼
                    ┌────────────────────────────┐
                    │  Send to Telegram          │
                    └────────┬───────────────────┘
                             │
                             ▼
                    ┌────────────────────────────┐
                    │  Telegram User             │
                    └────────────────────────────┘
```

## Обработка ошибок

### AmveraLLMService

```python
try:
    # Отправка запроса к API
    async with session.post(...) as response:
        if response.status == 200:
            # Успешный ответ
            return result["choices"][0]["message"]["content"]
        else:
            # HTTP ошибка
            logger.error(f"Ошибка: {response.status}")
            return None
except asyncio.TimeoutError:
    # Timeout
    logger.error("Timeout")
    return None
except Exception as e:
    # Другие ошибки
    logger.error(f"Исключение: {e}")
    return None
```

### chatgpt_router

```python
if response:
    # Успешный ответ
    await message.answer(response)
else:
    # Ошибка
    await message.answer("Произошла ошибка при обращении к ИИ...")
```

## Логирование

Все события логируются в файл `logs/bot.log`.

**Уровни логирования:**
- `DEBUG` - отладочная информация
- `INFO` - информационные сообщения
- `WARNING` - предупреждения
- `ERROR` - ошибки
- `CRITICAL` - критические ошибки

**Примеры логов:**
```
INFO: Бот запущен
INFO: Пользователь 123456 активировал режим ChatGPT
INFO: Отправка запроса к Amvera LLM
INFO: Статус ответа от Amvera LLM: 200
INFO: Успешный ответ от Amvera LLM
ERROR: Ошибка от Amvera LLM: 500 - Internal Server Error
```

## Тестирование

### Структура тестов

```
tests/
├── test_chatgpt_router.py          # Тесты для chatgpt_router
├── test_amvera_llm_service.py      # Тесты для AmveraLLMService
├── test_config.py                  # Тесты для Config
├── test_echo_router.py             # Тесты для echo_router
├── test_help_router.py             # Тесты для help_router
├── test_main.py                    # Тесты для main
├── test_start_router.py            # Тесты для start_router
├── test_text_service.py            # Тесты для text_service
└── test_utils_logging.py           # Тесты для logging
```

### Запуск тестов

```bash
# Все тесты
pytest

# С покрытием
pytest --cov=src

# Конкретный тест
pytest tests/test_chatgpt_router.py::test_chatgpt_start_handler
```

## Безопасность

### SSL/TLS

В текущей реализации отключена проверка SSL-сертификата для тестирования. Для продакшена необходимо включить проверку.

### Токены

Все токены хранятся в переменных окружения и не должны быть закоммичены в репозиторий.

### Логирование

Логирование не содержит чувствительной информации (токены, пароли и т.д.).

## Производительность

### Асинхронность

Все операции выполняются асинхронно с использованием `asyncio` и `aiohttp`.

### Timeout

Запросы к Amvera LLM имеют timeout 30 секунд.

### Кэширование

Кэширование не реализовано, но может быть добавлено в будущем.

## Масштабируемость

### Добавление новых команд

1. Создать новый файл в `src/bot/routers/`
2. Создать новый роутер
3. Зарегистрировать роутер в `src/bot/routers/__init__.py`

### Добавление новых сервисов

1. Создать новый файл в `src/bot/services/`
2. Создать новый класс сервиса
3. Экспортировать сервис в `src/bot/services/__init__.py`

## Зависимости

- **aiogram** - фреймворк для работы с Telegram Bot API
- **aiohttp** - асинхронный HTTP клиент
- **pydantic** - валидация данных
- **pydantic-settings** - управление конфигурацией
- **python-dotenv** - загрузка переменных окружения

## Версии

- **Python:** 3.11+
- **aiogram:** 3.3.0
- **aiohttp:** 3.9.5
