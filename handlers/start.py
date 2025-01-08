import asyncio
from pprint import pprint

from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, CallbackQuery
from aiogram.utils.chat_action import ChatActionSender

from create_bot import questions, bot
from keyboards.all_keyboards import main_kb, create_spec_kb, create_rat
from keyboards.inline_kbs import ease_link_kb, create_qst_inline_kb
from utils.my_utils import get_random_person

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


@start_router.message(F.text == 'Давай инлайн!')
async def get_inline_btn_link(message: Message):
    await message.answer('Вот тебе инлайн клавиатура со ссылками!', reply_markup=ease_link_kb())


@start_router.callback_query(F.data == 'get_person')
async def send_random_person(call: CallbackQuery):
    # это ответ для инлайн кнопки что б перестала мигать может выводить сообщение
    # await call.answer('Генерирую случайного пользователя',show_alert=True)
    await call.answer()
    user = get_random_person()
    formatted_message = (
        f"👤 <b>Имя:</b> {user['name']}\n"
        f"🏠 <b>Адрес:</b> {user['address']}\n"
        f"📧 <b>Email:</b> {user['email']}\n"
        f"📞 <b>Телефон:</b> {user['phone_number']}\n"
        f"🎂 <b>Дата рождения:</b> {user['birth_date']}\n"
        f"🏢 <b>Компания:</b> {user['company']}\n"
        f"💼 <b>Должность:</b> {user['job']}\n"
    )
    await call.message.answer(formatted_message)


@start_router.callback_query(F.data == "back_home")
async def inline_back_home(call: CallbackQuery):
    await call.answer("Вернемся в начало")
    await call.message.answer(text='Назад', reply_markup=main_kb(call.from_user.id))


@start_router.message(Command('faq'))
async def cmd_start_33(message: Message):
    await message.answer('Сообщение с инлайн клавиатурой с вопросами', reply_markup=create_qst_inline_kb(questions))


@start_router.callback_query(F.data.startswith('qst_'))
async def cmd_start_33(call: CallbackQuery):
    await call.answer()
    qst_id = int(call.data.replace('qst_', ''))
    qst_data = questions[qst_id]
    msg_text = f'Ответ на вопрос {qst_data.get("qst")}\n\n' \
               f'<b>{qst_data.get("answer")}</b>\n\n' \
               f'Выбери другой вопрос:'
    async with ChatActionSender(bot=bot, chat_id=call.from_user.id, action="typing"):
        await asyncio.sleep(2)
        await call.message.answer(msg_text, reply_markup=create_qst_inline_kb(questions))
