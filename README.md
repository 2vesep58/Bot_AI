# Telegram Бот с ИИ Amvera

Telegram-бот на Python с интеграцией ИИ Amvera для генерации текстов.

## Функциональность

- `/start` - приветственное сообщение
- `/help` - справка по командам
- `/chatgpt` - взаимодействие с ИИ Amvera
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
AMVERA_TOKEN=ваш_токен_amvera
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
│     │  └─ text.py
│     └─ utils/
│        ├─ __init__.py
│        └─ logging.py
└─ tests/
   ├─ __init__.py
   └─ test_text_service.py
```

## Команды бота

- `/start` - запуск бота и приветственное сообщение
- `/help` - справка по командам
- `/chatgpt` - начало диалога с ИИ Amvera
- `/stop` - завершение диалога с ИИ Amvera
- Любое другое сообщение - эхо-ответ

## Интеграция с Amvera

Бот использует API Amvera для генерации текстов. Для работы этой функции необходим токен API Amvera, который должен быть указан в переменных окружения.