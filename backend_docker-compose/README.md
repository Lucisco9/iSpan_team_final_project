# 在GCP上開啟專題網站
將這個資料夾上傳到GCP的虛擬主機上後執行以下動作:
1. cd ~/flaskapp
2. sudo docker-compose build
3. sudo docker-compose up (如果有更新flaskapp內的東西才需要加上 --build)
4. 將back.zip解壓後將back.sql移到~/flaskapp/data/mysql/db/內
5. docker exec -it db env LANG=C.UTF-8 /bin/bash
6. mysql -u root -pteamone
7. CREATE USER 'teamone'@'%' IDENTIFIED BY 'teamone'; ALTER USER 'teamone' IDENTIFIED WITH mysql_native_password BY 'teamone'; GRANT ALL PRIVILEGES ON *.* TO 'teamone'@'%' WITH GRANT OPTION; FLUSH PRIVILEGES;
8. create database teamone;
9. exit;
10. mysql -u root -pteamone teamone < back.sql

## 檔案說明
請先將flaskapp/app/data/json.zip解壓縮