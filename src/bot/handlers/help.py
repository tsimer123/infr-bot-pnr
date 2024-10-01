import sys
from aiogram import types
from pathlib import Path

from services.command_start import start_user
from services.log import write_log
from services.render_replay_str import print_format_log_cmd

async def command_help(message: types.Message):
    id_user_tg = message.from_user.id
    full_name = message.from_user.full_name
    tg_name = message.from_user.mention
    message_text = str(message.text)

    list_param_log_cmd = [0, 0, id_user_tg, tg_name, full_name]
    
    list_help = []
    str_help = ''

    try:
        users_id_db = start_user(id_user_tg, tg_name, full_name)

        log_id_db = write_log(users_id_db, 'input', message_text)

        list_param_log_cmd[0] = users_id_db
        list_param_log_cmd[1] = log_id_db 
            
        print_format_log_cmd(list_param_log_cmd, 'in', message_text)

        app_dir = Path(sys.argv[0]).parent
        name_f = "help.html"
        path_to_file_help = Path(app_dir, name_f)

        with open(path_to_file_help, 'r', encoding='utf8') as f_help:
            list_help = f_help.readlines()
        for line_f in list_help:
            str_help += line_f
        # await message.reply(str_help, parse_mode="MarkdownV2")
        
        await message.reply(str_help, parse_mode=types.ParseMode.HTML)
        print_format_log_cmd(list_param_log_cmd, 'out', 'ok')
        log_id_db = write_log(users_id_db, 'output', 'ok')
    except Exception as ex:
        print_format_log_cmd(list_param_log_cmd, 'err', ex.args[0])
        await message.reply('Ошибка Базы Данных (code error: 1003).\nОбратитесь к Администратору @etsimerman')
        
        