# Telegram Бот с ИИ Amvera

Telegram-бот на Python с интеграцией ИИ Amvera (модель gpt-5) для генерации текстов.

## Функциональность

- `/start` - приветственное сообщение
- `/help` - справка по командам
- `/chatgpt` - взаимодействие с ИИ Amvera (модель gpt-5)
- `/stop` - остановка диалога с ИИ
- Эхо-функциональность для всех остальных сообщений

## Установка и запуск

### Требования

- Python 3.11
- Виртуальное окружение Python

### Установка зависимостей

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Настройка переменных окружения

Создайте файл `.env` в корневой директории проекта:

```env
BOT_TOKEN=ваш_токен_бота
AMVERA_LLM_TOKEN=ваш_токен_amvera_llm
CONTEXT7_API_KEY=ваш_ключ_context7
```

### Запуск бота

```bash
python -m src.bot.main
```

## Структура проекта

```
.
├─ README.md
├─ requirements.txt
├─ .env
├─ .env.example
├─ src/
│  └─ bot/
│     ├─ __init__.py
│     ├─ __main__.py
│     ├─ main.py
│     ├─ config.py
│     ├─ routers/
│     │  ├─ __init__.py
│     │  ├─ start.py
│     │  ├─ help.py
│     │  ├─ echo.py
│     │  └─ chatgpt.py
│     ├─ keyboards/
│     │  ├─ __init__.py
│     │  └─ common.py
│     ├─ services/
│     │  ├─ __init__.py
│     │  ├─ text.py
│     │  └─ amvera_llm.py
│     └─ utils/
│        ├─ __init__.py
│        └─ logging.py
└─ tests/
   ├─ __init__.py
   ├─ test_chatgpt_router.py
   ├─ test_amvera_llm_service.py
   └─ ...
```

## Команды бота

- `/start` - запуск бота и приветственное сообщение
- `/help` - справка по командам
- `/chatgpt` - начало диалога с ИИ Amvera (модель gpt-5)
- `/stop` - завершение диалога с ИИ Amvera
- Любое другое сообщение - эхо-ответ (если не активирован режим ChatGPT)

## Интеграция с Amvera LLM

Бот использует API Amvera для генерации текстов с помощью модели gpt-5. 

### Как использовать

1. Отправьте команду `/chatgpt` для активации режима ИИ
2. Отправьте любое сообщение, и бот ответит с помощью ИИ Amvera
3. Отправьте команду `/stop` для выхода из режима ИИ

### Конфигурация

Для работы этой функции необходимо:
- Получить API токен Amvera LLM
- Добавить токен в переменную окружения `AMVERA_LLM_TOKEN`

### Документация API

- Swagger: https://lllm-swagger-amvera-services.amvera.io/openapi.yaml
- Документация: https://lllm-swagger-amvera-services.amvera.io/#/GPT/post_models_gpt

## Тестирование

Для запуска тестов используйте:

```bash
pytest
```

Для запуска тестов с покрытием:

```bash
pytest --cov=src
```

## Лицензия

126 | Этот проект распространяется под лицензией MIT. Подробности см. в файле [LICENSE](LICENSE).