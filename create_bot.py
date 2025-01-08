import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from decouple import config
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger

# from db_handler.db_class import PostgresHandler

# pg_db = PostgresHandler(config('PG_LINK'))
scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
# admins = [int(admin_id) for admin_id in config('ADMINS').split(',')]

# Удаляем все существующие обработчики
logger.remove()

# Настройка логирования
logger.add(
    sys.stdout,
    level="DEBUG",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> - "
           "<level>{level:^8}</level> - "
           "<cyan>{name}</cyan>:<magenta>{line}</magenta> - "
           "<yellow>{function}</yellow> - "
           "<white>{message}</white> <magenta>{extra[user]:->10}</magenta>",
)
# Конфигурация логгера с дополнительными полями это название полей для примера
logger.configure(extra={"ip": "", "user": ""})
# logger.add(
#     os.path.join(os.path.dirname(os.path.abspath(__file__)), "file.log"),
#     level="ERROR",
#     format="{time:YYYY-MM-DD HH:mm:ss} - {level} - {name}:{line} - {function} - {message} {extra[user]}",
#     rotation="1 day",
#     retention="7 days",
#     backtrace=True,
#     diagnose=True,
# )

# Теперь вы можете использовать logger в других модулях
# Явный экспорт для того что б mypy не ругался

#
bot = Bot(token=config('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

__all__ = ["logger", "bot", "dp", "scheduler"]

if __name__ == '__main__':
    logger.info('Инфо сообщение')
    logger.bind(ip='199.200.03.96', user="Boris").error('С биндов сообщения')
    logger.bind(user="Boris").debug('dssdfs')
    logger.bind(user="Boris").warning('dssdfs')
    logger.bind(user="Boris").critical('dssdfs')
