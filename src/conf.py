import os

from dotenv import load_dotenv

load_dotenv()

# conf connect db
username_db = str(os.environ.get('username_db'))
password_db = str(os.environ.get('password_db'))
host_db = str(os.environ.get('host_db'))
port_db = str(os.environ.get('port_db'))
database = str(os.environ.get('database'))

# conf tg bot
TOKEN = str(os.environ.get('TOKEN'))
