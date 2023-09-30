import pymysql
import pandas as pd

host = 'ip address'
user = 'your account'
password = 'your password'
database = 'your DB name'
port = 3306

# 建立mysql連線
conn = pymysql.connect(host=host, user=user,
                       password=password, database=database, port=port)

cursor = conn.cursor()

columns_to_select = ['WHOLE_DATE', 'WHOLE_TIME', 'ACCIDENT_TYPE', 'ADMIN_UNIT', 'CITY', 'ACCIDENT_ADDR', 'WEATHER', 'LIGHT', 'ROAD_TYPE_MAIN', 'SPEED_LIMIT', 'ROAD_TYPE_SUB1', 'ROAD_TYPE_SUB2', 'LOCATION_MAIN', 'LOCATION_SUB', 'PAVE_MTL', 'PAVE_CDN', 'PAVE_FLAW', 'BAR', 'BAR_QUA', 'BAR_VIS', 'SIGNAL_TYPE', 'SIGNAL_CDN', 'LANE_MAIN', 'LANE_SUB', 'LANE_LINE', 'LANE_LINE_SPEED',
                     'LANE_LINE_EDGE', 'ACCIDENT_OBJ', 'ACCIDENT_CASE', 'CAUSE_MAIN', 'CAUSE_SUB', 'ACCIDENT_DEAD', 'ACCIDENT_INJURY', 'ACCIDENT_OBJ_ORDER', 'VEHICLE_MAIN', 'VEHICLE_SUB', 'OBJ_GENDER', 'OBJ_AGE', 'PROTECTION', 'C_PDT_USAGE', 'OBJ_CDN_MAIN', 'OBJ_CDN_SUB', 'CRASH_MAIN', 'CRASH_SUB', 'CRASH_OTHER_MAIN', 'CRASH_OTHER_SUB', 'CAUSE_MAIN_DETAIL', 'CAUSE_SUB_DETAIL', 'HAR', 'LONGITUDE', 'LATITUDE']

delete_queries = [
    "DELETE FROM lucy_accident WHERE city='臺北市' AND LONGITUDE > 121.527 AND LATITUDE > 25.32",
    "DELETE FROM lucy_accident WHERE city='新北市' AND LONGITUDE > 121.607 AND LATITUDE < 24.836",
    "DELETE FROM lucy_accident WHERE city='新北市' AND LONGITUDE < 121.337 AND LATITUDE > 25.173",
    "DELETE FROM lucy_accident WHERE city='桃園市' AND LONGITUDE < 121.131 AND LATITUDE < 24.856",
    "DELETE FROM lucy_accident WHERE city='臺中市' AND LONGITUDE < 120.462 AND LATITUDE < 24.189",
    "DELETE FROM lucy_accident WHERE city='臺中市' AND LONGITUDE < 120.505 AND LATITUDE > 24.258",
    "DELETE FROM lucy_accident WHERE city IN ('台南市', '高雄市') AND LONGITUDE > 120.886 AND LATITUDE < 23.146",
    "DELETE FROM lucy_accident WHERE city IN ('台南市', '高雄市') AND LONGITUDE > 120.476 AND LATITUDE < 22.767",
    "DELETE FROM lucy_accident WHERE city IN ('台南市', '高雄市') AND LONGITUDE < 120.345 AND LATITUDE < 22.464",
    "DELETE FROM lucy_accident WHERE city IN ('台南市', '高雄市') AND LONGITUDE < 120.234 AND LATITUDE < 22.723"
]

for delete_query in delete_queries:
    cursor.execute(delete_query)
    conn.commit()

select_query = "SELECT * FROM lucy_accident"
cursor.execute(select_query)
results = cursor.fetchall()

columns = [column[0] for column in cursor.description]

data = []
for row in results:
    data.append(list(row))

df = pd.DataFrame(data, columns=columns_to_select)

cursor.close()
conn.close()

file_path = "/Users/lucy/BDSE30MP/test_drop.csv"

df.to_csv(file_path, index=False)


# %%第二次清整

host = 'ip address'
user = 'your account'
password = 'your password'
database = 'your DB name'
port = 3306

# 建立mysql連線
conn = pymysql.connect(host=host, user=user,
                       password=password, database=database, port=port)
cursor = conn.cursor()

columns_to_select = ['WHOLE_DATE', 'WHOLE_TIME', 'ACCIDENT_TYPE', 'ADMIN_UNIT', 'CITY', 'ACCIDENT_ADDR', 'WEATHER', 'LIGHT', 'ROAD_TYPE_MAIN', 'SPEED_LIMIT', 'ROAD_TYPE_SUB1', 'ROAD_TYPE_SUB2', 'LOCATION_MAIN', 'LOCATION_SUB', 'PAVE_MTL', 'PAVE_CDN', 'PAVE_FLAW', 'BAR', 'BAR_QUA', 'BAR_VIS', 'SIGNAL_TYPE', 'SIGNAL_CDN', 'LANE_MAIN', 'LANE_SUB', 'LANE_LINE', 'LANE_LINE_SPEED',
                     'LANE_LINE_EDGE', 'ACCIDENT_OBJ', 'ACCIDENT_CASE', 'CAUSE_MAIN', 'CAUSE_SUB', 'ACCIDENT_DEAD', 'ACCIDENT_INJURY', 'ACCIDENT_OBJ_ORDER', 'VEHICLE_MAIN', 'VEHICLE_SUB', 'OBJ_GENDER', 'OBJ_AGE', 'PROTECTION', 'C_PDT_USAGE', 'OBJ_CDN_MAIN', 'OBJ_CDN_SUB', 'CRASH_MAIN', 'CRASH_SUB', 'CRASH_OTHER_MAIN', 'CRASH_OTHER_SUB', 'CAUSE_MAIN_DETAIL', 'CAUSE_SUB_DETAIL', 'HAR', 'LONGITUDE', 'LATITUDE']

delete_queries = ["delete FROM lucy_accident WHERE city='臺北市' and LONGITUDE <121.364 and LATITUDE >25.152",
                  "delete from lucy_accident WHERE city='桃園市' and LONGITUDE >121.603 and LATITUDE <24.778",
                  "delete from lucy_accident WHERE city='高雄市' and LONGITUDE <120.026 and LATITUDE <23.01",
                  "delete from lucy_accident WHERE city='臺中市' and LONGITUDE <120.571 and LATITUDE >24.362",
                  "delete from lucy_accident WHERE city='新北市' and LONGITUDE >121.776 and LATITUDE <24.883"
                  ]


for delete_query in delete_queries:
    cursor.execute(delete_query)
    conn.commit()

select_query = "SELECT * FROM lucy_accident"
cursor.execute(select_query)
results = cursor.fetchall()

columns = [column[0] for column in cursor.description]

data = []
for row in results:
    data.append(list(row))

df = pd.DataFrame(data, columns=columns_to_select)

cursor.close()
conn.close()

file_path = "/Users/lucy/BDSE30MP/test_drop_2.csv"

df.to_csv(file_path, index=False)
