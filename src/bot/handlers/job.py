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
from dotenv import load_dotenv

load_dotenv()
HOST_PROMETHEUS = os.getenv("HOST_PROMETHEUS")
PORT_PROMETHEUS = os.getenv("PORT_PROMETHEUS")
api = PromqlHttpApi(f'http://{HOST_PROMETHEUS}:{PORT_PROMETHEUS}')
job = 'kroks-ural|kroks-msk'
noder = 'node_network_receive_bytes_total'
nodet = 'node_network_transmit_bytes_total'
device = 'wwan0'
step = '720'
locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")
@dp.message_handler(commands='job')
async def command_job(message: types.Message) -> None: 
    q_time = datetime(datetime.now().year, datetime.now().month, 1)
    q_time1 = datetime(datetime.now().year, datetime.now().month, datetime.now().day)
    q_time2 = datetime.now()
    plt.close('all')
    reqwest = 'node_uname_info{{job=~"{}"}}'.format(job)
    q = api.query(reqwest)
    df1 = q.to_dataframe()
    df3 = pd.DataFrame(columns=['timestamp', '__name__', 'device', 'instance', 'job', 'value', 'date', 'diff'])
    df5 = pd.DataFrame(columns=['timestamp', '__name__', 'device', 'instance', 'job', 'value', 'date', 'diff'])
    df7 = pd.DataFrame(columns=['timestamp', '__name__', 'device', 'instance', 'job', 'value', 'date', 'diff'])
    df9 = pd.DataFrame(columns=['timestamp', '__name__', 'device', 'instance', 'job', 'value', 'date', 'diff'])
    for inst in df1['instance']:
        df2 = prometh(noder, q_time, q_time2, inst)
        df3 = (df2.copy() if df3.empty else pd.concat([df3, df2], ignore_index=True))
        df4 = prometh(nodet, q_time, q_time2, inst)
        df5 = (df4.copy() if df5.empty else pd.concat([df5, df4], ignore_index=True))
        df6 = prometh(noder, q_time1, q_time2, inst)
        df7 = (df6.copy() if df7.empty else pd.concat([df7, df6], ignore_index=True))
        df8 = prometh(nodet, q_time1, q_time2, inst)
        df9 = (df8.copy() if df9.empty else pd.concat([df9, df8], ignore_index=True))
    df3['sumreceive'] =  round((df3.groupby(['instance'])['diff'].cumsum()/(1024*1024*1024)), 2)
    df3 = df3.groupby(['instance'])['sumreceive'].last()
    df10 = pd.merge(df1, df3, left_on='instance', right_on='instance')
    df11 = df10[['nodename', 'job', 'instance', 'sumreceive']].copy()
   
    df5['sumtransmit'] =  round((df5.groupby(['instance'])['diff'].cumsum()/(1024*1024*1024)), 2)
    df5 = df5.groupby(['instance'])['sumtransmit'].last()
    df12 = pd.merge(df11, df5, left_on='instance', right_on='instance')
    df13 = df12[['nodename', 'job', 'instance', 'sumreceive', 'sumtransmit']].copy()

    df7['sumreceivetoday'] =  round((df7.groupby(['instance'])['diff'].cumsum()/(1024*1024*1024)), 2)
    df7 = df7.groupby(['instance'])['sumreceivetoday'].last()
    df14 = pd.merge(df13, df7, left_on='instance', right_on='instance')
    df15 = df14[['nodename', 'job', 'instance', 'sumreceive', 'sumtransmit','sumreceivetoday']].copy()

    df9['sumtransmitoday'] =  round((df9.groupby(['instance'])['diff'].cumsum()/(1024*1024*1024)), 2)
    df9 = df9.groupby(['instance'])['sumtransmitoday'].last()
    df16 = pd.merge(df15, df9, left_on='instance', right_on='instance')
    df17 = df16[['nodename', 'job', 'instance', 'sumreceive', 'sumtransmit', 'sumreceivetoday', 'sumtransmitoday']].copy()
    df17['sumtoday'] = round(df17[['sumreceivetoday','sumtransmitoday']].sum(axis=1), 2)

    df17 = df17.sort_values('nodename')
    df18 = df17[['nodename', 'sumreceive', 'sumtransmit', 'sumtoday']].copy()
    df18 = df18.sort_values('nodename')
    
    fig, ax = plt.subplots()
    fig.patch.set_visible(False)
    table = ax.table(cellText=df18.values, colLabels=df18.columns, loc='center')
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
    await bot.send_document(message.chat.id, (filename, fit(df17)))
    
def prometh (node, time1, time2, instance):
    reqwest = '{} {{device="{}", instance="{}", job=~"{}"}}'.format(node, device, instance, job)
    q2 = api.query_range(reqwest, time1, time2, step)
    df = q2.to_dataframe()
    df.dropna()
    df = df.astype({"value": "Int64"})
    df["date"] = pd.to_datetime(df["timestamp"] + 10800, unit="s")
    df['diff'] = df["value"] - df["value"].shift(1)
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