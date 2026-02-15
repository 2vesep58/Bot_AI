import pytest
from aiogram import Dispatcher
from aiogram.types import Message, Chat, User
from aiogram.methods import SendMessage
from unittest.mock import patch, AsyncMock, MagicMock

from src.bot.routers.chatgpt import chatgpt_router, chatgpt_active, chatgpt_modes
from src.bot.config import Config, AmveraConfig


@pytest.fixture
def config():
    """Фикстура для создания конфигурации."""
    return Config(
        bot_token="test_token",
        amvera_llm_token="test_amvera_token",
        context7_api_key="test_context7_key"
    )


@pytest.mark.asyncio
async def test_chatgpt_start_handler():
    # Создаем диспетчер и регистрируем роутер
    dp = Dispatcher()
    dp.include_router(chatgpt_router)
    
    # Создаем тестовое сообщение
    message = Message(
        message_id=1,
        date="2023-01-01T00:00:00",
        chat=Chat(id=1, type="private"),
        from_user=User(id=1, is_bot=False, first_name="Test User"),
        text="/chatgpt"
    )
    
    # Обрабатываем сообщение
    result = await dp.feed_update(None, message)
    
    # Проверяем результат
    assert isinstance(result, SendMessage)
    assert result.text == "Выберите режим работы ИИ:"
    
    # Проверяем, что пользователь добавлен в список активных
    assert chatgpt_active.get(1) is True


@pytest.mark.asyncio
async def test_chatgpt_stop_handler():
    # Добавляем пользователя в список активных
    chatgpt_active[1] = True
    chatgpt_modes[1] = "normal"
    
    # Создаем диспетчер и регистрируем роутер
    dp = Dispatcher()
    dp.include_router(chatgpt_router)
    
    # Создаем тестовое сообщение
    message = Message(
        message_id=1,
        date="2023-01-01T00:00:00",
        chat=Chat(id=1, type="private"),
        from_user=User(id=1, is_bot=False, first_name="Test User"),
        text="/stop"
    )
    
    # Обрабатываем сообщение
    result = await dp.feed_update(None, message)
    
    # Проверяем результат
    assert isinstance(result, SendMessage)
    assert result.text == "Вы вышли из режима общения с ИИ. Теперь я буду работать как эхо-бот."
    
    # Проверяем, что пользователь удален из списка активных
    assert chatgpt_active.get(1) is None
    assert chatgpt_modes.get(1) is None


@pytest.mark.asyncio
async def test_normal_mode_handler():
    # Добавляем пользователя в список активных
    chatgpt_active[1] = True
    
    # Создаем диспетчер и регистрируем роутер
    dp = Dispatcher()
    dp.include_router(chatgpt_router)
    
    # Создаем тестовое сообщение
    message = Message(
        message_id=1,
        date="2023-01-01T00:00:00",
        chat=Chat(id=1, type="private"),
        from_user=User(id=1, is_bot=False, first_name="Test User"),
        text="Обычный режим"
    )
    
    # Обрабатываем сообщение
    result = await dp.feed_update(None, message)
    
    # Проверяем результат
    assert isinstance(result, SendMessage)
    assert result.text == "Вы выбрали обычный режим работы ИИ. Отправьте ваш запрос."
    
    # Проверяем, что режим установлен
    assert chatgpt_modes.get(1) == "normal"


@pytest.mark.asyncio
async def test_ascii_mode_handler():
    # Добавляем пользователя в список активных
    chatgpt_active[1] = True
    
    # Создаем диспетчер и регистрируем роутер
    dp = Dispatcher()
    dp.include_router(chatgpt_router)
    
    # Создаем тестовое сообщение
    message = Message(
        message_id=1,
        date="2023-01-01T00:00:00",
        chat=Chat(id=1, type="private"),
        from_user=User(id=1, is_bot=False, first_name="Test User"),
        text="ASCII-арт"
    )
    
    # Обрабатываем сообщение
    result = await dp.feed_update(None, message)
    
    # Проверяем результат
    assert isinstance(result, SendMessage)
    assert result.text == "Вы выбрали режим ASCII-арта. Отправьте ваш запрос."
    
    # Проверяем, что режим установлен
    assert chatgpt_modes.get(1) == "ascii"


@pytest.mark.asyncio
async def test_translate_mode_handler():
    # Добавляем пользователя в список активных
    chatgpt_active[1] = True
    
    # Создаем диспетчер и регистрируем роутер
    dp = Dispatcher()
    dp.include_router(chatgpt_router)
    
    # Создаем тестовое сообщение
    message = Message(
        message_id=1,
        date="2023-01-01T00:00:00",
        chat=Chat(id=1, type="private"),
        from_user=User(id=1, is_bot=False, first_name="Test User"),
        text="Перевод на английский"
    )
    
    # Обрабатываем сообщение
    result = await dp.feed_update(None, message)
    
    # Проверяем результат
    assert isinstance(result, SendMessage)
    assert result.text == "Вы выбрали режим перевода на английский. Отправьте ваш запрос."
    
    # Проверяем, что режим установлен
    assert chatgpt_modes.get(1) == "translate"


@pytest.mark.asyncio
async def test_cancel_mode_handler():
    # Добавляем пользователя в список активных
    chatgpt_active[1] = True
    chatgpt_modes[1] = "normal"
    
    # Создаем диспетчер и регистрируем роутер
    dp = Dispatcher()
    dp.include_router(chatgpt_router)
    
    # Создаем тестовое сообщение
    message = Message(
        message_id=1,
        date="2023-01-01T00:00:00",
        chat=Chat(id=1, type="private"),
        from_user=User(id=1, is_bot=False, first_name="Test User"),
        text="Отмена"
    )
    
    # Обрабатываем сообщение
    result = await dp.feed_update(None, message)
    
    # Проверяем результат
    assert isinstance(result, SendMessage)
    assert result.text == "Вы отменили выбор режима. Режим ИИ деактивирован."
    
    # Проверяем, что пользователь удален из списков
    assert chatgpt_active.get(1) is None
    assert chatgpt_modes.get(1) is None


@pytest.mark.asyncio
async def test_chatgpt_handler_normal_mode(config):
    # Добавляем пользователя в список активных и устанавливаем режим
    chatgpt_active[1] = True
    chatgpt_modes[1] = "normal"
    
    # Создаем диспетчер и регистрируем роутер
    dp = Dispatcher()
    dp.include_router(chatgpt_router)
    
    # Создаем тестовое сообщение
    message = Message(
        message_id=1,
        date="2023-01-01T00:00:00",
        chat=Chat(id=1, type="private"),
        from_user=User(id=1, is_bot=False, first_name="Test User"),
        text="Привет, ИИ!"
    )
    
    # Мокаем AmveraLLMService
    with patch("src.bot.services.amvera_llm.AmveraLLMService.get_response") as mock_get_response:
        mock_get_response.return_value = "Привет, человек!"
        
        # Обрабатываем сообщение
        result = await dp.feed_update(None, message, config=config)
        
        # Проверяем, что был вызван метод get_response с правильным промтом
        mock_get_response.assert_called_once_with("Привет, ИИ!")
        
        # Проверяем результат
        assert isinstance(result, SendMessage)
        assert result.text == "Привет, человек!"
        
        # Проверяем, что режим удален после обработки
        assert chatgpt_modes.get(1) is None


@pytest.mark.asyncio
async def test_chatgpt_handler_ascii_mode(config):
    # Добавляем пользователя в список активных и устанавливаем режим
    chatgpt_active[1] = True
    chatgpt_modes[1] = "ascii"
    
    # Создаем диспетчер и регистрируем роутер
    dp = Dispatcher()
    dp.include_router(chatgpt_router)
    
    # Создаем тестовое сообщение
    message = Message(
        message_id=1,
        date="2023-01-01T00:00:00",
        chat=Chat(id=1, type="private"),
        from_user=User(id=1, is_bot=False, first_name="Test User"),
        text="Нарисуй кота"
    )
    
    # Мокаем AmveraLLMService
    with patch("src.bot.services.amvera_llm.AmveraLLMService.get_response") as mock_get_response:
        mock_get_response.return_value = "  /\\_/\\\n ( ^.^ )\n  > ^ <"
        
        # Обрабатываем сообщение
        result = await dp.feed_update(None, message, config=config)
        
        # Проверяем, что был вызван метод get_response с правильным промтом
        mock_get_response.assert_called_once_with("Ответь на следующий запрос в виде ASCII-арта: Нарисуй кота")
        
        # Проверяем результат
        assert isinstance(result, SendMessage)
        assert result.text == "  /\\_/\\\n ( ^.^ )\n  > ^ <"
        
        # Проверяем, что режим удален после обработки
        assert chatgpt_modes.get(1) is None


@pytest.mark.asyncio
async def test_chatgpt_handler_translate_mode(config):
    # Добавляем пользователя в список активных и устанавливаем режим
    chatgpt_active[1] = True
    chatgpt_modes[1] = "translate"
    
    # Создаем диспетчер и регистрируем роутер
    dp = Dispatcher()
    dp.include_router(chatgpt_router)
    
    # Создаем тестовое сообщение
    message = Message(
        message_id=1,
        date="2023-01-01T00:00:00",
        chat=Chat(id=1, type="private"),
        from_user=User(id=1, is_bot=False, first_name="Test User"),
        text="Привет, как дела?"
    )
    
    # Мокаем AmveraLLMService
    with patch("src.bot.services.amvera_llm.AmveraLLMService.get_response") as mock_get_response:
        mock_get_response.return_value = "Hi, how are you?"
        
        # Обрабатываем сообщение
        result = await dp.feed_update(None, message, config=config)
        
        # Проверяем, что был вызван метод get_response с правильным промтом
        mock_get_response.assert_called_once_with("Переведи следующий текст на английский язык: Привет, как дела?")
        
        # Проверяем результат
        assert isinstance(result, SendMessage)
        assert result.text == "Hi, how are you?"
        
        # Проверяем, что режим удален после обработки
        assert chatgpt_modes.get(1) is None


@pytest.mark.asyncio
async def test_chatgpt_handler_no_mode_selected():
    # Добавляем пользователя в список активных
    chatgpt_active[1] = True
    
    # Создаем диспетчер и регистрируем роутер
    dp = Dispatcher()
    dp.include_router(chatgpt_router)
    
    # Создаем тестовое сообщение
    message = Message(
        message_id=1,
        date="2023-01-01T00:00:00",
        chat=Chat(id=1, type="private"),
        from_user=User(id=1, is_bot=False, first_name="Test User"),
        text="Привет, ИИ!"
    )
    
    # Обрабатываем сообщение
    result = await dp.feed_update(None, message)
    
    # Проверяем результат
    assert isinstance(result, SendMessage)
    assert result.text == "Пожалуйста, сначала выберите режим работы ИИ."


@pytest.mark.asyncio
async def test_chatgpt_handler_error(config):
    # Добавляем пользователя в список активных и устанавливаем режим
    chatgpt_active[1] = True
    chatgpt_modes[1] = "normal"
    
    # Создаем диспетчер и регистрируем роутер
    dp = Dispatcher()
    dp.include_router(chatgpt_router)
    
    # Создаем тестовое сообщение
    message = Message(
        message_id=1,
        date="2023-01-01T00:00:00",
        chat=Chat(id=1, type="private"),
        from_user=User(id=1, is_bot=False, first_name="Test User"),
        text="Привет, ИИ!"
    )
    
    # Мокаем AmveraLLMService для симуляции ошибки
    with patch("src.bot.services.amvera_llm.AmveraLLMService.get_response") as mock_get_response:
        mock_get_response.return_value = None
        
        # Обрабатываем сообщение
        result = await dp.feed_update(None, message, config=config)
        
        # Проверяем результат
        assert isinstance(result, SendMessage)
        assert result.text == "Произошла ошибка при обращении к ИИ. Пожалуйста, попробуйте позже."
