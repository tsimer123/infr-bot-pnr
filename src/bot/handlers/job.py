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
@dp.message_handler(commands='job')
async def command_job(message: types.Message) -> None:
    locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")
    plt.close('all')
    job = 'kroks-ural|kroks-msk'
    reqwest = 'node_uname_info{{job=~"{}"}}'.format(job)
    q = api.query(reqwest)
    df5 = q.to_dataframe()
    noder = 'node_network_receive_bytes_total'
    nodet = 'node_network_transmit_bytes_total'
    q_time = datetime.now()
    q_time1 = datetime(datetime.now().year, datetime.now().month, 1)
    device = 'wwan0'
    step = '1200'
    job = 'kroks-ural|kroks-msk'

    reqwest = '{} {{device="{}", job=~"{}"}}'.format(noder, device, job)
    q = api.query_range(reqwest, q_time1, q_time , step)
    df3 = q.to_dataframe()
    df3.dropna()
    df3 = df3.astype({"value": "Int64"})
    df3["date"] = pd.to_datetime(df3["timestamp"] + 10800, unit="s")
    df1 = df3.copy()
    df1 = df1.drop_duplicates (subset=['instance'])
    for inst in df1['instance']:
        df3.loc[((df3['instance'] == inst)), 'diff'] = df3["value"] - df3.shift(1)["value"]
    df3["diff"] = df3["diff"].fillna(0)
    df3.loc[df3['diff'] <0, 'diff'] = df3["value"]
    df3['sumreceive'] =  round((df3.groupby(['instance'])['diff'].cumsum()/(1024*1024*1024)), 2)
    df2 = df3.groupby(['instance'])['sumreceive'].last()
    df6 = pd.merge(df5, df2, left_on='instance', right_on='instance')
    df7 = df6[['nodename', 'job', 'instance', 'sumreceive']].copy()

    reqwest = '{} {{device="{}", job=~"{}"}}'.format(nodet, device, job)
    q = api.query_range(reqwest, q_time1, q_time , step)
    df3 = q.to_dataframe()
    df3.dropna()
    df3 = df3.astype({"value": "Int64"})
    df3["date"] = pd.to_datetime(df3["timestamp"] + 10800, unit="s")
    df1 = df3.copy()
    df1 = df1.drop_duplicates (subset=['instance'])
    for inst in df1['instance']:
        df3.loc[((df3['instance'] == inst)), 'diff'] = df3["value"] - df3.shift(1)["value"]
    df3["diff"] = df3["diff"].fillna(0)
    df3.loc[df3['diff'] <0, 'diff'] = df3["value"]
    df3['sumtransmit'] =  round((df3.groupby(['instance'])['diff'].cumsum()/(1024*1024*1024)), 2)
    df2 = df3.groupby(['instance'])['sumtransmit'].last()
    df4 = pd.merge(df7, df2, left_on='instance', right_on='instance')
    df5 = df4[['nodename', 'sumreceive', 'sumtransmit']].copy()

    fig, ax = plt.subplots()
    fig.patch.set_visible(False)
    table = ax.table(cellText=df5.values, colLabels=df5.columns, loc='center')
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
    await bot.send_document(message.chat.id, (filename, fit(df4)))

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