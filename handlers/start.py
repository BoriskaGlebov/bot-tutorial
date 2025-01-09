import asyncio
import os
from pprint import pprint

from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, FSInputFile, InputMediaVideo, InputMediaPhoto
from aiogram.utils.chat_action import ChatActionSender

from create_bot import questions, bot, admins, logger, all_media_dir
from filters.is_admin import IsAdmin
from keyboards.all_keyboards import main_kb, create_spec_kb, create_rat
from keyboards.inline_kbs import ease_link_kb, create_qst_inline_kb, get_inline_kb
from utils.my_utils import get_random_person
from work_time.time_func import get_msc_date

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
    long_text = (
        "<tg-spoiler>Это длинное сообщение, которое можно развернуть. "
        "Здесь может быть много информации, которая не помещается на экране.</tg-spoiler>"
    )
    await message.answer('Запуск сообщения по команде /start_2 используя фильтр Command()',
                         reply_markup=create_spec_kb())
    await asyncio.sleep(2)
    await message.reply(text='<b>Жирный</b> \n '
                             '<i>Курсив</i> \n'
                             '<u>Подчеркнутый</u> \n'
                             '<s>Зачеркнутый</s> \n'
                             '<tg-spoiler>Спойлер (скрытый текст)</tg-spoiler> \n'
                             '<a href="http://www.example.com/">Ссылка в тексте</a> \n'
                             '<code>Код с копированием текста при клике</code> \n'
                             '<pre>Спойлер с копированием текста</pre> \n', reply_markup=ReplyKeyboardRemove())
    await message.answer(text=long_text)


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


@start_router.message(Command(commands=["settings", "about"]))
async def univers_cmd_handler(message: Message, command: CommandObject):
    command_args: str = command.args
    command_name = 'settings' if 'settings' in message.text else 'about'
    response = f'Была вызвана команда /{command_name}'
    if command_args:
        response += f' с меткой <b>{command_args}</b>'
    else:
        response += ' без метки'
    await message.answer(response)


@start_router.message(F.contact)
async def get_contact(message: Message):
    await bot.send_message(chat_id=message.chat.id, text=f'{message.message_id}')
    await message.answer("Спасибоо за контакт")


@start_router.message(F.text.lower().contains('подписывайся'), IsAdmin(admins))
async def process_find_word(message: Message):
    await message.answer('О, админ, здарова! А тебе можно писать подписывайся.')


@start_router.message(F.text.lower().contains('подписывайся'))
async def process_find_word(message: Message):
    await message.answer('В твоем сообщении было найдено слово "подписывайся", а у нас такое писать запрещено!')


@start_router.message(F.text.lower().contains('охотник'))
async def cmd_start(message: Message, state: FSMContext):
    # отправка обычного сообщения
    await message.answer('Я думаю, что ты тут про радугу рассказываешь')

    # то же действие, но через объект бота
    await bot.send_message(chat_id=message.from_user.id, text='Для меня это слишком просто')

    # ответ через цитату
    msg = await message.reply('Ну вот что за глупости!?')

    # ответ через цитату, через объект bot
    await bot.send_message(chat_id=message.from_user.id, text='Хотя, это забавно...',
                           reply_to_message_id=msg.message_id)

    await bot.forward_message(chat_id=message.from_user.id, from_chat_id=message.from_user.id,
                              message_id=msg.message_id)

    data_task = {'user_id': message.from_user.id, 'full_name': message.from_user.full_name,
                 'username': message.from_user.username, 'message_id': message.message_id,
                 'date': get_msc_date(message.date)}
    logger.info(data_task)


@start_router.message(Command('test_edit_msg'))
async def cmd_start(message: Message, state: FSMContext):
    # Бот делает отправку сообщения с сохранением объекта msg
    msg = await message.answer('Отправляю сообщение')

    # Достаем ID сообщения
    msg_id = msg.message_id

    # Имитируем набор текста 2 секунды и отправляеВ коде оставлены комментарии. Единственное, на что нужно обратить внимание, — строка: м какое - то сообщение
    async with ChatActionSender(bot=bot, chat_id=message.from_user.id, action="typing"):
        await asyncio.sleep(2)
        await message.answer('Новое сообщение')

    # Делаем паузу ещё на 2 секунды
    await asyncio.sleep(2)

    # Изменяем текст сообщения, ID которого мы сохранили
    await bot.edit_message_text(text='<b>Отправляю сообщение!!!</b>', chat_id=message.from_user.id, message_id=msg_id)
    # НЕльзя редактировать сообщения которые сам не отправлял
    # await bot.edit_message_text(text='<b>Отправляю сообщение которое не отправлял!!!</b>', chat_id=message.from_user.id,
    #                             message_id=message.message_id)
    msg = await message.answer('Привет!')
    await asyncio.sleep(2)
    old_text = msg.text
    await msg.delete()
    await message.answer(old_text, reply_markup=main_kb(message.from_user.id))


@start_router.message(Command('test_copy_msg'))
async def cmd_start(message: Message, state: FSMContext):
    new_msg = await bot.copy_message(
        chat_id=message.from_user.id,
        from_chat_id=message.from_user.id,
        message_id=message.message_id
    )
    await asyncio.sleep(2)
    await message.delete()
    await asyncio.sleep(2)
    await bot.edit_message_text(
        text='<b>Отправляю сообщение которое сам же отредактировал хотя не имел доступа!!!</b>',
        chat_id=message.from_user.id,
        message_id=new_msg.message_id
    )


@start_router.message(Command('send_audio'))
async def cmd_start(message: Message, state: FSMContext):
    audio_file = FSInputFile(path=os.path.join(all_media_dir, 'ANNA_ASTI_-_Po_baram_74376135.mp3'))
    msg_id = await message.answer_audio(audio=audio_file, reply_markup=main_kb(message.from_user.id),
                                        caption='Моя <u>отформатированная</u> подпись к <b>файлу</b>')
    print(msg_id.message_id)


@start_router.message(Command('send_photo'))
async def cmd_start(message: Message, state: FSMContext):
    photo_file = FSInputFile(path=os.path.join(all_media_dir, 'babd6d37eb2dd965c7f1dfb516d54094.jpg'))
    msg_id = await message.answer_photo(photo=photo_file, reply_markup=main_kb(message.from_user.id),
                                        caption='Моя <u>отформатированная</u> подпись к <b>фото</b>')
    print(msg_id.photo[-1].file_id)
    print(msg_id.photo)
    await message.answer_photo(
        photo='AgACAgIAAxkDAAIBdWeAIZLFA5EKW5HTvUNh-v-NryinAAKp6jEb6DkBSKX9wFmlJc_eAQADAgADdwADNgQ')

    photo_url = 'https://indirimlerce.com/wp-content/uploads/2023/02/phyton-ile-neler-yapilabilir.jpg'
    msg_id = await message.answer_photo(photo=photo_url, reply_markup=main_kb(message.from_user.id),
                                        caption='Моя <u>отформатированная</u> подпись к <b>фото</b>')
    print(msg_id.photo[-1].file_id)


@start_router.message(Command('send_video'))
async def cmd_start(message: Message, state: FSMContext):
    video_file = FSInputFile(path=os.path.join(all_media_dir, 'hdecfc329_175871.mov'))
    msg = await message.answer_video(video=video_file,
                                     # reply_markup=main_kb(message.from_user.id),
                                     caption='Моя отформатированная подпись к файлу')
    await asyncio.sleep(2)
    await msg.edit_caption(caption='Новое описание к моему видео.')

    await message.answer("ХОБАНА")

    video_file = FSInputFile(path=os.path.join(all_media_dir, 'hdecfc329_175871.mov'))
    msg_1 = await message.answer_video(video=video_file,
                                       caption='Моя <b>отформатированная подпись</b> к файлу')
    await asyncio.sleep(2)
    await msg_1.edit_caption(caption='Новое описание к видео 1')

    await asyncio.sleep(2)
    new_video_file = FSInputFile(path=os.path.join(all_media_dir, 'sample-5s.mp4'))
    await msg_1.edit_media(media=InputMediaVideo(media=new_video_file, caption='Новое видео и у него новое описание.'),
                           reply_markup=get_inline_kb())


@start_router.message(Command('send_voice'))
async def cmd_start(message: Message, state: FSMContext):
    async with ChatActionSender.record_voice(bot=bot, chat_id=message.from_user.id):
        await asyncio.sleep(3)
        await message.answer_voice(voice=FSInputFile(
            path=os.path.join(all_media_dir, 'Korol_i_SHut_-_Lesnik_62571704.mp3')))


@start_router.message(Command('send_video_note'))
async def cmd_start(message: Message, state: FSMContext):
    async with ChatActionSender.record_video_note(bot=bot, chat_id=message.from_user.id):
        await asyncio.sleep(3)
        await message.answer_video_note(
            video_note="DQACAgIAAxkBAAIBkWeAJOHbappknyJQfA4ZlZnGYWkKAAIGawAC6DkBSHpyqaHN42DRNgQ")


@start_router.message(F.video_note)
async def cmd_start(message: Message, state: FSMContext):
    print(message.video_note.file_id)


@start_router.message(Command('send_media_group'))
async def cmd_start(message: Message, state: FSMContext):
    photo_1 = InputMediaPhoto(type='photo',
                              media=FSInputFile(
                                  path=os.path.join(all_media_dir, 'babd6d37eb2dd965c7f1dfb516d54094.jpg')),
                              caption='Описание ко <b>ВСЕЙ</b> медиагруппе')
    photo_2 = InputMediaPhoto(type='photo',
                              media=FSInputFile(
                                  path=os.path.join(all_media_dir, 'lake_mountain_tree_36589_2650x1600.jpg')))
    # photo_3 = InputMediaPhoto(type='photo',
    #                           media=FSInputFile(path=os.path.join(all_media_dir, 'photo_2024-06-05_09-32-15.jpg')))
    video_1 = InputMediaVideo(type='video',
                              media=FSInputFile(path=os.path.join(all_media_dir, 'hdecfc329_175871.mov')))
    # video_3 = InputMediaVideo(type='video',
    #                           media='DQACAgIAAxkBAAIBkWeAJOHbappknyJQfA4ZlZnGYWkKAAIGawAC6DkBSHpyqaHN42DRNgQ'),
    video_2 = InputMediaVideo(type='video',
                              media=FSInputFile(path=os.path.join(all_media_dir, 'sample-5s.mp4')))

    media = [photo_1, photo_2, video_1, video_2]
    await message.answer_media_group(media=media)
