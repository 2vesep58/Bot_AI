from aiogram import Router
from aiogram.types import Message

echo_router = Router()


@echo_router.message()
async def echo_handler(message: Message) -> None:
    """
    Обработчик эхо-сообщений.

    :param message: Сообщение.
    """
    if message.text:
        await message.answer(message.text)
    else:
        await message.answer("Эхо-бот поддерживает только текстовые сообщения.")