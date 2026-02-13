import pytest
from unittest.mock import patch, AsyncMock, MagicMock

from src.bot.main import on_startup, on_shutdown, main
from src.bot.config import Config


@pytest.mark.asyncio
async def test_on_startup():
    """Тест обработчика запуска бота."""
    # Создаем моки для диспетчера, бота и конфигурации
    dispatcher = MagicMock()
    bot = MagicMock()
    config = Config(
        bot_token="test_token",
        amvera_llm_token="test_amvera_token",
        context7_api_key="test_context7_key"
    )
    
    # Проверяем, что функция не вызывает исключений
    await on_startup(dispatcher, bot, config)
    
    # Проверяем, что logging.info был вызван
    with patch("src.bot.main.logging") as mock_logging:
        await on_startup(dispatcher, bot, config)
        mock_logging.info.assert_called_once_with("Бот запущен")


@pytest.mark.asyncio
async def test_on_shutdown():
    """Тест обработчика остановки бота."""
    # Создаем моки для диспетчера и бота
    dispatcher = MagicMock()
    bot = MagicMock()
    
    # Настраиваем моки
    dispatcher.fsm.storage.close = AsyncMock()
    bot.session.close = AsyncMock()
    
    # Проверяем, что функция не вызывает исключений
    await on_shutdown(dispatcher, bot)
    
    # Проверяем, что logging.info был вызван
    with patch("src.bot.main.logging") as mock_logging:
        await on_shutdown(dispatcher, bot)
        mock_logging.info.assert_called_once_with("Бот остановлен")
    
    # Проверяем, что методы закрытия были вызваны
    dispatcher.fsm.storage.close.assert_called_once()
    bot.session.close.assert_called_once()


@pytest.mark.asyncio
async def test_main():
    """Тест главной функции."""
    # Мокаем все зависимости
    with patch("src.bot.main.load_config") as mock_load_config, \
         patch("src.bot.main.setup_logging") as mock_setup_logging, \
         patch("src.bot.main.Bot") as mock_bot, \
         patch("src.bot.main.Dispatcher") as mock_dispatcher, \
         patch("src.bot.main.setup_routers") as mock_setup_routers, \
         patch("src.bot.main.on_shutdown") as mock_on_shutdown, \
         patch("src.bot.main.asyncio") as mock_asyncio:
        
        # Настраиваем моки
        config = Config(
            bot_token="test_token",
            amvera_llm_token="test_amvera_token",
            context7_api_key="test_context7_key"
        )
        mock_load_config.return_value = config
        
        bot_instance = MagicMock()
        mock_bot.return_value = bot_instance
        
        dp_instance = MagicMock()
        mock_dispatcher.return_value = dp_instance
        
        router_instance = MagicMock()
        mock_setup_routers.return_value = router_instance
        
        # Вызываем тестируемую функцию
        await main()
        
        # Проверяем, что все зависимости были вызваны
        mock_load_config.assert_called_once()
        mock_setup_logging.assert_called_once_with(config)
        mock_bot.assert_called_once_with(token=config.bot_token.get_secret_value())
        mock_dispatcher.assert_called_once()
        dp_instance.include_router.assert_called_once_with(router_instance)
        dp_instance.startup.register.assert_called_once_with(on_startup)
        dp_instance.shutdown.register.assert_called_once_with(on_shutdown)
        dp_instance.start_polling.assert_called_once_with(bot_instance, config=config)
        mock_on_shutdown.assert_called_once_with(dp_instance, bot_instance)