import pandas as pd
import numpy as np
df = pd.read_csv(
    '/Users/lucy/BDSE30MP/code/anlysis_model/高雄市_ALL.csv', encoding='UTF-8')

df = df.drop(['WHOLE_DATE', 'WHOLE_TIME', 'ADMIN_UNIT', 'Temperature', 'WD', 'WSGust', 'WDGust', 'visb', 'PrecpHour',
             'PUN_LINE_SIGNAL', 'PUN_RED_LIGHT', 'PUN_OVER_SPEED', 'PUN_IGNORE_WALKER', 'PUN_ROAD_KIND', 'PUN_PARKING'], axis=1)

# 妖魔鬼怪取代成nan
df[['RH', 'WS', 'Precp']] = df[['RH', 'WS', 'Precp']].replace(
    ['/', 'X', '...', 'V', '&', 'T'], np.nan)

# 檢查目前缺失值數量
df[['RH', 'WS', 'Precp']].info()

# 轉數字
df[['RH', 'WS', 'Precp']] = df[['RH', 'WS', 'Precp']].apply(
    pd.to_numeric, errors='coerce')


print(f'補值前中位數：\n{df[["RH","WS","Precp"]].median()}')
print(f'補值前平均：\n{df[["RH","WS","Precp"]].mean()}')


# 濕度和雨量同時空值時補中位數
rh_median = df['RH'].median()
precp_median = df['Precp'].median()

mask1 = df['RH'].isna() & df['Precp'].isna()


df.loc[mask1, 'RH'] = rh_median
df.loc[mask1, 'Precp'] = precp_median

# 濕度和雨量單一為空值但另一個為0

df.loc[df['RH'].isna() & (df['Precp'] == 0), 'RH'] = 0
df.loc[df['Precp'].isna() & (df['RH'] == 0), 'Precp'] = 0

# 風速空值補中位數
df['WS'] = df['WS'].fillna(df['WS'].median())

# 檢查目前缺失值數量
df[['RH', 'WS', 'Precp']].info()

print(f'補值後中位數：\n{df[["RH","WS","Precp"]].median()}')
print(f'補值後平均：\n{df[["RH","WS","Precp"]].mean()}')
