from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

start_router = Router()


@start_router.message(CommandStart())
async def start_handler(message: Message) -> None:
    """
    Обработчик команды /start.

    :param message: Сообщение.
    """
    await message.answer("Привет! Я эхо-бот. Отправь мне любое сообщение, и я его повторю.")