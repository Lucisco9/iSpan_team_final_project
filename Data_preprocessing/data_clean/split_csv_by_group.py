
import pandas as pd

df = pd.read_csv('你的csv檔路徑', encoding='UTF-8')

output_dir = '分組拆解完的檔案存放路徑'
grouped = df.groupby('要作為分組依據的欄位名稱')


for type_, data in grouped1:
    file_name = f'{type_}你的檔名.csv'
    data.to_csv(file_name, index=False)
    print(f"{output_dir}{file_name} 檔案已保存")

print("mission complete")
