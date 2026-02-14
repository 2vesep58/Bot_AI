from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
import logging

from src.bot.config import Config
from src.bot.services.amvera_llm import AmveraLLMService

chatgpt_router = Router()

# Храним состояние активации ChatGPT для каждого пользователя
chatgpt_active = {}


@chatgpt_router.message(Command("chatgpt"))
async def chatgpt_start_handler(message: Message) -> None:
    """
    Обработчик команды /chatgpt.

    :param message: Сообщение.
    """
    logging.info(f"Пользователь {message.from_user.id} активировал режим ChatGPT")
    chatgpt_active[message.from_user.id] = True
    await message.answer("Отправьте мне сообщение, и я отвечу с помощью ИИ. Чтобы выйти из режима ИИ, отправьте /stop.")


@chatgpt_router.message(Command("stop"))
async def chatgpt_stop_handler(message: Message) -> None:
    """
    Обработчик команды /stop для выхода из режима ChatGPT.

    :param message: Сообщение.
    """
    logging.info(f"Пользователь {message.from_user.id} деактивировал режим ChatGPT")
    if message.from_user.id in chatgpt_active:
        del chatgpt_active[message.from_user.id]
    await message.answer("Вы вышли из режима общения с ИИ. Теперь я буду работать как эхо-бот.")


@chatgpt_router.message(F.text)
async def chatgpt_handler(message: Message, config: Config) -> None:
    """
    Обработчик сообщений для ChatGPT.

    :param message: Сообщение.
    :param config: Конфигурация бота.
    """
    logging.info(f"Получено сообщение от пользователя {message.from_user.id}: {message.text}")
    
    # Проверяем, что пользователь активировал режим ChatGPT
    if message.from_user.id in chatgpt_active:
        logging.info(f"Пользователь {message.from_user.id} находится в режиме ChatGPT")
        # Проверяем, что сообщение не является командой
        if message.text and not message.text.startswith('/'):
            logging.info(f"Отправка запроса к Amvera LLM для пользователя {message.from_user.id}")
            
            # Показываем пользователю, что бот обрабатывает запрос
            await message.answer("⏳ Обрабатываю ваш запрос...")
            
            # Отправляем действие "печатает" пользователю
            await message.bot.send_chat_action(message.chat.id, "typing")
            
            # Создаем сервис и получаем ответ
            llm_service = AmveraLLMService(config)
            response = await llm_service.get_response(message.text)
            
            if response:
                await message.answer(response)
            else:
                await message.answer("Произошла ошибка при обращении к ИИ. Пожалуйста, попробуйте позже.")
        else:
            logging.info(f"Сообщение пользователя {message.from_user.id} является командой, пропускаем")
    else:
        logging.info(f"Пользователь {message.from_user.id} не находится в режиме ChatGPT, сообщение обрабатывается другими роутерами")
