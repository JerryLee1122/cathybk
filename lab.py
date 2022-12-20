import pandas as pd
import os
from sys import exit

dir_path = '/Users/jerry/cathybk/files/'

def tidy_file (file_name):
    df = pd.read_csv(dir_path + file_name)
    new_header = df.iloc[0]

    df = df[1:]
    df.columns = new_header

    file_name_y = file_name.split('_')[0][0:3]
    file_name_q = file_name.split('_')[0][-1]
    file_name_city = file_name.split('_')[1]
    file_name_type = file_name.split('_')[4][0]

    df_name = file_name_y + '_' + file_name_q + '_' + file_name_city + '_' + file_name_type

    df['df_name'] = df_name
    return df

def zh2digit (zh_num):
    zh2digit_table = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '十': 10}
    
    # 位數遞增，由高位開始取
    digit_num = 0
    # 結果
    result = 0
    # 暫時存儲的變量
    tmp = 0
    
    if isinstance(zh_num, float):
        return 0
    
    while digit_num < len(zh_num):
        tmp_zh = zh_num[digit_num]
        tmp_num = zh2digit_table.get(tmp_zh, None)
        
        if tmp_num == 10:
            if tmp == 0:
                tmp = 1
            result = result + tmp_num * tmp
            tmp = 0
        elif tmp_num is not None:
            tmp = tmp * 10 + tmp_num
        digit_num += 1
        
    result = result + tmp
    return result

def main():
    #取得檔名list
    res = []
    for path in os.listdir(dir_path):
        # check if current path is a file and is a csv file
        if os.path.isfile(os.path.join(dir_path, path)) and path[-3:]=='csv':
            res.append(path)
    
    df_all = pd.DataFrame()
    for f in res:
        print(f)
        #106S2_B_lvr_land_B.csv 原始檔案有問題
        if f != '106S2_B_lvr_land_B.csv':
            df_output = tidy_file(f)
            
        
        # try:
        #     df_output = tidy_file(f)
        # except pd.io.common.EmptyDataError:
        #     df_output = pd.DataFrame()
        df_all = df_all.append(df_output, ignore_index=True)
    
    #filter
    df_filter = df_all[(df_all['main use'] == '住家用') & (df_all['building state'].str.contains('住宅大樓'))]
    df_filter['ttl_floor_zh'] = df_filter['total floor number'].str.replace('層','')
    df_filter['ttl_floor_num'] = df_filter['ttl_floor_zh'].map(zh2digit)
    df_filter = df_filter[df_filter['ttl_floor_num'] >= 13]
    df_filter = df_filter.drop(columns=['ttl_floor_zh', 'ttl_floor_num'])
    df_all = df_filter
    
    #count
    #df_all = df_all.sample(n=5)
    
    ttl_item = df_all[df_all.columns[0]].count()
    ttl_parking = len(df_all[df_all['transaction sign'].str.contains('車位')])
    avg_price = df_all['total price NTD'].astype(int).mean()
    avg_parking_price = df_all[df_all['transaction sign'].str.contains('車位')]['total price NTD'].astype(int).mean()
    
    # print('總件數=' + str(ttl_item))
    # print('總車位數=' + str(ttl_parking))
    # print('平均總價元=' + str(avg_price))
    # print('平均車位總價元=' + str(avg_parking_price))
    
    data=[
        ['總件數', ttl_item],
        ['總車位數', ttl_parking],
        ['平均總價元', avg_price], 
        ['平均車位總價元', avg_parking_price]
    ]
    
    df_count = pd.DataFrame(data, columns=['計算項目', '數值'])

    df_all.to_csv('filter.csv')
    df_count.to_csv('count.csv')
    
    


if __name__ == "__main__":
    main()
