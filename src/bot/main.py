import asyncio
import logging

from aiogram import Bot, Dispatcher

from src.bot.config import Config, load_config
from src.bot.routers import setup_routers
from src.bot.utils.logging import setup_logging


async def on_startup(dispatcher: Dispatcher, bot: Bot, config: Config) -> None:
    """
    Действия при запуске бота.

    :param dispatcher: Диспетчер бота.
    :param bot: Бот.
    :param config: Конфигурация бота.
    """
    logging.info("Бот запущен")


async def on_shutdown(dispatcher: Dispatcher, bot: Bot) -> None:
    """
    Действия при остановке бота.

    :param dispatcher: Диспетчер бота.
    :param bot: Бот.
    """
    logging.info("Бот остановлен")
    await dispatcher.fsm.storage.close()
    await bot.session.close()


async def main() -> None:
    """Главная функция для запуска бота."""
    # Загрузка конфигурации
    config = load_config()

    # Настройка логирования
    setup_logging(config)

    # Создание бота и диспетчера
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()

    # Регистрация роутеров
    dp.include_router(setup_routers())

    # Регистрация обработчиков событий
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    # Запуск бота
    try:
        await dp.start_polling(bot, config=config)
    finally:
        await on_shutdown(dp, bot)


if __name__ == "__main__":
    asyncio.run(main())