import pytest
import logging
import os
import tempfile
from unittest.mock import patch

from src.bot.utils.logging import setup_logging
from src.bot.config import Config


def test_setup_logging():
    """Тест настройки логирования."""
    # Создаем временную директорию для логов
    with tempfile.TemporaryDirectory() as temp_dir:
        # Создаем конфигурацию с временной директорией для логов
        config = Config(
            bot_token="test_token",
            amvera_llm_token="test_amvera_token",
            context7_api_key="test_context7_key"
        )
        
        # Мокаем os.path.exists и os.makedirs для использования временной директории
        with patch("os.path.exists") as mock_exists, \
             patch("os.makedirs") as mock_makedirs, \
             patch("src.bot.utils.logging.os.path.join", return_value=os.path.join(temp_dir, "bot.log")):
            
            # Настраиваем возвращаемые значения для моков
            mock_exists.return_value = False
            
            # Вызываем тестируемую функцию
            setup_logging(config)
            
            # Проверяем, что os.makedirs был вызван с правильными аргументами
            mock_makedirs.assert_called_once_with("logs")
            
            # Проверяем, что логирование настроено правильно
            logger = logging.getLogger()
            assert logger.level == logging.INFO
            
            # Проверяем, что добавлены нужные обработчики
            handlers = logger.handlers
            assert len(handlers) == 2
            assert any(isinstance(handler, logging.FileHandler) for handler in handlers)
            assert any(isinstance(handler, logging.StreamHandler) for handler in handlers)
            
            # Проверяем формат логов
            formatter = handlers[0].formatter
            assert formatter._fmt == "%(asctime)s - %(name)s - %(levelname)s - %(message)s"