import os
import csv

directory = 'D:/zz_Mete_Fore/2010-2013csv-4.02'

'''
def select_from():   # 查找/删除/保留特定行
    for dir_path, dir_name, file_names in os.walk(directory):
        for file_name in file_names:
            # if file_name == 'All.csv':
                csv_file_in = os.path.join(dir_path, file_name)
                file_name_1 = file_name.split('.')[0]+'_p'+'.csv'
                csv_file_out = os.path.join(dir_path, file_name_1)
                print('processing ' + csv_file_in)
                with open(csv_file_in, 'r') as f_in, open(csv_file_out, 'w', newline='') as f_out:
                    reader = csv.reader(f_in, skipinitialspace=True)
                    writer = csv.writer(f_out, delimiter=',')
                    # write headers
                    writer.writerow(next(reader))
                    for row in reader:
                        if row[-1] != 'NULL':   # 保留最后一列不为NULL的行
                            writer.writerow(row)


def select_from_1():   # 查找/删除/保留特定行
    for dir_path, dir_name, file_names in os.walk(directory):
        for file_name in file_names:
            if file_name == 'All_p.csv':  # 仅处理All_p文件
                csv_file_in = os.path.join(dir_path, file_name)
                file_name_1 = 'Rain_py'+'.csv'
                csv_file_out = os.path.join(dir_path, file_name_1)
                print('processing ' + csv_file_in)
                with open(csv_file_in, 'r') as f_in, open(csv_file_out, 'w', newline='') as f_out:
                    reader = csv.reader(f_in, skipinitialspace=True)
                    writer = csv.writer(f_out, delimiter=',')
                    # write headers
                    first_row = next(reader)
                    i = first_row.index('Precipitation')
                    writer.writerow(first_row)
                    rows_affected = 0
                    for row in reader:
                        if row[i] != '0000'\
                                and row[i] != '000'\
                                and row[i] != '00000'\
                                and row[i] != '////'\
                                and row[i] != '/////'\
                                and row[i] != '///':
                            writer.writerow(row)
                            rows_affected += 1
                print('' + rows_affected + '行受影响')
'''


def condition(raw_i, description):
    if description.isdigit():
        if not raw_i.isdigit():
            return raw_i == description
        else:
            return int(raw_i) == int(description)
    elif description == 'rain':
        return is_rain(raw_i)
    elif description == 'not rain':
        return raw_i == '0000'
    elif description == 'null':
        return is_null(raw_i)
    elif description == 'not null':
        return not is_null(raw_i)
    elif description[0:2] == 'gt':
        return int(raw_i) > int(description[2:])
    elif description[0:3] == 'ngt':
        return int(raw_i) <= int(description[3:])
    elif description[-3:] == 'min':
        return is_x_min(raw_i, description[0:2])
    elif description == 'True':
        return True
    else:
        return raw_i == description


def is_null(raw_i):
    if raw_i == 'NULL' :
        return True


def is_x_min(observe_times, x):
    if observe_times[-4:] == x + '00':
        return True


def is_rain(precipitation):    # 降水不为零，有雨
    if str(precipitation).isdigit() and int(precipitation) > 0:
        return True


'''
 and precipitation != '0'\
            and precipitation != '0000' \
            and precipitation != 'error'\
            and precipitation != '000' \
            and precipitation != '00000' \
            and precipitation != '////' \
            and precipitation != '/////' \
            and precipitation != '///'
'''


def select(key, from_f, to_f, description):   # 查找/删除/保留特定行
    for dir_path, dir_name, file_names in os.walk(directory):
        for file_name in file_names:
            if file_name == from_f:  # 仅处理All文件
                csv_file_in = os.path.join(dir_path, file_name)
                file_name_1 = to_f
                csv_file_out = os.path.join(dir_path, file_name_1)
                print('processing ' + csv_file_in)
                with open(csv_file_in, 'r') as f_in, open(csv_file_out, 'w', newline='') as f_out:
                    reader = csv.reader(f_in, skipinitialspace=True)
                    writer = csv.writer(f_out, delimiter=',')
                    # write headers
                    first_row = next(reader)
                    if key.isdigit():
                        i = int(key)
                    else:
                        i = first_row.index(key)
                    writer.writerow(first_row)
                    rows_affected = 0
                    for row in reader:
                        if condition(row[i],description) :
                            writer.writerow(row)
                            rows_affected += 1
                print(str(rows_affected) + " 行受影响")


# select('ObservTimes', 'All_py.csv', 'All_00.csv', 'True')
# select('Precipitation', 'All_10_60min_sub.csv', 'Rain_1hour.csv', 'rain')
select('Precipitation', 'Rain_1hour.csv', 'Rain_ngt3.csv', 'ngt3')


def select_1(from_f, to_f):   # 查找/删除/保留特定行
    for dir_path, dir_name, file_names in os.walk(directory):
        for file_name in file_names:
            if file_name == from_f:  # 仅处理All文件
                csv_file_in = os.path.join(dir_path, file_name)
                file_name_1 = to_f
                csv_file_out = os.path.join(dir_path, file_name_1)
                print('processing ' + csv_file_in)
                with open(csv_file_in, 'r') as f_in, open(csv_file_out, 'w', newline='') as f_out:
                    reader = csv.DictReader(f_in, skipinitialspace=True)
                    writer = csv.writer(f_out, delimiter=',')
                    # write headers
                    first_row = next(reader)
                    writer.writerow(first_row)
                    rows_affected = 0
                    for row in reader:
                        writer.writerow(row)
                        rows_affected += 1
                print(rows_affected,"行受影响")

# select_1('All_py.csv', 'All_short.csv')
