# Изменения в проекте

## Краткое резюме

Интегрирована поддержка Amvera LLM (модель gpt-5) в Telegram бот. Теперь по команде `/chatgpt` бот отвечает как обычная LLM с помощью ИИ Amvera.

## Что было добавлено

### 1. Новый сервис AmveraLLMService
- **Файл:** `src/bot/services/amvera_llm.py`
- **Функция:** Взаимодействие с API Amvera LLM
- **Основной метод:** `get_response(user_message: str) -> Optional[str]`

### 2. Обновленный роутер chatgpt
- **Файл:** `src/bot/routers/chatgpt.py`
- **Изменения:** Использует новый сервис AmveraLLMService
- **Команды:**
  - `/chatgpt` - активирует режим ИИ
  - `/stop` - деактивирует режим ИИ

### 3. Новые тесты
- **Файл:** `tests/test_amvera_llm_service.py` - тесты для сервиса
- **Файл:** `tests/test_chatgpt_router.py` - обновленные тесты для роутера

### 4. Документация
- **USAGE.md** - руководство по использованию
- **INTEGRATION.md** - описание интеграции
- **CHANGES.md** - этот файл
- **.env.example** - пример конфигурации

## Как использовать

### Установка
```bash
pip install -r requirements.txt
```

### Запуск
```bash
python -m src.bot.main
```

### Использование в Telegram
1. Отправьте `/chatgpt` для активации режима ИИ
2. Отправьте любое сообщение
3. Бот ответит с помощью ИИ Amvera
4. Отправьте `/stop` для выхода из режима ИИ

## Переменные окружения

Убедитесь, что в файле `.env` указаны:
```env
BOT_TOKEN=ваш_токен_бота
AMVERA_LLM_TOKEN=ваш_токен_amvera
CONTEXT7_API_KEY=ваш_ключ_context7
```

## Технические детали

- **API Endpoint:** https://lllm.amvera.io/v1/chat/completions
- **Модель:** gpt-5
- **Timeout:** 30 секунд
- **Обработка ошибок:** HTTP ошибки, timeout, исключения

## Файлы, которые были изменены

### Созданы:
- `src/bot/services/amvera_llm.py`
- `tests/test_amvera_llm_service.py`
- `USAGE.md`
- `INTEGRATION.md`
- `CHANGES.md`
- `.env.example`

### Обновлены:
- `src/bot/routers/chatgpt.py`
- `src/bot/services/__init__.py`
- `requirements.txt`
- `README.md`
- `tests/test_chatgpt_router.py`

## Примечания

- SSL-сертификат отключен для тестирования (нужно включить для продакшена)
- Все операции логируются в `logs/bot.log`
- Сервис обрабатывает все типы ошибок и возвращает `None` в случае проблем
