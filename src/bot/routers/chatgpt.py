from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
import logging

from src.bot.config import load_config
from src.bot.services.amvera_llm import AmveraLLMService
from src.bot.keyboards import get_chatgpt_modes_keyboard

chatgpt_router = Router()

# Храним состояние активации ChatGPT для каждого пользователя
chatgpt_active = {}
# Храним выбранный режим работы ИИ для каждого пользователя
chatgpt_modes = {}

# Загружаем конфигурацию один раз при импорте
config = load_config()


@chatgpt_router.message(Command("chatgpt"))
async def chatgpt_start_handler(message: Message) -> None:
    """
    Обработчик команды /chatgpt.

    :param message: Сообщение.
    """
    logging.info(f"Пользователь {message.from_user.id} активировал режим ChatGPT")
    chatgpt_active[message.from_user.id] = True
    await message.answer("Выберите режим работы ИИ:", reply_markup=get_chatgpt_modes_keyboard())


@chatgpt_router.message(Command("stop"))
async def chatgpt_stop_handler(message: Message) -> None:
    """
    Обработчик команды /stop для выхода из режима ChatGPT.

    :param message: Сообщение.
    """
    logging.info(f"Пользователь {message.from_user.id} деактивировал режим ChatGPT")
    if message.from_user.id in chatgpt_active:
        del chatgpt_active[message.from_user.id]
    if message.from_user.id in chatgpt_modes:
        del chatgpt_modes[message.from_user.id]
    await message.answer("Вы вышли из режима общения с ИИ. Теперь я буду работать как эхо-бот.", reply_markup=ReplyKeyboardRemove())


# Обработчики выбора режима работы ИИ
@chatgpt_router.message(F.text == "Обычный режим")
async def normal_mode_handler(message: Message) -> None:
    """
    Обработчик выбора обычного режима работы ИИ.

    :param message: Сообщение.
    """
    if message.from_user.id in chatgpt_active:
        chatgpt_modes[message.from_user.id] = "normal"
        await message.answer("Вы выбрали обычный режим работы ИИ. Отправьте ваш запрос.", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("Сначала активируйте режим ИИ с помощью команды /chatgpt.")


@chatgpt_router.message(F.text == "ASCII-арт")
async def ascii_mode_handler(message: Message) -> None:
    """
    Обработчик выбора режима ASCII-арта.

    :param message: Сообщение.
    """
    if message.from_user.id in chatgpt_active:
        chatgpt_modes[message.from_user.id] = "ascii"
        await message.answer("Вы выбрали режим ASCII-арта. Отправьте ваш запрос.", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("Сначала активируйте режим ИИ с помощью команды /chatgpt.")


@chatgpt_router.message(F.text == "Перевод на английский")
async def translate_mode_handler(message: Message) -> None:
    """
    Обработчик выбора режима перевода на английский.

    :param message: Сообщение.
    """
    if message.from_user.id in chatgpt_active:
        chatgpt_modes[message.from_user.id] = "translate"
        await message.answer("Вы выбрали режим перевода на английский. Отправьте ваш запрос.", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("Сначала активируйте режим ИИ с помощью команды /chatgpt.")


@chatgpt_router.message(F.text == "Рецепт из холодильника")
async def recipe_mode_handler(message: Message) -> None:
    """
    Обработчик выбора режима рецепта из холодильника.

    :param message: Сообщение.
    """
    if message.from_user.id in chatgpt_active:
        chatgpt_modes[message.from_user.id] = "recipe"
        await message.answer("Вы выбрали режим рецепта из холодильника. Напишите продукты, которые у вас есть.", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("Сначала активируйте режим ИИ с помощью команды /chatgpt.")


@chatgpt_router.message(F.text == "Отмена")
async def cancel_mode_handler(message: Message) -> None:
    """
    Обработчик отмены выбора режима работы ИИ.

    :param message: Сообщение.
    """
    if message.from_user.id in chatgpt_active:
        del chatgpt_active[message.from_user.id]
        if message.from_user.id in chatgpt_modes:
            del chatgpt_modes[message.from_user.id]
        await message.answer("Вы отменили выбор режима. Режим ИИ деактивирован.", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("Сначала активируйте режим ИИ с помощью команды /chatgpt.")


@chatgpt_router.message(F.text)
async def chatgpt_handler(message: Message) -> None:
    """
    Обработчик сообщений для ChatGPT.

    :param message: Сообщение.
    """
    logging.info(f"Получено сообщение от пользователя {message.from_user.id}: {message.text}")

    # Проверяем, что пользователь активировал режим ChatGPT
    if message.from_user.id in chatgpt_active:
        logging.info(f"Пользователь {message.from_user.id} находится в режиме ChatGPT")
        # Проверяем, что сообщение не является командой
        if message.text and not message.text.startswith('/'):
            # Проверяем, что пользователь выбрал режим работы ИИ
            if message.from_user.id in chatgpt_modes:
                mode = chatgpt_modes[message.from_user.id]
                logging.info(f"Пользователь {message.from_user.id} выбрал режим работы ИИ: {mode}")

                # Формируем промт в зависимости от выбранного режима
                if mode == "normal":
                    prompt = message.text
                elif mode == "ascii":
                    prompt = f"Ответь на следующий запрос в виде ASCII-арта: {message.text}"
                elif mode == "translate":
                    prompt = f"Переведи следующий текст на английский язык: {message.text}"
                elif mode == "recipe":
                    prompt = f"Из следующих продуктов предложи рецепты блюд, которые можно приготовить: {message.text}"
                else:
                    prompt = message.text

                logging.info(f"Отправка запроса к Amvera LLM для пользователя {message.from_user.id}")

                # Показываем пользователю, что бот обрабатывает запрос
                await message.answer("⏳ Обрабатываю ваш запрос...")

                # Отправляем действие "печатает" пользователю
                await message.bot.send_chat_action(message.chat.id, "typing")

                # Создаем сервис и получаем ответ
                llm_service = AmveraLLMService(config)
                response = await llm_service.get_response(prompt)

                if response:
                    await message.answer(response)
                else:
                    await message.answer("Произошла ошибка при обращении к ИИ. Пожалуйста, попробуйте позже.")

                # Удаляем информацию о выбранном режиме, чтобы пользователь мог выбрать другой режим при следующем запросе
                del chatgpt_modes[message.from_user.id]
            else:
                await message.answer("Пожалуйста, сначала выберите режим работы ИИ.")
        else:
            logging.info(f"Сообщение пользователя {message.from_user.id} является командой, пропускаем")
    else:
        logging.info(f"Пользователь {message.from_user.id} не находится в режиме ChatGPT, сообщение обрабатывается другими роутерами")
