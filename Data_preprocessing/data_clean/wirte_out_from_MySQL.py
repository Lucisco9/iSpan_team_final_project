
import pandas as pd
import pymysql


# connection

host = 'ip address'
user = 'your account'
password = 'your password'
database = 'your DB name'
port = 3306

conn = pymysql.connect(host=host, user=user,
                       password=password, database=database, port=port)


query = '''
你要查詢的條件
'''
# 執行查詢並讀取到 DataFrame
df = pd.read_sql(query, conn)

dest = '/Users/lucy/BDSE30MP/'
# dest_folder='C:/Users/student/Main_P/'
# 將 DataFrame 保存為 CSV
df.to_csv(f'{dest}with_CAMERA_by_month.csv', encoding='utf-8', index=False)

conn.close()
