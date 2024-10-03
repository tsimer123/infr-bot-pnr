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

job = 'kroks-ural|kroks-msk'
noder = 'node_network_receive_bytes_total'
nodet = 'node_network_transmit_bytes_total'
device = 'wwan0'
step = '180'
api = PromqlHttpApi('http://192.1.0.106:12190')
locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")
@dp.message_handler(commands='job')
async def command_job(message: types.Message) -> None: 
    q_time = datetime(datetime.now().year, datetime.now().month, 1)
    q_time1 = datetime(datetime.now().year, datetime.now().month, datetime.now().day)
    q_time2 = datetime.now()
    plt.close('all')
    reqwest = 'node_uname_info{{job=~"{}"}}'.format(job)
    q = api.query(reqwest)
    df5 = q.to_dataframe()

    df2 = prometh(noder, q_time, q_time2)
    df2['sumreceive'] =  round((df2.groupby(['instance'])['diff'].cumsum()/(1024*1024*1024)), 2)
    df2 = df2.groupby(['instance'])['sumreceive'].last()
    df6 = pd.merge(df5, df2, left_on='instance', right_on='instance')
    df7 = df6[['nodename', 'job', 'instance', 'sumreceive']].copy()

    df3 = prometh(nodet, q_time, q_time2)
    df3['sumtransmit'] =  round((df3.groupby(['instance'])['diff'].cumsum()/(1024*1024*1024)), 2)
    df3 = df3.groupby(['instance'])['sumtransmit'].last()
    df8 = pd.merge(df7, df3, left_on='instance', right_on='instance')
    df18 = df8[['nodename', 'job', 'instance', 'sumreceive', 'sumtransmit']].copy()

    df9 = prometh(noder, q_time1, q_time2)
    df9['sumreceivetoday'] =  round((df9.groupby(['instance'])['diff'].cumsum()/(1024*1024*1024)), 2)
    df9 = df9.groupby(['instance'])['sumreceivetoday'].last()
    df11 = pd.merge(df18, df9, left_on='instance', right_on='instance')
    df19 = df11[['nodename', 'job', 'instance', 'sumreceive', 'sumtransmit','sumreceivetoday']].copy()

    df12 = prometh(nodet, q_time1, q_time2)
    df12['sumtransmitoday'] =  round((df12.groupby(['instance'])['diff'].cumsum()/(1024*1024*1024)), 2)
    df12 = df12.groupby(['instance'])['sumtransmitoday'].last()
    df14 = pd.merge(df19, df12, left_on='instance', right_on='instance')
    df20 = df14[['nodename', 'job', 'instance', 'sumreceive', 'sumtransmit', 'sumreceivetoday', 'sumtransmitoday']].copy()
    df20['sumtoday'] = round(df20[['sumreceivetoday','sumtransmitoday']].sum(axis=1), 2)

    df20 = df20.sort_values('nodename')
    df15 = df20[['nodename', 'sumreceive', 'sumtransmit', 'sumtoday']].copy()
    df15 = df15.sort_values('nodename')
    
    fig, ax = plt.subplots()
    fig.patch.set_visible(False)
    table = ax.table(cellText=df15.values, colLabels=df15.columns, loc='center')
    table.set_fontsize(22)
    table.scale(1,2)
    ax.axis('off')
    ax.axis('tight')
    fig.tight_layout()
    b = BytesIO()
    plt.savefig(b, format='jpg')
    b.seek(0)
    media = types.MediaGroup()
    media.attach_photo(b, 'Суммарный трафик приема и передачи в GB с начала месяца')
    await message.reply_media_group(media=media)
    
    filename = "prometheus {}.xlsx".format(datetime.now().strftime("%d.%m.%y"))
    await bot.send_document(message.chat.id, (filename, fit(df20)))

def prometh (node, time1, time2):
    reqwest = '{} {{device="{}", job=~"{}"}}'.format(node, device, job)
    q = api.query_range(reqwest, time1, time2, step)
    df = q.to_dataframe()
    df.dropna()
    df = df.astype({"value": "Int64"})
    df["date"] = pd.to_datetime(df["timestamp"] + 10800, unit="s")
    df1 = df.copy()
    df1 = df1.drop_duplicates (subset=['instance'])
    for inst in df1['instance']:
        df.loc[((df['instance'] == inst)), 'diff'] = df["value"] - df.shift(1)["value"]
    df["diff"] = df["diff"].fillna(0)
    df.loc[df['diff'] <0, 'diff'] = df["value"]   
    return df

def fit (df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Лист1')
    workbook = writer.book
    worksheet = writer.sheets['Лист1']
    worksheet.autofit()
    (max_row, max_col) = df.shape
    column_settings = [{'header': column} for column in df.columns]
    worksheet.add_table(0, 0, max_row, max_col - 1, {'columns': column_settings, 'style': 'Table Style Medium 11' })
    workbook.close()
    document = output.getvalue()
    return document