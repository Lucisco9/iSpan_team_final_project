import pandas as pd


merge_WC = pd.read_csv(
    '/Users/lucy/BDSE30MP/data_CLEAN/with_CAMERA_by_month.csv', encoding='utf-8')

merge_WC.insert(0, 'CITY', merge_WC['camera_id'].str[:2])
merge_WC['CITY'] = merge_WC['CITY'].replace(
    {'KH': '高雄市', 'TP': '臺北市', 'TC': '臺中市', 'TY': '桃園市', 'TN': '臺南市', 'NP': '新北市'})

# 計算有科技執法 2022/12/1前後月平均事故量差異
merge_WC['diff_per_monthly'] = ((merge_WC['after_avg_BY_MONTH'] -
                                merge_WC['before_avg_BY_MONTH']) / merge_WC['before_avg_BY_MONTH']) * 100

WC_decrease_m = (merge_WC['diff_per_monthly'] < 0).sum()
merge_WC['diff_per_monthly'] = merge_WC['diff_per_monthly'].map(
    '{:.2f}%'.format)

dest = '/Users/lucy/BDSE30MP/'
merge_WC.to_csv(f'{dest}merge_WC.csv', encoding='utf-8', index=False)
