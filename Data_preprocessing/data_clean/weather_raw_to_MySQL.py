# 檔案名稱取出日期值並加入檔案欄位中
import csv
import os
import re
import pymysql
import time

# 資料庫必要資訊
db_config = {
    "host": "ip address",
    "user": "your account",
    "password": "your password",
    "database": "your DB name"
}
# 連接到MySQL資料庫
conn = pymysql.connect(**db_config)
cursor = conn.cursor()

# 原始檔案所在目錄
source_path = "../data_RAW/六都天氣資料/有效測站_by_all"

# 更改後的檔案要儲存的地方
# dest_path = "./new_466930/"

# 取檔名裡觀測站ID的正規表達式
patternId = r"^(.*?)-"

# 取檔名裡年月日的正規表達式
patternWholeDate = r"(\d{4}-\d{2}-\d{2})"

# # 取檔名裡年的正規表達式
# patternYear = r"-(\d{4})-"

# # 取檔名裡月的正規表達式
# patternMonth = r"-(\d{2})-"

# # 取檔名裡日的正規表達式
# patternDate = r"-(\d{2})\."

# 將目錄裡的檔案利用迴圈依序做處理
start_time = time.time()
row_total_count = 1
for filename in os.listdir(source_path):

    # 利用正規表達式取出檔名的觀測站ID
    match = re.search(patternId, filename)
    match_station_ID = match.group(1)

    # 利用正規表達式取出檔名的年月日
    match = re.search(patternWholeDate, filename)
    match_whole_date = match.group()

    # # 利用正規表達式取出檔名的年
    # match = re.search(patternYear, filename)
    # match_year = match.group()

    # # 利用正規表達式取出檔名的月
    # match = re.search(patternMonth, filename)
    # match_month = match.group()

    # # 利用正規表達式取出檔名的日
    # match = re.search(patternDate, filename)
    # match_date = match.group()

    # 將檔案讀取
    with open(os.path.join(source_path, filename), "r", newline="", encoding="utf-8") as file:

        # 將讀取的csv去除掉前兩行存在rows變數裡
        reader = csv.reader(file)
        rows = list(reader)
        rows = rows[2:]

        # 將觀測站的ID塞到第一列
        for row in rows[0:]:
            row.insert(0, f"{match_station_ID}")

        # 將日期塞到第二列
        for row in rows[0:]:
            row.insert(1, f"{match_whole_date}")

        # for row in rows[0:]:
        #     row.insert(2, f"{match_year}")

        # for row in rows[0:]:
        #     row.insert(3, f"{match_month}")

        # for row in rows[0:]:
        #     row.insert(4, f"{match_date}")

        # 將修改後的資料塞到weater的table裡
        try:
            for row in rows[0:]:
                row_total_count += 1
                cursor.execute("INSERT INTO lucy_weather(Station_ID , whole_date, ObsTime, StnPres, SeaPres, Temperature, Td_dew_point, RH, WS, WD, WSGust,WDGust, Precp, PrecpHour, SunShine, GloblRad, Visb, UVI, Cloud_Amount) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", row)

            if row_total_count % 30000 == 0:
                conn.commit()

        except pymysql.MySQLError as e:
            with open('error_log9.txt', 'a') as err_log:  # 記得 改一下erro_log的編號
                err_log.write(
                    f"Error inserting file:{filename}, row: {row}: {str(e)}\n")

        finally:
            # 這部分的代碼無論是否有錯誤都會執行
            conn.commit()   # 最後剩餘的commit
            print(f"Finished processing row {row}")
end_time = time.time()
elapsed_time = end_time - start_time
print(f"The code took {elapsed_time} seconds to run.")

# 改名後另存新檔

# with open(os.path.join(dest_path, filename), "w", newline="", encoding="utf-8") as file:
#     writer = csv.writer(file)
#     writer.writerows(rows)
cursor.close()
conn.close()
