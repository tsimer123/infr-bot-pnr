import pandas as pd
import datetime
import locale
from promql_http_api import PromqlHttpApi
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy import select
from datetime import time
from datetime import date, timedelta

api = PromqlHttpApi('http://192.1.0.106:12190')
locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")
conn_string = 'postgresql://postgres:1234@localhost:5432/infr_bot_pnr'
job = 'kroks-ural|kroks-msk'
reqwest = 'node_uname_info{{job=~"{}"}}'.format(job)
q = api.query(reqwest)
df5 = q.to_dataframe()
df5 = df5[['nodename', 'job', 'instance']].copy()
'''
print(df5)
db = create_engine(conn_string)
conn = db.connect() 
df5.to_sql('node_uname_info', con=conn, if_exists='append', index=False)   
conn.commit() 
conn.close() 
'''
noder = "node_network_receive_bytes_total"
nodet = "node_network_transmit_bytes_total"
device = 'wwan0'
step = '60'

def promet (node):
    
    db = create_engine(conn_string)
    conn = db.connect() 
    sql_query = pd.read_sql("SELECT date FROM %s order by date desc limit 1;" % (node), con=conn)
    df = pd.DataFrame(sql_query, columns = ['date'])
    q_time1 = df['date'].values[0]
    q_time1 = pd.to_datetime(q_time1)
    conn.commit() 
    conn.close()
    
    #q_time1 = datetime(datetime.now().year, datetime.now().month-1, 1)
    #q_time1 = datetime(datetime.now().year, datetime.now().month, 1)
    while (q_time1 < datetime.today() - timedelta(days=1)):
        q_time = q_time1 + timedelta(days=1)
        reqwest = '{} {{device="{}", job=~"{}"}}'.format(node, device, job)
        q = api.query_range(reqwest, q_time1, q_time , step)
        df3 = q.to_dataframe()
        df3.dropna()
        df3 = df3.astype({"value": "Int64"})
        df1 = df3.copy()
        df1 = df1.drop_duplicates (subset=['instance'])
        for inst in df1['instance']:
            df3.loc[((df3['instance'] == inst)), 'diff'] = df3["value"] - df3.shift(1)["value"]
        df3["diff"] = df3["diff"].fillna(0)
        df3.loc[df3['diff'] <0, 'diff'] = df3["value"]
        df3['summa'] = df3.groupby(['instance'])['diff'].cumsum()
        df2 = df3.groupby(['instance'])['summa'].last()
        df6 = pd.merge(df5, df2, left_on='instance', right_on='instance')
        q_time2 = q_time - timedelta(seconds = 1)
        df6['date'] = pd.DataFrame([[q_time2]], index=df6.index) 
        db = create_engine(conn_string)
        conn = db.connect() 
        df6.to_sql("%s" % (node), con=conn, if_exists='append', index=False)
        conn.commit() 
        conn.close()
        q_time1 = q_time1 + timedelta(days=1)
    return
promet(noder)
promet(nodet)
