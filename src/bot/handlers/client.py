from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from bot.create_bot import dp, bot

from bot.handlers.start import command_start
from bot.handlers.help import command_help
from bot.handlers.ausweis import command_ausweis
from bot.handlers.instance import command_instance
from bot.handlers.job import command_job
from bot.handlers.kroks import command_kroks
from bot.handlers.zabix import download_document

def register_handler_client(db: Dispatcher):
    #dp.register_message_handler(unknown_message, content_types=['ANY'])
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(command_help, commands=['help'])
    dp.register_message_handler(command_ausweis, commands=['ausweis'], state="*")
    dp.register_message_handler(command_instance, commands=['instance'])
    dp.register_message_handler(command_job, commands=['job'])
    dp.register_message_handler(command_kroks, commands=['kroks'])
    dp.register_message_handler(download_document, content_types=types.ContentType.DOCUMENT)