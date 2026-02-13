import logging
import os
from typing import Any

from src.bot.config import Config


def setup_logging(config: Config) -> None:
    """
    Настройка логирования.

    :param config: Конфигурация приложения.
    """
    # Создаем директорию для логов, если она не существует
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Настройка логирования в файл и в консоль
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(os.path.join(log_dir, "bot.log"), encoding="utf-8"),
            logging.StreamHandler()
        ]
    )