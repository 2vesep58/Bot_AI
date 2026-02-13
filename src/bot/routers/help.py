from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

help_router = Router()


@help_router.message(Command("help"))
async def help_handler(message: Message) -> None:
    """
    Обработчик команды /help.

    :param message: Сообщение.
    """
    await message.answer("Это простой эхо-бот. Отправь мне любое сообщение, и я его повторю.")