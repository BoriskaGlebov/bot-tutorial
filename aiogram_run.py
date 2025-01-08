import asyncio

from aiogram.types import BotCommand, BotCommandScopeDefault

from create_bot import bot, dp, scheduler, logger
from handlers.start import start_router


# Функция, которая настроит командное меню (дефолтное для всех пользователей)
async def set_commands():
    """
    BotCommand: объект, используемый для создания команд бота.
    Каждая команда имеет два атрибута: command (имя команды) и
    description (описание команды).

    BotCommandScopeDefault: объект, определяющий область действия команд.
    В данном случае используется область по умолчанию, что означает,
    что команды будут действовать для всех пользователей.
    :return:
    """
    commands = [BotCommand(command='start', description='Старт'),
                BotCommand(command='start_2', description='Старт 2'),
                BotCommand(command='start_3', description='Старт 3'),
                BotCommand(command='faq', description='Частые вопросы')
                ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


# Функция, которая выполнится когда бот запустится
async def start_bot():
    await set_commands()


async def main():
    # регистрация роутеров
    dp.include_router(start_router)
    dp.startup.register(start_bot)

    # запуск бота в режиме long polling при запуске бот очищает все обновления, которые были за его моменты бездействия
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("Bot started")
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        logger.info("Bot stoped")
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
