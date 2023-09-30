import datetime
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

# %%
# mac
# df = pd.read_csv('/Users/lucy/BDSE30MP/RAW/全國交通事故資料/SIX_CITY_ALL.csv',encoding='UTF-8-sig', header=0,index_col=False).replace('\\N',None) #SQL匯出時會把空值補為\N，要取代

# windows
df = pd.read_csv('C:/Users/student/Main_P/data_CLEAN/SIX_CITY_ALL.csv', encoding='UTF-8-sig',
                 header=0, index_col=False).replace('\\N', None)  # SQL匯出時會把空值補為\N，要取代成空值

# %% 對 'OBJ_AGE' 欄位的數值清整
df['OBJ_AGE'].astype(int)
bins_age = [0, 18, 40, 65, np.inf]
labels_age = ['少年', '青年', '中年', '老年']
df['OBJ_AGE_CATEGORICAL'] = pd.cut(df['OBJ_AGE'].astype(
    int), bins=bins_age, labels=labels_age, right=False, include_lowest=True)
df.loc[df['OBJ_AGE'] < 0, 'OBJ_AGE'] = np.nan
df['OBJ_AGE'] = df['OBJ_AGE_CATEGORICAL']
df = df.drop(columns=['OBJ_AGE_CATEGORICAL'])

# %% 對 'SPEED_LIMIT' 欄位的數值清整

df.loc[(df['SPEED_LIMIT'] > 0) & (df['SPEED_LIMIT'] < 10), 'SPEED_LIMIT'] = df.loc[(
    df['SPEED_LIMIT'] > 0) & (df['SPEED_LIMIT'] < 10), 'SPEED_LIMIT'].astype(int) * 10
df.loc[(df['SPEED_LIMIT'] >= 30) & (df['SPEED_LIMIT'] < 110),
       'SPEED_LIMIT'] = (df['SPEED_LIMIT'] // 10) * 10
df.loc[(df['SPEED_LIMIT'] > 110) & (df['SPEED_LIMIT'] < 200),
       'SPEED_LIMIT'] = ((df['SPEED_LIMIT'] % 100) // 10) * 10
df.loc[df['SPEED_LIMIT'] > 199, 'SPEED_LIMIT'] = (
    (df['SPEED_LIMIT'] // 100)*10).astype(int)
df.loc[(df['SPEED_LIMIT'] >= 10) & (df['SPEED_LIMIT'] < 30) & ~
       df['SPEED_LIMIT'].isin([10, 15, 20, 25]), 'SPEED_LIMIT'] = None
df.loc[df['SPEED_LIMIT'] == 0, 'SPEED_LIMIT'] = None


# %%當事者順位清整
df['ACCIDENT_OBJ_ORDER'] = df['ACCIDENT_OBJ_ORDER'].astype(int)

df.columns
df.info()
df.head()


# %%檢查
columns_to_check = ["SPEED_LIMIT"]

for column in columns_to_check:
    unique_values = df[column].unique()
    print(f"Column '{column}': {unique_values}")

# 匯出CSV
# df.to_csv('SIX_CITY_V2.csv',encoding='utf-8',index=False)


# %% 對經緯度兩欄位的數值清整
# mac
# df_LL= pd.read_csv('/Users/lucy/BDSE30MP/RAW/全國交通事故資料/SIX_CITY_V2.csv',encoding='UTF-8-sig', header=0,index_col=False)

# windows
df_ori = pd.read_csv('C:/Users/student/Main_P/data_CLEAN/SIX_CITY_V2.csv',
                     encoding='UTF-8', header=0, index_col=False)

df_adj = pd.read_csv('C:/Users/student/Desktop/LL_FLAW_NP.csv',
                     encoding='UTF-8-sig', header=0, index_col=False)
df_ori.info()
df_adj.info()

df_ori['WHOLE_DATE'] = pd.to_datetime(df_ori['WHOLE_DATE'])
df_adj['WHOLE_DATE'] = pd.to_datetime(df_adj['WHOLE_DATE'])
df_ori['ACCIDENT_TYPE'] = df_ori['ACCIDENT_TYPE'].astype(str)
df_adj['ACCIDENT_TYPE'] = df_adj['ACCIDENT_TYPE'].astype(str)
df_ori['ACCIDENT_ADDR'] = df_ori['ACCIDENT_ADDR'].astype(str)
df_adj['ACCIDENT_ADDR'] = df_adj['ACCIDENT_ADDR'].astype(str)

# 遍歷df_ori的每一行資料
for index, row in df_ori.iterrows():
    # 檢查日期、時間和地址是否能在df_adj中找到對應的正確經緯度
    mask = (df_adj['WHOLE_DATE'] == row['WHOLE_DATE']) & (df_adj['ACCIDENT_TYPE']
                                                          == row['ACCIDENT_TYPE']) & (df_adj['ACCIDENT_ADDR'] == row['ACCIDENT_ADDR'])
    if not df_adj.loc[mask].empty:

        # 取得對應的正確經緯度
        correct_longitude = df_adj.loc[mask, 'ADJ_LONGITUDE'].values[0]
        correct_latitude = df_adj.loc[mask, 'ADJ_LATITUDE'].values[0]

        # 更新df_ori中對應行的經緯度值
        df_ori.at[index, 'LONGITUDE'] = correct_longitude
        df_ori.at[index, 'LATITUDE'] = correct_latitude


# 把datetime改回來
df_ori['WHOLE_DATE'] = df_ori['WHOLE_DATE'].dt.strftime('%Y-%m-%d')
df_ori.info()
df_adj.info()

# 檢查
out_of_range_longitude = df_ori.loc[df_ori['LONGITUDE'] > 123, 'LONGITUDE']
out_of_range_latitude = df_ori.loc[df_ori['LATITUDE'] > 26, 'LATITUDE']

# 檢查超出範圍的經度
if not out_of_range_longitude.empty:
    print("超出範圍的經度:")
    print(out_of_range_longitude)

# 檢查超出範圍的緯度
if not out_of_range_latitude.empty:
    print("超出範圍的緯度:")
    print(out_of_range_latitude)
