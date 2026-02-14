import pytest
from aiogram import Dispatcher
from aiogram.types import Message, Chat, User
from aiogram.methods import SendMessage
from unittest.mock import patch, AsyncMock, MagicMock

from src.bot.routers.chatgpt import chatgpt_router, chatgpt_active
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
    assert result.text == "Отправьте мне сообщение, и я отвечу с помощью ИИ. Чтобы выйти из режима ИИ, отправьте /stop."
    
    # Проверяем, что пользователь добавлен в список активных
    assert chatgpt_active.get(1) is True


@pytest.mark.asyncio
async def test_chatgpt_stop_handler():
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
        text="/stop"
    )
    
    # Обрабатываем сообщение
    result = await dp.feed_update(None, message)
    
    # Проверяем результат
    assert isinstance(result, SendMessage)
    assert result.text == "Вы вышли из режима общения с ИИ. Теперь я буду работать как эхо-бот."
    
    # Проверяем, что пользователь удален из списка активных
    assert chatgpt_active.get(1) is None


@pytest.mark.asyncio
async def test_chatgpt_handler(config):
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
    
    # Мокаем AmveraLLMService
    with patch("src.bot.services.amvera_llm.AmveraLLMService.get_response") as mock_get_response:
        mock_get_response.return_value = "Привет, человек!"
        
        # Обрабатываем сообщение
        result = await dp.feed_update(None, message, config=config)
        
        # Проверяем результат
        assert isinstance(result, SendMessage)
        assert result.text == "Привет, человек!"


@pytest.mark.asyncio
async def test_chatgpt_handler_error(config):
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
    
    # Мокаем AmveraLLMService для симуляции ошибки
    with patch("src.bot.services.amvera_llm.AmveraLLMService.get_response") as mock_get_response:
        mock_get_response.return_value = None
        
        # Обрабатываем сообщение
        result = await dp.feed_update(None, message, config=config)
        
        # Проверяем результат
        assert isinstance(result, SendMessage)
        assert result.text == "Произошла ошибка при обращении к ИИ. Пожалуйста, попробуйте позже."
