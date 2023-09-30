import pandas as pd
import numpy as np
from geopy.distance import geodesic

# 讀取檔案 mac
# df_a = pd.read_csv('/Users/lucy/BDSE30MP/data_CLEAN/高雄市_All.csv',encoding='UTF-8-sig', header=0,index_col=False)
# df_b = pd.read_csv('/Users/lucy/BDSE30MP/data_RAW/六都科技執法資料/科技執法總清單_20230627_NP.csv',encoding='UTF-8-sig',header=0,index_col=False)

# 讀取檔案-woindows
df_a = pd.read_csv(
    'C:/Users/student/Main_P/data_CLEAN/by_city&AT/高雄市_ALL.csv', encoding='UTF-8-sig')
df_b = pd.read_csv(
    'C:/Users/student/Main_P/data_RAW/六都科技執法清單/科技執法總清單_20230627_NP.csv', encoding='UTF-8-sig')

df_b['緯度'] = pd.to_numeric(df_b['緯度'], errors='coerce')
df_b['經度'] = pd.to_numeric(df_b['經度'], errors='coerce')
df_b = df_b.dropna(subset=['緯度', '經度'])

# 初始化兩個新欄位
df_a['near_df_b_longitude'] = None
df_a['near_df_b_latitude'] = None


# 對 df_b 的每一行執行迴圈
for idx_b, row_b in df_b.iterrows():
    try:
        # 取出 df_b 的經緯度
        center = (row_b['緯度'], row_b['經度'])

        # 對 df_a 的每一行執行迴圈
        for idx_a, row_a in df_a.iterrows():

            try:
                # 取出 df_a 的經緯度
                point = (row_a['LATITUDE'], row_a['LONGITUDE'])

                # 計算兩點間的距離
                dist = geodesic(center, point).meters

                # 如果距離在 500 公尺內
                if dist <= 500:
                    # 則在 df_a 中填入 df_b 的經緯度
                    df_a.at[idx_a, 'near_df_b_latitude'] = row_b['緯度']
                    df_a.at[idx_a, 'near_df_b_longitude'] = row_b['經度']
            except Exception as e:
                print(f'Error processing df_a row {idx_a}: {e}')

    except Exception as e:
        print(f'Error processing df_b row {idx_b}: {e}')

df_a.to_csv('df_a_geopy.csv', encoding='UTF-8-sig', index=False)
