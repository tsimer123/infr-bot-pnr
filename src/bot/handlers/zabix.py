import pandas as pd
import ipaddress 
from io import BytesIO
from aiogram import types
from bot.create_bot import dp, bot

async def download_document(message: types.Message) -> None:
    output = BytesIO()
    await message.document.download(destination = output)
    df = pd.read_excel(output, dtype=object)
    if df.columns[0] == 'Ip':
        try:
            for ip in df['Ip']:
                ip = ipaddress.IPv4Address(ip)
            df['Порты'] = df['Порты'][0].astype(str)
            df['Порты'] = (df['Порты'][0]).replace(' ', '')
            df.ffill(inplace=True)
            df['Шаблон'] = df['Шаблон'].astype(int)
            df['Статус'] = df['Статус'].astype(int)
            df.loc[df['Имя'] != '', 'Имя'] = df['Имя'].values[0] + df.index
            df['Имя'] = df['Имя'].astype(int)
            df3 = pd.DataFrame(columns=['Ip', 'Шаблон', 'Статус'])
            df4 = pd.DataFrame(columns=['Ip', 'Шаблон', 'Статус', 'item'])
            df2 = df[['Ip', 'Шаблон', 'Статус']].copy()
            (max_row2, max_col2) = df2.shape
            for port in (df['Порты'][0]).split(','):
                df3 = df2.copy()
                df3 = df3.assign(item = port)
                df4 = (df3.copy() if df4.empty else pd.concat([df4, df3], ignore_index=True))
            df4 = df4.reindex(columns=['Ip', 'Шаблон', 'item', 'Статус'])
            df4 = df4.rename(columns={'Ip': 'IP', 'Шаблон': 'ID шаблона (31771 - телнет) / 109464 - оч частый / 88426 моэск', 'item': 'Имя item', 'Статус': 'item status (0 вкл / 1 выкл)'})
            df5 = df.copy()
            df5['Имя'] = df5['Имя'].astype(str)
            df5['Хост'] = df5['Хост1'] + '_' + df5['Хост2'] + '_' + df5['Имя'] + '_' + df5['Ip']
            df5['ИмяхостA'] = df5['Имя1'] + '_' + df5['Имя2'] + '_' + df5['Имя'] + '_' + df5['Ip']
            df5['№ п/п'] = df5.index + 1
            df6 = df5[['№ п/п', 'Хост', 'ИмяхостA', 'Ip']].copy()
            df6 = df6.assign(a = '0')
            df6 = df6.assign(b = '0')
            await bot.send_document(message.chat.id, ('set_item_status.xlsx', fit(max_row2, df, df4)))
            await bot.send_document(message.chat.id, ('import_zabbix.xlsx', fit2(df6)))
        except ValueError:
            text = "Строка {} IP адрес {} с ошибкой".format(df[df['Ip'] == ip].index.item()+2, ip)
            await message.reply(text, parse_mode = 'HTML')

def fit (max_row2, df, df4):
    output3 = BytesIO()
    writer = pd.ExcelWriter(output3, engine='xlsxwriter')
    df4.to_excel(writer, index=False, sheet_name='Лист1')
    workbook = writer.book
    worksheet = writer.sheets['Лист1']
    col=5
    for port in (df['Порты'][0]).split(','):
        worksheet.write(0, col, port)
        worksheet.write(1, col, max_row2)
        col += 1
    worksheet.autofit()
    (max_row, max_col) = df4.shape
    column_settings = [{'header': column} for column in df4.columns]
    worksheet.add_table(0, 0, max_row, max_col - 1, {'columns': column_settings, 'style': 'Table Style Medium 11' })
    workbook.close()
    document = output3.getvalue()
    return document

def fit2 (df6):
    output4 = BytesIO()
    writer = pd.ExcelWriter(output4, engine='xlsxwriter')
    df6.to_excel(writer, index=False, sheet_name='Лист1')
    workbook = writer.book
    worksheet = writer.sheets['Лист1']
    worksheet.autofit()
    (max_row, max_col) = df6.shape
    column_settings = [{'header': column} for column in df6.columns]
    worksheet.add_table(0, 0, max_row, max_col - 1, {'columns': column_settings, 'style': 'Table Style Medium 11' })
    workbook.close()
    document = output4.getvalue()
    return document

