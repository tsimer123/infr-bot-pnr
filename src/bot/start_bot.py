import sys
from aiogram.utils import executor
from .create_bot import dp
from .handlers import client

def run_bot():


	async def on_startup(_):
		print('Бот вышел в онлайн', file=sys.stderr)

	# from handlers import client, other

	client.register_handler_client(dp)
	# other.register_handler_other(dp)

	executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
