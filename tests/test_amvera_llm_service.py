import pytest
import asyncio
from unittest.mock import patch, AsyncMock
import aiohttp

from src.bot.services.amvera_llm import AmveraLLMService
from src.bot.config import Config


@pytest.fixture
def config():
    """Фикстура для создания конфигурации."""
    return Config(
        bot_token="test_token",
        amvera_llm_token="test_amvera_token",
        context7_api_key="test_context7_key"
    )


@pytest.mark.asyncio
async def test_amvera_llm_service_get_response_success(config):
    """Тест успешного получения ответа от Amvera LLM."""
    service = AmveraLLMService(config)
    
    # Мокаем aiohttp.ClientSession
    with patch("aiohttp.ClientSession.post") as mock_post:
        # Создаем мок-ответ
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={
            "choices": [{
                "message": {
                    "content": "Привет, человек!"
                }
            }]
        })
        
        # Настраиваем контекстный менеджер
        mock_post.return_value.__aenter__.return_value = mock_response
        mock_post.return_value.__aexit__.return_value = None
        
        # Получаем ответ
        response = await service.get_response("Привет, ИИ!")
        
        # Проверяем результат
        assert response == "Привет, человек!"


@pytest.mark.asyncio
async def test_amvera_llm_service_get_response_error(config):
    """Тест обработки ошибки от Amvera LLM."""
    service = AmveraLLMService(config)
    
    # Мокаем aiohttp.ClientSession
    with patch("aiohttp.ClientSession.post") as mock_post:
        # Создаем мок-ответ с ошибкой
        mock_response = AsyncMock()
        mock_response.status = 500
        mock_response.text = AsyncMock(return_value="Internal Server Error")
        
        # Настраиваем контекстный менеджер
        mock_post.return_value.__aenter__.return_value = mock_response
        mock_post.return_value.__aexit__.return_value = None
        
        # Получаем ответ
        response = await service.get_response("Привет, ИИ!")
        
        # Проверяем результат
        assert response is None


@pytest.mark.asyncio
async def test_amvera_llm_service_get_response_timeout(config):
    """Тест обработки timeout при обращении к Amvera LLM."""
    service = AmveraLLMService(config)
    
    # Мокаем aiohttp.ClientSession
    with patch("aiohttp.ClientSession.post") as mock_post:
        # Настраиваем мок для выброса исключения
        mock_post.side_effect = asyncio.TimeoutError()
        
        # Получаем ответ
        response = await service.get_response("Привет, ИИ!")
        
        # Проверяем результат
        assert response is None


@pytest.mark.asyncio
async def test_amvera_llm_service_get_response_exception(config):
    """Тест обработки исключения при обращении к Amvera LLM."""
    service = AmveraLLMService(config)
    
    # Мокаем aiohttp.ClientSession
    with patch("aiohttp.ClientSession.post") as mock_post:
        # Настраиваем мок для выброса исключения
        mock_post.side_effect = Exception("Network error")
        
        # Получаем ответ
        response = await service.get_response("Привет, ИИ!")
        
        # Проверяем результат
        assert response is None
