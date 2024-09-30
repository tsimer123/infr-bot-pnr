import asyncio
import aiogram.utils.markdown as md
from aiogram import types
from bot.create_bot import dp, bot
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
from services.command_start import start_user
from services.log import write_log
from services.render_replay_str import print_format_log_cmd

class Form(StatesGroup):
    choice = State()
    file = State()

list = ['Статистика УСПД Нартис', 'Топология Гермес', 'МРСК Центр']
list2 = ['Иваново', 'Липецк', 'НиНо', 'Смоленск', 'Тамбов']
@dp.message_handler(commands='ausweis')
async def command_ausweis(message: types.Message, state: FSMContext):
    message_text = str(message.text)
    list_param_log_cmd = [0, 0, message.from_user.id, message.from_user.mention, message.from_user.full_name]
    try:
        list_param_log_cmd[0] = start_user(message.from_user.id, message.from_user.mention, message.from_user.full_name)
        list_param_log_cmd[1] = write_log(start_user(message.from_user.id, message.from_user.mention, message.from_user.full_name), 'input', message_text)
        print_format_log_cmd(list_param_log_cmd, 'in', message_text)
    except Exception as ex:
        print_format_log_cmd(list_param_log_cmd, 'err', ex.args[0])
        await message.reply('Ошибка Базы Данных (code error: 1003).\n Обратитесь к Администратору @etsimerman')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(*list)
    await message.reply("Выберете раздел", reply_markup=markup)
    await Form.choice.set()
    await asyncio.sleep(3600)
    current_state = await state.get_state()
    if current_state is None:
        return
    message_text = "таймаут"
    list_param_log_cmd = [0, 0, message.from_user.id, message.from_user.mention, message.from_user.full_name]
    list_param_log_cmd[0] = start_user(message.from_user.id, message.from_user.mention, message.from_user.full_name)
    list_param_log_cmd[1] = write_log(start_user(message.from_user.id, message.from_user.mention, message.from_user.full_name), 'input', message_text)
    textout = """Отменено по таймауту на состояние {current_st}"""
    textout = textout.format(current_st=current_state)
    print_format_log_cmd(list_param_log_cmd, 'in', textout)
    await state.finish()
    await message.reply('Отменено по таймауту', reply_markup=types.ReplyKeyboardRemove())
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(lambda msg: msg.text.lower() == 'отмена', state="*")
async def command_cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    message_text = str(message.text)
    list_param_log_cmd = [0, 0, message.from_user.id, message.from_user.mention, message.from_user.full_name]
    list_param_log_cmd[0] = start_user(message.from_user.id, message.from_user.mention, message.from_user.full_name)
    list_param_log_cmd[1] = write_log(start_user(message.from_user.id, message.from_user.mention, message.from_user.full_name), 'input', message_text)
    textout = """Отменено на состояние {current_st}"""
    textout = textout.format(current_st=current_state)
    print_format_log_cmd(list_param_log_cmd, 'in', textout)
    await state.finish()
    await message.reply('Отменено', reply_markup=types.ReplyKeyboardRemove())
@dp.message_handler(state=Form.choice) 
@dp.message_handler(lambda message: message.text in list, state=Form.choice)
async def process_choice(message: types.Message, state: FSMContext):
    if (message.text not in list) and (message.text not in list2):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add(*list)
        return await message.reply("Плохой выбор. Выберите из списка.", reply_markup=markup)
    if message.text == 'МРСК Центр':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add(*list2)
        return await message.reply("Выберите регион из списка.", reply_markup=markup)
    async with state.proxy() as data:
        data['src'] = message.text
    await Form.next()
    await message.reply('Ok', reply_markup=types.ReplyKeyboardRemove())
    await message.reply("Пришлите файлы \n - Для выхода из режима отправки файлов отправьте команду /cancel или слово - отмена")
@dp.message_handler(state=Form.file)    
@dp.message_handler(content_types=['document'], state=Form.file)
async def download_ausweis(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if data['src'] == 'Статистика УСПД Нартис': src = 'C:/temp/received/1/' + message.document.file_name
        if data['src'] == 'Топология Гермес': src = 'C:/temp/received/2/' + message.document.file_name
        if data['src'] == 'Иваново': src = 'C:/temp/received/3/' + message.document.file_name
        if data['src'] == 'Липецк': src = 'C:/temp/received/4/' + message.document.file_name
        if data['src'] == 'НиНо': src = 'C:/temp/received/5/' + message.document.file_name
        if data['src'] == 'Смоленск': src = 'C:/temp/received/6/' + message.document.file_name
        if data['src'] == 'Тамбов': src = 'C:/temp/received/7/' + message.document.file_name
    await message.document.download(src)
    await message.reply(f"<b>Сохранено</b>", parse_mode = 'HTML')