from pprint import pprint

from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message

from keyboards.all_keyboards import main_kb, create_spec_kb, create_rat

start_router = Router()


#
# @start_router.message(CommandStart())
# async def cmd_start(message: Message):
#     pprint(f"ID пользователя {message.from_user.id}")
#     print(f"ID бота {message.bot.id}")
#     # await message.answer('Запуск сообщения по команде /start используя фильтр CommandStart()')
#     await message.answer(f"ID пользователя {message.from_user.id}")
#     await message.answer(f"ID бота {message.bot.id}")
#     await message.answer('Запуск сообщения по команде /start используя фильтр CommandStart()',
#                          reply_markup=main_kb(message.from_user.id))

@start_router.message(CommandStart())
async def cmd_start(message: Message, command: CommandObject):
    """
    https://t.me/tutorial_boriska_bot?start=Xsdfsdf обработка ссылки после start что
    б понять откуда появился пользователь с какого ресурса
    :param message:
    :param command:
    :return:
    """
    command_args: str = command.args
    if command_args:
        await message.answer(
            f'Запуск сообщения по команде /start используя фильтр CommandStart() с меткой <b>{command_args}</b>',
            reply_markup=main_kb(message.from_user.id))
    else:
        await message.answer(
            f'Запуск сообщения по команде /start используя фильтр CommandStart() без метки',
            reply_markup=main_kb(message.from_user.id))


@start_router.message(Command('start_2'))
async def cmd_start_2(message: Message):
    await message.answer('Запуск сообщения по команде /start_2 используя фильтр Command()',
                         reply_markup=create_spec_kb())


@start_router.message(F.text == '/start_3')
async def cmd_start_3(message: Message):
    await message.answer('Запуск сообщения по команде /start_3 используя магический фильтр F.text!',
                         reply_markup=create_rat())
