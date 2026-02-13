from aiogram import Router


def setup_routers() -> Router:
    """
    Регистрация роутеров.

    :return: Роутер.
    """
    from src.bot.routers.chatgpt import chatgpt_router
    from src.bot.routers.echo import echo_router
    from src.bot.routers.help import help_router
    from src.bot.routers.start import start_router

    router = Router()
    router.include_routers(
        start_router,
        help_router,
        chatgpt_router,
        echo_router,
    )
    return router