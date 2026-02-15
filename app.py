import asyncio
import logging
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from src.bot.config import load_config
from src.bot.routers import setup_routers
from src.bot.utils.logging import setup_logging

# Загрузка конфигурации
config = load_config()

# Настройка логирования
setup_logging(config)

# Получение путей из конфигурации
WEBHOOK_HOST = config.webhook_host
WEBHOOK_PORT = config.webhook_port
WEBHOOK_PATH = config.webhook_path
WEBHOOK_SECRET = config.webhook_secret if config.webhook_secret else None

# URL вебхука (для HTTPS используем порт 443, не включаем его в URL)
if WEBHOOK_PORT == 443:
    WEBHOOK_URL = f"https://{WEBHOOK_HOST}{WEBHOOK_PATH}"
else:
    WEBHOOK_URL = f"https://{WEBHOOK_HOST}:{WEBHOOK_PORT}{WEBHOOK_PATH}"

# Создание бота и диспетчера
bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()

# Регистрация роутеров
dp.include_router(setup_routers())


async def on_startup():
    """Действия при запуске приложения."""
    logging.info("Запуск приложения")
    
    # Установка вебхука
    await bot.set_webhook(
        url=WEBHOOK_URL,
        secret_token=WEBHOOK_SECRET
    )
    logging.info(f"Вебхук установлен: {WEBHOOK_URL}")


async def on_shutdown():
    """Действия при остановке приложения."""
    logging.info("Остановка приложения")
    
    # Удаление вебхука
    await bot.delete_webhook()
    logging.info("Вебхук удален")


def main():
    """Главная функция для запуска веб-сервера."""
    # Регистрация обработчиков событий
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    # Создание веб-приложения
    app = web.Application()
    
    # Создание обработчика запросов
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=WEBHOOK_SECRET,
    )
    
    # Регистрация обработчика в приложении
    app.router.add_route("*", WEBHOOK_PATH, webhook_requests_handler.handle)
    
    # Установка приложения в обработчик
    setup_application(app, dp, bot=bot)
    
    # Запуск веб-сервера
    web.run_app(app, host=WEBHOOK_HOST, port=WEBHOOK_PORT)


if __name__ == "__main__":
    main()