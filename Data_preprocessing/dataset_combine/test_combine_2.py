import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# 讀取檔案 mac
# df_a = pd.read_csv('/Users/lucy/BDSE30MP/data_CLEAN/高雄市_ALL.csv', encoding='UTF-8-sig')
# df_b = pd.read_csv('/Users/lucy/BDSE30MP/data_RAW/六都科技執法資料/科技執法總清單_20230627_NP.csv', encoding='UTF-8-sig')

# 讀取檔案-woindows
df_a = pd.read_csv(
    'C:/Users/student/Main_P/data_CLEAN/by_city&AT/高雄市_ALL.csv', encoding='UTF-8-sig')
df_b = pd.read_csv(
    'C:/Users/student/Main_P/data_RAW/六都科技執法清單/科技執法總清單_20230627_NP.csv', encoding='UTF-8-sig')

df_b['緯度'] = pd.to_numeric(df_b['緯度'], errors='coerce')
df_b['經度'] = pd.to_numeric(df_b['經度'], errors='coerce')
df_b = df_b.dropna(subset=['緯度', '經度'])

# 創建 GeoDataFrame
geometry_a = [Point(xy) for xy in zip(df_a["LONGITUDE"], df_a["LATITUDE"])]
gdf_a = gpd.GeoDataFrame(df_a, geometry=geometry_a)

geometry_b = [Point(xy) for xy in zip(df_b["經度"], df_b["緯度"])]
gdf_b = gpd.GeoDataFrame(df_b, geometry=geometry_b)

# 將資料的座標系統設定為 EPSG:3826
gdf_a.set_crs(epsg=3826, inplace=True)
gdf_b.set_crs(epsg=3826, inplace=True)

# 建立空間索引
sindex = gdf_b.sindex

# 建立空的 list 用以儲存結果
near_b_id = []
near_b_lat = []
near_b_long = []

# 設定閾值
threshold = 0.0045  # 單位為度，根據需求調整

# 對於 gdf_a 中的每一個點
for point in gdf_a.geometry:
    # 使用空間索引找出鄰近的點
    possible_matches_index = list(sindex.nearest(point.bounds))
    possible_matches = gdf_b.iloc[possible_matches_index]
    # 計算距離並找出最近的點
    closest_point = possible_matches.geometry.distance(point).idxmin()
    # 如果最近的點距離在 500 公尺以內
    if point.distance(gdf_b.geometry.loc[closest_point]) <= threshold:
        # 將該點的經緯度 ID 添加到 list
        near_b_id.append(gdf_b['TEMP ID'].loc[closest_point])
        # 使用 y 屬性來取得點的緯度
        near_b_lat.append(gdf_b.geometry.loc[closest_point].y)
        # 使用 x 屬性來取得點的經度
        near_b_long.append(gdf_b.geometry.loc[closest_point].x)
    else:
        # 如果沒有點在 500 公尺以內，則添加 None
        near_b_id.append(None)
        near_b_lat.append(None)
        near_b_long.append(None)


# 將資料的座標系統轉換回 EPSG:4326（WGS 84）
gdf_a = gdf_a.to_crs(epsg=4326)
gdf_b = gdf_b.to_crs(epsg=4326)

# 為 df_a 新增欄位
df_a['near_df_b_longitude'] = near_b_long
df_a['near_df_b_latitude'] = near_b_lat
df_a['near_df_b_id'] = near_b_id


# 新欄位空值的用原本的經緯度
df_a.loc[df_a['near_df_b_longitude'].isna(
), 'near_df_b_longitude'] = df_a.loc[df_a['near_df_b_longitude'].isna(), 'LONGITUDE']
df_a.loc[df_a['near_df_b_latitude'].isna(
), 'near_df_b_latitude'] = df_a.loc[df_a['near_df_b_latitude'].isna(), 'LATITUDE']


# 將資料寫入 CSV 檔案
df_a.to_csv('ALLKS_geopandas.csv', encoding='UTF-8-sig', index=False)
count_dict = df_a.groupby('near_df_b_id').size().to_dict()
df_counts = pd.DataFrame(list(count_dict.items()),
                         columns=['near_b_id', 'count'])
df_counts.to_csv('ALLKS_counts_geopandas.csv',
                 encoding='UTF-8-sig', index=False)
