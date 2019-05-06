import pandas as pd
import numpy as np
import csv
# filename = 'D:/zz_Mete_Fore/2010-2013csv-3.29/2010071920-2010072208/Rain_p.csv'
'''
0-1-2
3-4-5
6-7-8
'''
csv_file_in = 'D:/zz_Mete_Fore/10分钟训练数据集（dbz）.csv'
csv_file_out = 'D:/zz_Mete_Fore/10分钟训练数据集（dbz）_处理后.csv'
with open(csv_file_in, 'r') as f_in, open(csv_file_out, 'w', newline='') as f_out:
    reader = csv.reader(f_in, skipinitialspace=True)
    writer = csv.writer(f_out, delimiter=',')
    # write headers
    first_row = next(reader)
    writer.writerow(first_row)
    rows_affected = 0
    for row in reader:
        if int(row[-1])>1 and int(row[-1]) <= 200 :
            writer.writerow(row)
            rows_affected += 1
print(str(rows_affected) + " 行受影响")

'''

csv_file = 'new1.csv'
csv_new_file = 'new2.csv'
df = pd.read_csv(csv_file)
df.drop(index=0, inplace=True)
df.reset_index(inplace=True, drop=True)
j = 6
for index, row in df.iterrows():
    print("shape=", df.shape[0],"index=",index)
    if index == 0:
        continue
    if index == df.shape[0]:
        break
    if df.loc[index, 'name'] == df.loc[index - 1, 'name']:
        print('same')

    else:
        if index != 0:
            print('change')
            df.drop(index=index, inplace=True)
            df.reset_index(inplace=True, drop=True)
df.to_csv(csv_new_file,index=False, header=1, mode='w')

'''
'''
df = pd.read_csv(csv_file)
df_new = df.drop_duplicates(subset=['age'], axis=1, keep='first')    # 去掉age列重复的行
df_new.to_csv(csv_new_file, columns=['name','age'], index=False, header=1, mode='w')    # index索引，header表头
for index, row in df.iterrows():
     print(index,row['age'],row['name'])

'''

'''



filename = 'C:/Users/金科/Desktop/自动站信息表.csv'


with open(filename) as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)

with open(filename) as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['StationNum'] == 'L8010':
            print(row
'''
'''
data = [['name', 'age'],
        ['Bob', 14],
        ['Tom', 23],
        ['Bill', 30],
        ['Linda', 24],
        ['Jim', 3],
        ['Hel', 30]
        ]
filename1 = 'example.csv'
with open(filename1,'w',newline='') as f:
    writer = csv.writer(f)
    for row in data:
        writer.writerow(row)
'''
'''
# 删除/保留特定行
with open('example.csv', 'r') as f_in, open('f_out.csv', 'w', newline='') as f_out:
    reader = csv.reader(f_in, skipinitialspace=True)
    writer = csv.writer(f_out, delimiter=',')
    # write headers
    writer.writerow(next(reader))
    for row in reader:
        if int(row[-1]) >= 24:    # -1 means the last column
            writer.writerow(row)
'''
'''
os.walk()会返回三元元组（dirpath，dirname，filenames）
dirpath: 根路径（字符串）
dirnames:路径下所有目录（列表）
filenames:路径下所有非目录文件名
'''
'''
import os
directory = 'folder'
for dir_path, dir_name, file_names in os.walk(directory):
    for file_name in file_names:
        print(os.path.join(dir_path, file_name))
'''