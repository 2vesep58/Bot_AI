"""Клавиатуры для бота."""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_chatgpt_modes_keyboard() -> ReplyKeyboardMarkup:
    """
    Получить клавиатуру с режимами работы ChatGPT.

    :return: Клавиатура с кнопками режимов.
    """
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Обычный режим")],
            [KeyboardButton(text="ASCII-арт")],
            [KeyboardButton(text="Перевод на английский")],
            [KeyboardButton(text="Рецепт из холодильника")],
            [KeyboardButton(text="Отмена")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    return keyboard
