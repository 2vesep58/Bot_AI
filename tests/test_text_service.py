import pytest

from src.bot.services.text import process_text


def test_process_text() -> None:
    """Тест обработки текста."""
    # Подготовка данных
    input_text = "Привет, мир!"
    expected_result = "Привет, мир!"

    # Выполнение тестируемого кода
    result = process_text(input_text)

    # Проверка результата
    assert result == expected_result


def test_process_text_empty() -> None:
    """Тест обработки пустого текста."""
    # Подготовка данных
    input_text = ""
    expected_result = ""

    # Выполнение тестируемого кода
    result = process_text(input_text)

    # Проверка результата
    assert result == expected_result


def test_process_text_special_characters() -> None:
    """Тест обработки текста со специальными символами."""
    # Подготовка данных
    input_text = "Тест со спецсимволами: !@#$%^&*()"
    expected_result = "Тест со спецсимволами: !@#$%^&*()"

    # Выполнение тестируемого кода
    result = process_text(input_text)

    # Проверка результата
    assert result == expected_result