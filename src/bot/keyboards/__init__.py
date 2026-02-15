"""Модуль клавиатур для бота."""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_chatgpt_modes_keyboard() -> ReplyKeyboardMarkup:
    """
    Создать клавиатуру для выбора режима работы ИИ.
    
    :return: Клавиатура с режимами работы ИИ.
    """
    keyboard = [
        [KeyboardButton(text="Обычный режим")],
        [KeyboardButton(text="ASCII-арт")],
        [KeyboardButton(text="Перевод на английский")],
        [KeyboardButton(text="Рецепт из холодильника")],
        [KeyboardButton(text="Отмена")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)