import pytest
from aiogram import Dispatcher
from aiogram.types import Message, Chat, User
from aiogram.methods import SendMessage
from aiogram.filters import Command

from src.bot.routers.help import help_router


@pytest.mark.asyncio
async def test_help_handler():
    # Создаем диспетчер и регистрируем роутер
    dp = Dispatcher()
    dp.include_router(help_router)
    
    # Создаем тестовое сообщение
    message = Message(
        message_id=1,
        date="2023-01-01T00:00:00",
        chat=Chat(id=1, type="private"),
        from_user=User(id=1, is_bot=False, first_name="Test User"),
        text="/help"
    )
    
    # Обрабатываем сообщение
    result = await dp.feed_update(None, message)
    
    # Проверяем результат
    assert isinstance(result, SendMessage)
    assert result.text == "Это простой эхо-бот. Отправь мне любое сообщение, и я его повторю."