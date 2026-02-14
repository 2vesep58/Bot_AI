# Быстрый старт

## 1. Установка зависимостей

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Настройка переменных окружения

Убедитесь, что в файле `.env` указаны:

```env
BOT_TOKEN=ваш_токен_бота_telegram
AMVERA_LLM_TOKEN=ваш_токен_amvera_llm
CONTEXT7_API_KEY=ваш_ключ_context7
```

Вы можете скопировать `.env.example` и заполнить значения:

```bash
copy .env.example .env
```

## 3. Запуск бота

```bash
python -m src.bot.main
```

## 4. Использование в Telegram

### Активировать режим ИИ
```
/chatgpt
```

### Отправить сообщение ИИ
```
Что такое Python?
```

### Выйти из режима ИИ
```
/stop
```

## Доступные команды

- `/start` - приветственное сообщение
- `/help` - справка по командам
- `/chatgpt` - активировать режим ИИ
- `/stop` - деактивировать режим ИИ

## Тестирование

```bash
pytest
```

## Документация

- **README.md** - основная документация
- **USAGE.md** - подробное руководство по использованию
- **INTEGRATION.md** - описание интеграции с Amvera LLM
- **CHANGES.md** - список изменений

## Решение проблем

### Ошибка: "ModuleNotFoundError: No module named 'aiogram'"

Убедитесь, что вы установили зависимости:
```bash
pip install -r requirements.txt
```

### Ошибка: "Invalid token"

Проверьте, что в файле `.env` указан правильный токен Telegram бота.

### Ошибка: "Unauthorized" при обращении к Amvera LLM

Проверьте, что в файле `.env` указан правильный токен Amvera LLM.

### Бот не отвечает

Проверьте логи в файле `logs/bot.log`.

## Дополнительная информация

- **Документация aiogram:** https://docs.aiogram.dev/
- **Документация Amvera LLM:** https://lllm-swagger-amvera-services.amvera.io/
- **Документация Python:** https://docs.python.org/3/
