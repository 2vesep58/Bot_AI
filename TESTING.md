# Тестирование

## Структура тестов

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

## Запуск тестов

### Все тесты

```bash
pytest
```

### С покрытием

```bash
pytest --cov=src
```

### Конкретный файл

```bash
pytest tests/test_chatgpt_router.py
```

### Конкретный тест

```bash
pytest tests/test_chatgpt_router.py::test_chatgpt_start_handler
```

### С подробным выводом

```bash
pytest -v
```

### С выводом логов

```bash
pytest -s
```

## Тесты AmveraLLMService

### test_amvera_llm_service_get_response_success

Тест успешного получения ответа от Amvera LLM.

```python
@pytest.mark.asyncio
async def test_amvera_llm_service_get_response_success(config):
    service = AmveraLLMService(config)
    
    with patch("aiohttp.ClientSession.post") as mock_post:
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={
            "choices": [{
                "message": {
                    "content": "Привет, человек!"
                }
            }]
        })
        
        mock_post.return_value.__aenter__.return_value = mock_response
        mock_post.return_value.__aexit__.return_value = None
        
        response = await service.get_response("Привет, ИИ!")
        
        assert response == "Привет, человек!"
```

### test_amvera_llm_service_get_response_error

Тест обработки ошибки от Amvera LLM.

```python
@pytest.mark.asyncio
async def test_amvera_llm_service_get_response_error(config):
    service = AmveraLLMService(config)
    
    with patch("aiohttp.ClientSession.post") as mock_post:
        mock_response = AsyncMock()
        mock_response.status = 500
        mock_response.text = AsyncMock(return_value="Internal Server Error")
        
        mock_post.return_value.__aenter__.return_value = mock_response
        mock_post.return_value.__aexit__.return_value = None
        
        response = await service.get_response("Привет, ИИ!")
        
        assert response is None
```

### test_amvera_llm_service_get_response_timeout

Тест обработки timeout при обращении к Amvera LLM.

```python
@pytest.mark.asyncio
async def test_amvera_llm_service_get_response_timeout(config):
    service = AmveraLLMService(config)
    
    with patch("aiohttp.ClientSession.post") as mock_post:
        mock_post.side_effect = asyncio.TimeoutError()
        
        response = await service.get_response("Привет, ИИ!")
        
        assert response is None
```

### test_amvera_llm_service_get_response_exception

Тест обработки исключения при обращении к Amvera LLM.

```python
@pytest.mark.asyncio
async def test_amvera_llm_service_get_response_exception(config):
    service = AmveraLLMService(config)
    
    with patch("aiohttp.ClientSession.post") as mock_post:
        mock_post.side_effect = Exception("Network error")
        
        response = await service.get_response("Привет, ИИ!")
        
        assert response is None
```

## Тесты chatgpt_router

### test_chatgpt_start_handler

Тест активации режима ИИ.

```python
@pytest.mark.asyncio
async def test_chatgpt_start_handler():
    dp = Dispatcher()
    dp.include_router(chatgpt_router)
    
    message = Message(
        message_id=1,
        date="2023-01-01T00:00:00",
        chat=Chat(id=1, type="private"),
        from_user=User(id=1, is_bot=False, first_name="Test User"),
        text="/chatgpt"
    )
    
    result = await dp.feed_update(None, message)
    
    assert isinstance(result, SendMessage)
    assert result.text == "Отправьте мне сообщение, и я отвечу с помощью ИИ. Чтобы выйти из режима ИИ, отправьте /stop."
    assert chatgpt_active.get(1) is True
```

### test_chatgpt_stop_handler

Тест деактивации режима ИИ.

```python
@pytest.mark.asyncio
async def test_chatgpt_stop_handler():
    chatgpt_active[1] = True
    
    dp = Dispatcher()
    dp.include_router(chatgpt_router)
    
    message = Message(
        message_id=1,
        date="2023-01-01T00:00:00",
        chat=Chat(id=1, type="private"),
        from_user=User(id=1, is_bot=False, first_name="Test User"),
        text="/stop"
    )
    
    result = await dp.feed_update(None, message)
    
    assert isinstance(result, SendMessage)
    assert result.text == "Вы вышли из режима общения с ИИ. Теперь я буду работать как эхо-бот."
    assert chatgpt_active.get(1) is None
```

### test_chatgpt_handler

Тест обработки сообщения в режиме ИИ.

```python
@pytest.mark.asyncio
async def test_chatgpt_handler(config):
    chatgpt_active[1] = True
    
    dp = Dispatcher()
    dp.include_router(chatgpt_router)
    
    message = Message(
        message_id=1,
        date="2023-01-01T00:00:00",
        chat=Chat(id=1, type="private"),
        from_user=User(id=1, is_bot=False, first_name="Test User"),
        text="Привет, ИИ!"
    )
    
    with patch("src.bot.services.amvera_llm.AmveraLLMService.get_response") as mock_get_response:
        mock_get_response.return_value = "Привет, человек!"
        
        result = await dp.feed_update(None, message, config=config)
        
        assert isinstance(result, SendMessage)
        assert result.text == "Привет, человек!"
```

### test_chatgpt_handler_error

Тест обработки ошибки при обращении к LLM.

```python
@pytest.mark.asyncio
async def test_chatgpt_handler_error(config):
    chatgpt_active[1] = True
    
    dp = Dispatcher()
    dp.include_router(chatgpt_router)
    
    message = Message(
        message_id=1,
        date="2023-01-01T00:00:00",
        chat=Chat(id=1, type="private"),
        from_user=User(id=1, is_bot=False, first_name="Test User"),
        text="Привет, ИИ!"
    )
    
    with patch("src.bot.services.amvera_llm.AmveraLLMService.get_response") as mock_get_response:
        mock_get_response.return_value = None
        
        result = await dp.feed_update(None, message, config=config)
        
        assert isinstance(result, SendMessage)
        assert result.text == "Произошла ошибка при обращении к ИИ. Пожалуйста, попробуйте позже."
```

## Мокирование

### Мокирование aiohttp.ClientSession

```python
from unittest.mock import patch, AsyncMock

with patch("aiohttp.ClientSession.post") as mock_post:
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value={...})
    
    mock_post.return_value.__aenter__.return_value = mock_response
    mock_post.return_value.__aexit__.return_value = None
    
    # Ваш код здесь
```

### Мокирование AmveraLLMService

```python
from unittest.mock import patch

with patch("src.bot.services.amvera_llm.AmveraLLMService.get_response") as mock_get_response:
    mock_get_response.return_value = "Ответ от LLM"
    
    # Ваш код здесь
```

## Фикстуры

### config

Фикстура для создания конфигурации.

```python
@pytest.fixture
def config():
    return Config(
        bot_token="test_token",
        amvera_llm_token="test_amvera_token",
        context7_api_key="test_context7_key"
    )
```

## Покрытие кода

### Запуск с покрытием

```bash
pytest --cov=src
```

### Генерация HTML отчета

```bash
pytest --cov=src --cov-report=html
```

### Просмотр отчета

```bash
open htmlcov/index.html
```

## Непрерывная интеграция

### GitHub Actions

Пример конфигурации для GitHub Actions:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.11
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: pytest --cov=src
```

## Лучшие практики

1. **Используйте фикстуры** для создания тестовых данных
2. **Мокируйте внешние зависимости** (API, БД и т.д.)
3. **Тестируйте обработку ошибок** (исключения, timeout и т.д.)
4. **Используйте асинхронные тесты** для асинхронного кода
5. **Проверяйте покрытие кода** (минимум 80%)
6. **Используйте описательные имена** для тестов
7. **Тестируйте граничные случаи** (пустые строки, None и т.д.)

## Решение проблем

### Ошибка: "RuntimeError: Event loop is closed"

Используйте `@pytest.mark.asyncio` для асинхронных тестов.

### Ошибка: "ModuleNotFoundError"

Убедитесь, что вы установили зависимости:
```bash
pip install -r requirements.txt
```

### Ошибка: "Timeout"

Увеличьте timeout в конфигурации pytest:
```bash
pytest --timeout=300
```

## Дополнительная информация

- **pytest:** https://docs.pytest.org/
- **unittest.mock:** https://docs.python.org/3/library/unittest.mock.html
- **pytest-asyncio:** https://github.com/pytest-dev/pytest-asyncio
