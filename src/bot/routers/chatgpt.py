from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
import aiohttp
import json
import logging
import ssl

from src.bot.config import Config

chatgpt_router = Router()

# URL для доступа к API Amvera LLM
AMVERA_LLM_URL = "https://lllm.amvera.io/v1/chat/completions"

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
            
            # Формируем запрос к API Amvera LLM
            payload = {
                "model": "gpt-5",
                "messages": [
                    {
                        "role": "user",
                        "content": message.text
                    }
                ]
            }

            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {config.amvera.token.get_secret_value()}"
            }

            # Отключаем проверку SSL-сертификата (только для тестирования!)
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE

            try:
                logging.info(f"Отправка запроса к Amvera LLM: {payload}")
                logging.info(f"Заголовки запроса: {headers}")
                # Отправляем запрос к API Amvera LLM
                async with aiohttp.ClientSession() as session:
                    async with session.post(AMVERA_LLM_URL, json=payload, headers=headers, ssl=ssl_context) as response:
                        logging.info(f"Статус ответа от Amvera LLM: {response.status}")
                        if response.status == 200:
                            # Получаем ответ от API
                            result = await response.json()
                            logging.info(f"Ответ от Amvera LLM: {result}")
                            # Отправляем ответ пользователю
                            await message.answer(result["choices"][0]["message"]["content"])
                        else:
                            error_text = await response.text()
                            logging.error(f"Ошибка от Amvera LLM: {response.status} - {error_text}")
                            await message.answer("Произошла ошибка при обращении к ИИ. Код ошибки: " + str(response.status))
            except Exception as e:
                # Обрабатываем возможные ошибки
                logging.error(f"Исключение при обращении к Amvera LLM: {e}")
                await message.answer("Произошла ошибка при обращении к ИИ. Пожалуйста, попробуйте позже.")
        else:
            logging.info(f"Сообщение пользователя {message.from_user.id} является командой, пропускаем")
    else:
        logging.info(f"Пользователь {message.from_user.id} не находится в режиме ChatGPT, сообщение обрабатывается другими роутерами")
        # Если режим ChatGPT не активирован, сообщение обрабатывается другими роутерами (например, эхо)