import pytest
from aiogram import Dispatcher
from aiogram.types import Message, Chat, User
from aiogram.methods import SendMessage

from src.bot.routers.echo import echo_router


@pytest.mark.asyncio
async def test_echo_handler_text():
    # Создаем диспетчер и регистрируем роутер
    dp = Dispatcher()
    dp.include_router(echo_router)
    
    # Создаем тестовое сообщение
    message = Message(
        message_id=1,
        date="2023-01-01T00:00:00",
        chat=Chat(id=1, type="private"),
        from_user=User(id=1, is_bot=False, first_name="Test User"),
        text="Тестовое сообщение"
    )
    
    # Обрабатываем сообщение
    result = await dp.feed_update(None, message)
    
    # Проверяем результат
    assert isinstance(result, SendMessage)
    assert result.text == "Тестовое сообщение"


@pytest.mark.asyncio
async def test_echo_handler_non_text():
    # Создаем диспетчер и регистрируем роутер
    dp = Dispatcher()
    dp.include_router(echo_router)
    
    # Создаем тестовое сообщение без текста
    message = Message(
        message_id=1,
        date="2023-01-01T00:00:00",
        chat=Chat(id=1, type="private"),
        from_user=User(id=1, is_bot=False, first_name="Test User"),
        text=None
    )
    
    # Обрабатываем сообщение
    result = await dp.feed_update(None, message)
    
    # Проверяем результат
    assert isinstance(result, SendMessage)
    assert result.text == "Эхо-бот поддерживает только текстовые сообщения."