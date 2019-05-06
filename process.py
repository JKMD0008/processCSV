import struct
import numpy as np
import binascii
import scipy.misc
import os
import bz2
import shutil
import pandas as pd
import matplotlib.pyplot as pyplot
import datetime


rada_dir = 'G:/SWAN_RADAMOSAIC_PRODUCTS'
rada_des = 'G:/Mete_Fore/rada_des'


def enter():
    """
    入口
    """
    # gather_csv('Rain_1hour.csv')
    match_time('50', '48', 201008271450)  #  00,00 10,12 20,18 30,30 40,42 50,48
    # reformat_train_data()
    # traverse_draw_data()
    # get_pure_binary()


def read_bin(path, for_what):
    """
    读取二进制文件
    """
    # 打印信息
    print_txt = []
    # 获取文件名
    file_name = path.split('/')[-1].split('.')[0]
    f = open(path, 'rb')
    zon_name = f.read(12)
    info = remove_invalid(f.read(38))
    # info = f.read(38)
    title = remove_invalid(f.read(8))
    # title = f.read(8)
    version = f.read(8)
    year = f.read(2)
    month = f.read(2)
    day = f.read(2)
    hour = f.read(2)
    minute = f.read(2)
    interval = f.read(2)
    XNumGrids = f.read(2)
    YNumGrids = f.read(2)
    ZNumGrids = f.read(2)
    RadarCount = f.read(4)

    StartLon = f.read(4)
    StartLat = f.read(4)
    CenterLon = f.read(4)
    CenterLat = f.read(4)
    XReso = f.read(4)
    YReso = f.read(4)
    ZhighGrids = f.read(160)

    # TODO 注释掉所有打印信息，暂时不需要
    XNumGrids = int.from_bytes(XNumGrids, byteorder='little')
    YNumGrids = int.from_bytes(YNumGrids, byteorder='little')
    ZNumGrids = int.from_bytes(ZNumGrids, byteorder='little')
    StartLon = struct.unpack('<f', StartLon)[0]
    StartLat = struct.unpack('<f', StartLat)[0]
    str_cities = str(get_station_name(f))
    if for_what == 'draw' or for_what == 'both':
        print_txt.append('文件名称：' + str(zon_name.decode('utf-8')))
        print_txt.append('文件说明：' + str(info))
        print_txt.append('文件标志：' + str(title))
        print_txt.append('文件版本：' + str(version.decode('utf-8')))
        print_txt.append('年 year: ' + str(int.from_bytes(year, byteorder='little')))
        print_txt.append('月 month: ' + str(int.from_bytes(month, byteorder='little')))
        print_txt.append('天 day: ' + str(int.from_bytes(day, byteorder='little')))
        print_txt.append('小时 hour: ' + str(int.from_bytes(hour, byteorder='little')))
        print_txt.append('分 minute: ' + str(int.from_bytes(minute, byteorder='little')))
        print_txt.append('间隔 interval: ' + str(int.from_bytes(interval, byteorder='little')))
        print_txt.append('横向数量 X num: ' + str(XNumGrids))
        print_txt.append('纵向数量 Y num: ' + str(YNumGrids))
        print_txt.append('纵深数量 Z num: ' + str(ZNumGrids))
        print_txt.append('拼图雷达数 Radar Count: ' + str(int.from_bytes(RadarCount, byteorder='little')))
        print_txt.append('网格开始经度 StartLon：' + str(StartLon))  # 00 00 e6 6B
        print_txt.append('网格开始纬度 StartLat：' + str(StartLat))  # 00008b
        print_txt.append('网格中心经度 CenterLon: ' + str(struct.unpack('<f', CenterLon)[0]))
        print_txt.append('网格中心纬度 CenterLat: ' + str(struct.unpack('<f', CenterLat)[0]))
        print_txt.append('经度方向分辨率 XReso：' + str(struct.unpack('<f', XReso)[0]))
        print_txt.append('纬度方向分辨率 YReso：' + str(struct.unpack('<f', YReso)[0]))
        print_txt.append('垂直方向的高度（单位km）数目根据ZnumGrids而得（最大40层）：' + str(struct.unpack('<40i', ZhighGrids)[0]))
        print_txt.append('有效站点名称：')
        print_txt.append(str_cities)
        print_txt.append('雷达站点所在经度（4x20）：')
    for i in range(4):
        str_item = str(read_item(f))
        if for_what == 'draw' or for_what == 'both':
            print_txt.append(str_item)
    if for_what == 'draw' or for_what == 'both':
        print_txt.append('雷达站点所在纬度（4x20）：')
    for i in range(4):
        str_item = str(read_item(f))
        if for_what == 'draw' or for_what == 'both':
            print_txt.append(str_item)
    print_txt.append('无用经纬度（4x20）：')
    for i in range(4):
        str_item = str(read_item(f))
        if for_what == 'draw' or for_what == 'both':
            print_txt.append(str_item)

    # f_info.close()

    MosaicFlag = f.read(20)
    # 都是0（没用）
    Reserved = f.read(172)
    if for_what == 'draw' or for_what == 'both':
        print_txt.append('该雷达数据是否包含在本次拼图中 MosaicFlag：\n' + str(list(MosaicFlag)))
        print_txt.append('Reserved：' + str(int.from_bytes(Reserved, byteorder='little')))
        bin_name = os.path.basename(f.name).split('.')[0]
        draw_swan_data(f, XNumGrids, YNumGrids, ZNumGrids, bin_name, print_txt)  # 画图
    if for_what == 'match' or for_what == 'both':
        nps = read_swan_data(f, XNumGrids, YNumGrids, ZNumGrids, file_name)  # 计算
        result = {
            'nps': nps,
            'startLon': float(StartLon),
            'startLat': float(StartLat),
            'yNum': YNumGrids,
            'xNum': XNumGrids,
        }
        return result


def draw_swan_data(f, x_num, y_num, z_num, bin_name, print_txt):
    """
    绘制图像
    """
    jpg_root_dir = 'G:/Mete_Fore/draw/'
    jpg_dir = jpg_root_dir + bin_name
    if not os.path.exists(jpg_dir):
        os.makedirs(jpg_dir)
    np.savetxt(jpg_dir + '/' + bin_name + '_head.txt', print_txt, fmt="%s")
    i_jpg_path = jpg_dir + '/' + bin_name + '_'
    max_jpg_path = jpg_dir + '/' + bin_name + '_max.jpg'
    print(max_jpg_path, 'saving')
    draw_max = np.zeros([y_num, x_num])  # 创建空的二维y×x数组
    draw_i = np.zeros([y_num, x_num])

    for z in range(z_num):
        for y in range(y_num):
            for x in range(x_num):
                item = int.from_bytes(f.read(1), byteorder='little')
                draw_i[y,x] = item
                if item > draw_max[y, x]:
                    draw_max[y, x] = item
        np.savetxt(i_jpg_path + str(z) + '.txt', draw_i, fmt="%d")
        draw_img(draw_i, i_jpg_path + str(z) + '.jpg')
    np.savetxt(i_jpg_path + '_max.txt', draw_max, fmt="%d")
    draw_img(draw_max, max_jpg_path)


def draw_img(df_source, save_jpg_path):
    """
    绘制图像
    """
    # pyplot.imshow(df_source)
    # pyplot.show()
    scipy.misc.imsave(save_jpg_path, df_source)
    print(save_jpg_path, 'saved')


def traverse_draw_data():
    """
    绘制雷达图像
    """
    path = rada_des
    flag = False
    for top, dirs, files in os.walk(path):
        for filename in files:
            if filename.startswith('.'):
                continue
            # print(os.path.join(path, filename))

            if filename.endswith('13.bin'):
                print('processing ',filename)
                read_bin(os.path.join(path, filename), 'draw_img')
            # if filename == '201308280006.bin':
            # if filename == '201308161536.bin':
            #     flag = True

def match_time(csv_time, rada_time, break_time):
    csv_df = pd.read_csv('D:/zz_Mete_Fore/2010-2013csv-4.02/all/rain_all_'+csv_time+'.csv', index_col=None,
                            header=None)
    folder = rada_des
    breakpoint_path = 'D:/zz_Mete_Fore/2010-2013csv-4.02/all/breakpoint/'
    train_data = np.zeros(22)
    train_csv = 'D:/zz_Mete_Fore/2010-2013csv-4.02/all/降水' + csv_time + 'min_雷达' + rada_time + 'min_匹配结果.csv'


    flag1 = False
    ti = 0
    for filename in os.listdir(folder):
        if filename.split('.')[0].endswith(rada_time):   # csv 和 rada 进行匹配。
            match_time = int(filename.split('.')[0]) + int(csv_time) - int(rada_time)
            if len(csv_df[csv_df.loc[:, 3] == match_time].index.tolist()) > 0:
                print('当前匹配的时间：', match_time)
                if match_time != break_time and flag1 == False:
                    ti += 1
                    print('跳过',ti)
                    continue
                flag1 = True
                result = read_bin(folder + '/' + filename, 'match')
                # print(result)
                nps = result['nps'][2:]
                startLon = result['startLon']
                startLat = result['startLat']
                for row in csv_df[csv_df.loc[:, 3] == match_time].values:
                    try:
                        # 降雨量 经/纬度
                        rainfall = int(row[4])
                        longitude = float(row[1])
                        latitude = float(row[2])
                        stationNum = row[0]
                        # 在图像上取值的位置 = (给出的经(纬)度 - 雷达起始的经(纬)度) / 0.01
                        longitudeNum = int(abs(longitude - float(startLon)) / 0.01)  # x轴上取值
                        latitudeNum = int(abs(latitude - float(startLat)) / 0.01)  # y轴上取值
                        # TODO mdf文件存在错误数据
                        # 保存某一条降雨数据对应17层矩阵上的数值数组
                        head_info = [match_time, stationNum, latitude, longitude]
                        once_trian_data = []
                        for np_item in nps:
                            item_num = np.sum(np_item[latitudeNum - 1:latitudeNum + 2, longitudeNum - 1:longitudeNum + 2]) / 9
                            once_trian_data.append(round(float(item_num), 2))
                        # 删除都为0的情况
                        if np.sum(once_trian_data) == 0:
                            continue
                        once_trian_data = head_info + once_trian_data
                        once_trian_data.append(rainfall)
                        train_data = np.vstack((train_data, once_trian_data))
                    except Exception:
                        print('Error Time：', match_time)
                        break
                break_name = breakpoint_path + datetime.datetime.now().strftime('%Y-%m-%d %H_%M_%S') + '_' + str(match_time)
                pd.DataFrame(train_data[1:]).to_csv(break_name + '.csv', index=None, columns=None, header=None)
                # 保存结果
            pd.DataFrame(train_data[1:]).to_csv(train_csv, index=None, columns=None, header=None)

        else:
            continue


def read_swan_data(f, x_num, y_num, z_num, file_name):
    """
    读取每个bin文件的实际内容
    """
    one_time_nps = []
    # 1 - 19 层
    for z in range(z_num - 2):
        curr_np = np.zeros([y_num, x_num])
        for y in range(y_num):
            for x in range(x_num):
                item = int.from_bytes(f.read(1), byteorder='little')
                curr_np[y, x] = item
        one_time_nps.append(curr_np)
    return one_time_nps


def convetTimeCallback(dateStr):
    """
    转换时间戳格式1
    """
    dateStr = str(dateStr)
    if not dateStr[0].isdigit():
        return dateStr
    dateArr = dateStr.split(' ')
    date_p1_arr = dateArr[0].split('-')
    date_p1_arr[1] = date_p1_arr[1] if len(date_p1_arr[1]) == 2 else '0' + date_p1_arr[1]
    date_p1_arr[2] = date_p1_arr[2] if len(date_p1_arr[2]) == 2 else '0' + date_p1_arr[2]
    full_time = ''.join(date_p1_arr) + ''.join(dateArr[1].split(':')[:-1])
    return full_time


def convertTimeCallback2(dateStr):
    """
    转换时间戳格式，去掉末尾的00
    """
    dateStr = str(dateStr)
    return dateStr[:-2]


def get_pure_binary():
    """
    清洗原始数据，为每一个bin文件单独创建文件夹
    原始文件路径source_folder和目标文件路径des_folder需要修改
    """
    source_folder = rada_dir
    des_folder = rada_des
    for top, dirs, files in os.walk(source_folder):
        for file in files:
            if file.startswith('.'):
                continue
            file_name = file.split('_')[-1]
            # ==============
            # 为每一个雷达文件创建单独的文件夹并保存
            # os.mkdir(des_folder + '/' + file_name.split('.')[0])
            # shutil.copyfile(os.path.join(top, file), des_folder + '/' + file_name.split('.')[0] + '/' + file_name)
            # ==============
            if file_name.endswith('4.bin'):
                shutil.copyfile(os.path.join(top, file), des_folder + '/' + file_name)


def remove_invalid(source):
    """
    过滤无用信息
    """
    station_str = ''.join(['%02X' % x for x in source]).strip()
    station_str = station_str[::-1]
    index = 0
    if station_str.count('0') == len(station_str):
        return
    for i, c in enumerate(station_str):
        if c != '0':
            index = i
            break
    cut0str = station_str[index:][::-1]
    return binascii.a2b_hex(cut0str).decode('gb18030')


def decompress_b2z():
    """
    将b2z压缩包解压为二进制文件
    """
    path = '/Users/Cortana/Desktop/16'  # bz2 folder
    new_path = '/Users/Cortana/Desktop/16_un/'  # bin folder
    for top, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(top, file)
            un_file_path = new_path + file[:-4]
            with open(un_file_path, 'wb') as new_file, bz2.BZ2File(file_path, 'rb') as bz2_file:
                for data in iter(lambda: bz2_file.read(100 * 1024), b''):
                    new_file.write(data)


def move_files():
    """
    移动文件
    """
    source_folder = '/Users/Cortana/Desktop/雷达文件'  # 原文件夹
    des_folder_17 = '/Users/Cortana/Desktop/17/'  # 目的文件夹
    for top, dirs, files in os.walk(source_folder):
        for file in files:
            if file.find('_2017') > 0:
                new_name = file.split('_')[-1]
                shutil.copyfile(os.path.join(top, file), des_folder_17 + new_name)


def gather_csv(file_name):
    """
    收集所有同类数据
    """
    path = 'D:/zz_Mete_Fore/2010-2013csv-4.02'
    csv_all = 'D:/zz_Mete_Fore/2010-2013csv-4.02/all/gather_'+file_name
    df_result = pd.DataFrame()  # 60min
    for top, dirs, files in os.walk(path):
        for filename in files:
            if filename == file_name:
                try:
                    df = pd.read_csv(os.path.join(top, filename))
                except UnicodeDecodeError:
                    continue
                df_result = df_result.append(pd.DataFrame(df.values[1:]))

    df_result.loc[:, 3] = df_result.loc[:, 3].map(convertTimeCallback2)
    # 删除无效降雨数据
    df_result = df_result[df_result.loc[:, 4] > 1]
    df_result = df_result[df_result.loc[:, 4] < 200]
    # 写入保存
    df_result.to_csv(csv_all, index=None, header=None)
    # return df_result20


def read_df(path, encodeType='utf-8'):
    """
    按照不同的encode type读取csv文件
    """
    reserve_columns = ['站点编号', '降雨量', '经度', '纬度', '世界时间（字符串）']
    rain_df = pd.DataFrame(pd.read_csv(path, encoding=encodeType), columns=reserve_columns, index=None)
    rain_df['经度'] = rain_df['经度'].fillna('null')
    rain_df = rain_df[~rain_df['经度'].isin(['null'])]
    rain_df['世界时间（字符串）'] = rain_df['世界时间（字符串）'].map(convertTimeCallback2)
    print(path.split('/')[-2], rain_df)
    return rain_df


def reformat_train_data():
    """
    重新整理训练数据集
    操作方式能更简单，太困了 不想改了
    """
    raw_result = pd.read_csv('/Users/Cortana/PycharmProjects/weather/binary/result.csv', index_col=None, header=None)
    dbz_in_resut = raw_result.loc[:, 3:19]  # 灰度值
    head_info_result = raw_result.loc[:, :2]  # 时间、经纬度
    rainfall_result = raw_result.loc[:, 20:]  # 降雨
    max_in_rows = dbz_in_resut.max(axis=1)  # 最大灰度值
    reconcat_result = pd.concat(objs=[dbz_in_resut, max_in_rows], axis=1)
    # 转换为dbz
    reconcat_result = (reconcat_result.values.astype(np.float64) - 66) / 2
    reconcat_result[reconcat_result < 0] = 0

    final_result = pd.concat(objs=[head_info_result, pd.DataFrame(reconcat_result), rainfall_result], axis=1)
    final_result.to_csv('最终数据集.csv', index=None, header=None)


def read_item(f):
    """
    气象站坐标（暂时没用）
    """
    curr_f = f.read(20)
    return list(map(lambda a: round(a, 4), struct.unpack('<5f', curr_f)))
    # return ' '.join(map(str, list(map(lambda a: round(a, 4), struct.unpack('<5f', curr_f)))))


def get_station_name(f):
    """
    获取气象站名称（暂时没用）
    """
    cities = []
    for i in range(20):
        station_raw = f.read(16)
        curr_station = remove_invalid(station_raw)
        if curr_station is None:
            continue
        cities.append(curr_station)
        # print('站点%d %s' % (i + 1, curr_station))
    return cities


if __name__ == '__main__':
    enter()
