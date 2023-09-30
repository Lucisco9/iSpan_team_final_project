import pymysql
import pandas as pd

# connection

host = 'ip address'
user = 'your account'
password = 'your password'
database = 'your DB name'
port = 3306

conn = pymysql.connect(host=host, user=user,
                       password=password, database=database, port=port)

# table name from DB
table_name = 'your table name'

source_path = "your csv file path"

df = pd.read_csv(f'{source_path}', encoding='UTF-8', header=0, index_col=False)


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
