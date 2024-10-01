import pandas as pd
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import calendar
import locale
import os
from io import BytesIO
from aiogram import types
from promql_http_api import PromqlHttpApi
from datetime import datetime
from bot.create_bot import dp, bot
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

api = PromqlHttpApi('http://192.1.0.106:12190')
job = 'kroks-ural|kroks-msk'
reqwest = 'node_uname_info{{job=~"{}"}}'.format(job)
q = api.query(reqwest)
df = q.to_dataframe()
df['kroks'] = df['nodename'] + " " + df['job'] + " " + df['instance']
df1 = df['kroks']
listdf = df1.values
@dp.message_handler(commands='instance')
async def command_instance(message: types.Message) -> None:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(*listdf)
    await message.reply("Выберете оборудование", reply_markup=markup)
@dp.message_handler(lambda message: message.text in listdf)
async def process_en(message: types.Message):
    if message.text in listdf:
        parts = (message.text).split()
        nodename = parts[0]
        parts2 = parts[2].split(':')
        instance = parts2[0]
        media = []
        locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")
        q_time = datetime.now()
        q_time1 = datetime(datetime.now().year, datetime.now().month, 1)
        device = 'wwan0'
        step = '1200'
        media = types.MediaGroup()
        noder = 'node_network_receive_bytes_total'
        reqwest = '{} {{device="{}", instance="{}:9100"}}'.format(noder, device, instance)
        q = api.query_range(reqwest, q_time1, q_time , step)
        media.attach_photo(graf(q, nodename, noder), 'receive_bytes')
        nodet = 'node_network_transmit_bytes_total'
        reqwest = '{} {{device="{}", instance="{}:9100"}}'.format(nodet, device, instance)
        q = api.query_range(reqwest, q_time1, q_time , step)
        media.attach_photo(graf(q, nodename, nodet), 'transmit_bytes')
        await message.reply('Ok', reply_markup=types.ReplyKeyboardRemove())
        await message.reply_media_group(media=media)

def graf (q, nodename, node):
    plt.close('all')
    df = q.to_dataframe()
    df = df.astype({"value": "Int64"})
    df["diff"] = df["value"] - df.shift(1)["value"]
    df["diff"] = df["diff"].fillna(0)
    df.loc[df['diff'] <0, 'diff'] = df["value"]
    traffic = df['diff'].sum()/1024/1024/1024
    df["date"] = pd.to_datetime(df["timestamp"] + 10800, unit="s")
    fig = plt.figure()
    fig.autofmt_xdate()
    ax = fig.add_subplot(111)
    month = calendar.month_name[datetime.now().month]
    label=nodename
    ax.plot(df['date'], df['diff']/1024/1024/1024, label=label)
    ax.xaxis.set(
    minor_locator=mdates.DayLocator(interval=2),
    minor_formatter=mdates.DateFormatter('%d'),    
    major_locator=mdates.MonthLocator(),            
    major_formatter=mdates.DateFormatter('%d')
    )
    title = '{} wwan0'.format(node)
    plt.title(title)
    plt.ylabel('GBytes')
    plt.xlabel(month)
    plt.legend(loc="upper right")
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    textstr = '$\sum traffic=%.0f$ GB'%(traffic)
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=10, verticalalignment='top', bbox=props)
    b = BytesIO()
    plt.savefig(b, format='jpg')
    b.seek(0)
    return b