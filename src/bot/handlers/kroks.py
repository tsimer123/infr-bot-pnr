import os
import json
import pandas as pd
from dotenv import load_dotenv
import datetime
import locale
#from sqlalchemy import create_engine
from datetime import datetime
from io import BytesIO
from aiogram import types
from bot.create_bot import dp, bot
from sql.engine import engine

#load_dotenv()
#username_db = os.getenv("username_db")
#password_db = os.getenv("password_db")
#host_db = os.getenv("host_db")
#port_db = os.getenv("port_db")
#database = os.getenv("database")
#locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")

db = engine
@dp.message_handler(commands='kroks')
async def command_kroks(message: types.Message) -> None: 
    timestart = datetime(datetime.now().year, datetime.now().month, 1)
    timestartday = datetime(datetime.now().year, datetime.now().month, datetime.now().day)
    timestop = datetime.now()
    #conn_string = (f'postgresql+psycopg2://{username_db}:{password_db}@{host_db}:{port_db}/{database}')
    #db = create_engine(conn_string)
    conn = db.connect()
    sql_query = pd.read_sql(f"SELECT iccid, nodename, instance, COALESCE(imei) as imei, COALESCE(sim1) as sim1, COALESCE(sim2) as sim2, MAX(summa) as summa, MIN(date) as mindate, MAX(date) as maxdate FROM kroks_network_bytes_sum WHERE date BETWEEN '{timestart}' and '{timestop}' GROUP BY iccid, nodename, instance, imei, sim1, sim2 ORDER BY instance, mindate;", con=conn)
    df = pd.DataFrame(sql_query, columns = ['iccid', 'nodename', 'instance', 'imei', 'sim1', 'sim2', 'summa', 'mindate', 'maxdate'])
    sql_query = pd.read_sql(f"SELECT iccid, nodename, instance, COALESCE(imei) as imei, COALESCE(sim1) as sim1, COALESCE(sim2) as sim2, (MAX(summa)-MIN(summa)) as summa, MIN(date) as mindate, MAX(date) as maxdate FROM kroks_network_bytes_sum WHERE date BETWEEN '{timestartday}' and '{timestop}' GROUP BY iccid, nodename, instance, imei, sim1, sim2 ORDER BY instance, mindate;", con=conn)
    df2 = pd.DataFrame(sql_query, columns = ['iccid', 'nodename', 'instance', 'imei', 'sim1', 'sim2', 'summa', 'mindate', 'maxdate'])
    conn.close()
    filename = "kroks {}.xlsx".format(datetime.now().strftime("%d.%m.%y"))
    await bot.send_document(message.chat.id, (filename, fit(df, df2)))

def fit (df, df2):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Месяц')
    workbook = writer.book
    worksheet = writer.sheets['Месяц']
    worksheet.autofit()
    (max_row, max_col) = df.shape
    column_settings = [{'header': column} for column in df.columns]
    worksheet.add_table(0, 0, max_row, max_col - 1, {'columns': column_settings, 'style': 'Table Style Medium 11' })
    df2.to_excel(writer, index=False, sheet_name='День')
    worksheet = writer.sheets['День']
    worksheet.autofit()
    (max_row, max_col) = df2.shape
    column_settings = [{'header': column} for column in df2.columns]
    worksheet.add_table(0, 0, max_row, max_col - 1, {'columns': column_settings, 'style': 'Table Style Medium 11' })
    workbook.close()
    document = output.getvalue()
    return document