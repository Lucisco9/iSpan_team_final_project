
import pymysql
import pandas as pd
import numpy as np
import os


host = 'ip address'
user = 'your account'
password = 'your password'
database = 'your DB name'
port = 3306

# 建立mysql連線
conn = pymysql.connect(host=host, user=user,
                       password=password, database=database, port=port)

# 指定要寫入的資料庫表名稱
table_name = 'table name'


source_path = "folder name"


for filename in os.listdir(source_path):
    if not filename.endswith('.csv'):
        continue
    df = pd.read_csv(f'{source_path}{filename}',
                     encoding='UTF-8', header=0, index_col=False)


# df_a=pd.read_csv('C:/Users/student/Main_P/CODE/anlysis_model/merged2.csv', encoding='UTF-8')
df_a = pd.read_csv('/Users/lucy/BDSE30MP/weather_clean/臺北市_ALL.csv')

df_a = df_a.drop(['WD', 'WSGust', 'WDGust', 'visb', 'PrecpHour'], axis=1)

# df_b=pd.read_csv('C:/Users/student/Main_P/CODE/anlysis_model/AVG_T_daily_WEATHER.csv', encoding='UTF-8')
df_b = pd.read_csv(
    '/Users/lucy/BDSE30MP/weather_clean/daily_weather_feature_TP.csv', encoding='UTF-8')

# 把溫度度風速雨量的非數字取代成nan
df_a[['Temperature', 'WS', 'RH', 'Precp']] = df_a[['Temperature', 'WS',
                                                   'RH', 'Precp']].replace(['/', 'X', '...', 'V', '&', 'T'], np.nan)

# 氣溫補值

df_merged = pd.merge(df_a, df_b, left_on=['WHOLE_DATE', 'CITY'], right_on=[
                     'whole_date', 'city'])

df_merged['Temperature'].fillna(df_merged['AVGT_TP'], inplace=True)
df_merged.info()
df_a = df_merged.iloc[:, :-3]


# 轉數字
df_a[['Temperature', 'WS', 'RH', 'Precp']] = df_a[['Temperature',
                                                   'WS', 'RH', 'Precp']].apply(pd.to_numeric, errors='coerce')
df_a[['Temperature', 'RH', 'WS', 'Precp']].info()

print(f'補值前中位數：\n{df_a[["Temperature","RH","WS","Precp"]].median()}')
print(f'補值前平均：\n{df_a[["Temperature","RH","WS","Precp"]].mean()}')

# 風速空值補中位數
df_a['WS'] = df_a['WS'].fillna(df_a['WS'].median())

# 濕度和雨量同時空值時補中位數
rh_median = df_a['RH'].median()
precp_median = df_a['Precp'].median()
mask1 = df_a['RH'].isna() & df_a['Precp'].isna()
df_a.loc[mask1, 'RH'] = rh_median
df_a.loc[mask1, 'Precp'] = precp_median

# 濕度有值，雨量沒值-補雨量中位數
mask2 = df_a['RH'].notna() & df_a['Precp'].isna()
df_a.loc[mask2, 'Precp'] = precp_median

# 雨量有值，濕度沒值-補中位數
mask3 = df_a['Precp'].notna() & df_a['RH'].isna()
df_a.loc[mask3, 'RH'] = rh_median


# 檢查目前缺失值數量
df_a[['Temperature', 'RH', 'WS', 'Precp']].info()

print(f'補值後中位數：\n{df_a[["Temperature","RH","WS","Precp"]].median()}')
print(f'補值後平均：\n{df_a[["Temperature","RH","WS","Precp"]].mean()}')

df_a.to_csv('TP_CLEAN.csv', index=False, encoding='utf-8')


# 一行一行寫入資料庫
for row in df.itertuples(index=False):
    values = ', '.join([f"'{value}'" if pd.notnull(
        value) else 'NULL' for value in row])
    query = f"INSERT INTO {table_name} VALUES ({values})"
    try:
        with conn.cursor() as cursor:

            cursor.execute(query)

    except pymysql.MySQLError as e:
        print(f"row: {row}: {str(e)}\n")

conn.commit()
print(f"Finished processing row {row}")

conn.close()
