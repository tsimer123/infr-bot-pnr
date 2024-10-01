import sys
from aiogram import types
from datetime import datetime

from bot.create_bot import bot
from services.command_start import start_user
from services.log import write_log
from services.render_replay_str import print_format_log_cmd

async def command_start(message: types.Message):
    try:
        id_user_tg = message.from_user.id
        full_name = message.from_user.full_name
        tg_name = message.from_user.mention
        message_text = str(message.text)

        list_param_log_cmd = [0, 0, id_user_tg, tg_name, full_name]

        try:        
            users_id_db = start_user(id_user_tg, tg_name, full_name)      

            log_id_db = write_log(users_id_db, 'input', '/start')

            list_param_log_cmd[0] = users_id_db
            list_param_log_cmd[1] = log_id_db
        
            print_format_log_cmd(list_param_log_cmd, 'in', message_text)            
            
            await bot.send_message(message.from_user.id, 'Добро пожаловать, ' + " " + str(full_name)\
                                   + ", предлагаем ознакомиться с возможностями Бота, отправив ему команду /help")
            log_id_db = write_log(users_id_db, 'input', 'ok')
            await message.delete()
        except Exception as ex:
            print(str(datetime.now()) + ' ' + str(ex.args[0]), file=sys.stderr)
            await bot.send_message(message.from_user.id, 'Ошибка Базы Данных (code error: 1003).\nОбратитесь к Администратору @etsimerman')
            
    except:
        await message.reply('Общение с ботом через ЛС, напишите ему:\nhttps://t.me/SEK_ADPU_bot')
        