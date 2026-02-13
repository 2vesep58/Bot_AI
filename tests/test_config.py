import pytest
import os
from unittest.mock import patch

from src.bot.config import Config, load_config


def test_config_creation():
    """Тест создания конфигурации."""
    # Тестируем создание конфигурации с валидными данными
    with patch.dict(os.environ, {
        "BOT_TOKEN": "test_bot_token",
        "AMVERA_LLM_TOKEN": "test_amvera_token",
        "CONTEXT7_API_KEY": "test_context7_key"
    }):
        config = Config()
        
        # Проверяем, что значения установлены правильно
        assert config.bot_token.get_secret_value() == "test_bot_token"
        assert config.amvera_llm_token.get_secret_value() == "test_amvera_token"
        assert config.context7_api_key.get_secret_value() == "test_context7_key"


def test_config_properties():
    """Тест свойств конфигурации."""
    # Тестируем свойства конфигурации
    with patch.dict(os.environ, {
        "BOT_TOKEN": "test_bot_token",
        "AMVERA_LLM_TOKEN": "test_amvera_token",
        "CONTEXT7_API_KEY": "test_context7_key"
    }):
        config = Config()
        
        # Проверяем свойства
        assert config.bot.token.get_secret_value() == "test_bot_token"
        assert config.amvera.token.get_secret_value() == "test_amvera_token"
        assert config.mcp.context7_api_key.get_secret_value() == "test_context7_key"


def test_load_config():
    """Тест функции загрузки конфигурации."""
    # Тестируем функцию загрузки конфигурации
    with patch.dict(os.environ, {
        "BOT_TOKEN": "test_bot_token",
        "AMVERA_LLM_TOKEN": "test_amvera_token",
        "CONTEXT7_API_KEY": "test_context7_key"
    }):
        config = load_config()
        
        # Проверяем, что возвращается объект Config
        assert isinstance(config, Config)
        
        # Проверяем значения
        assert config.bot_token.get_secret_value() == "test_bot_token"
        assert config.amvera_llm_token.get_secret_value() == "test_amvera_token"
        assert config.context7_api_key.get_secret_value() == "test_context7_key"