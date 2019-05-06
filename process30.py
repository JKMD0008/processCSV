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

rada_dir = 'G:/Mete_Fore/SWAN_RADAMOSAIC_PRODUCTS'
rada_des = 'G:/Mete_Fore/rada_des'

def read_bin(path):
    """
    读取二进制文件
    """
    # 获取文件名
    file_name = path.split('/')[-1].split('.')[0]
    f = open(path, 'rb')
    zon_name = f.read(12)
    info = remove_invalid(f.read(38))
    # info = f.read(38)
    title = remove_invalid(f.read(8))
    # title = f.read(8)
    version = f.read(8)
    # print('文件名称：', zon_name.decode('utf-8'))
    # print('文件说明：', info)
    # print('文件标志：', title)
    # print('文件版本：', version.decode('utf-8'))
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
    # print('年 year: ', int.from_bytes(year, byteorder='little'))
    # print('月 month: ', int.from_bytes(month, byteorder='little'))
    # print('天 day: ', int.from_bytes(day, byteorder='little'))
    # print('小时 hour: ', int.from_bytes(hour, byteorder='little'))
    # print('分 minute: ', int.from_bytes(minute, byteorder='little'))
    # print('间隔 interval: ', int.from_bytes(interval, byteorder='little'))
    XNumGrids = int.from_bytes(XNumGrids, byteorder='little')
    # print('横向数量 X num: ', XNumGrids)
    YNumGrids = int.from_bytes(YNumGrids, byteorder='little')
    # print('纵向数量 Y num: ', YNumGrids)
    ZNumGrids = int.from_bytes(ZNumGrids, byteorder='little')
    # print('纵深数量 Z num: ', ZNumGrids)
    # print('拼图雷达数 Radar Count: ', int.from_bytes(RadarCount, byteorder='little'))

    StartLon = struct.unpack('<f', StartLon)[0]
    # print('网格开始经度 StartLon：', StartLon)  # 00 00 e6 6B
    StartLat = struct.unpack('<f', StartLat)[0]
    # print('网格开始纬度 StartLat：', StartLat)  # 00008b
    # print('网格中心经度 CenterLon: ', struct.unpack('<f', CenterLon)[0])
    # print('网格中心纬度 CenterLat: ', struct.unpack('<f', CenterLat)[0])
    # print('经度方向分辨率 XReso：', struct.unpack('<f', XReso)[0])
    # print('纬度方向分辨率 YReso：', struct.unpack('<f', YReso)[0])
    # print('垂直方向的高度（单位km）数目根据ZnumGrids而得（最大40层）：', struct.unpack('<40i', ZhighGrids)[0])

    # print('有效站点名称：')
    get_station_name(f)

    # print('雷达站点所在经度（4x20）：')
    for i in range(4):
        read_item(f)

    for i in range(4):
        read_item(f)

    for i in range(4):
        read_item(f)

    # f_info.close()

    MosaicFlag = f.read(20)
    # print('该雷达数据是否包含在本次拼图中 MosaicFlag：\n', *list(MosaicFlag))

    # 都是0（没用）
    Reserved = f.read(172)
    # print('Reserved：', int.from_bytes(Reserved, byteorder='little'))

    # draw_swan_data(f, XNumGrids, YNumGrids, ZNumGrids, file_name) # 画图
    nps = read_swan_data(f, XNumGrids, YNumGrids, ZNumGrids, file_name)  # 计算
    result = {
        'nps': nps,
        'startLon': float(StartLon),
        'startLat': float(StartLat),
        'yNum': YNumGrids,
        'xNum': XNumGrids,
    }
    return result


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


def read_item(f):
    """
    气象站坐标（暂时没用）
    """
    curr_f = f.read(20)
    # print(*list(map(lambda a: round(a, 4), struct.unpack('<5f', curr_f))), '\n')
    # return ' '.join(map(str, list(map(lambda a: round(a, 4), struct.unpack('<5f', curr_f)))))


def get_station_name(f):
    """
    获取气象站名称（暂时没用）
    """
    for i in range(20):
        station_raw = f.read(16)
        curr_station = remove_invalid(station_raw)
        if curr_station is None:
            continue
        # cities.append(curr_station)
        # print('站点%d %s' % (i + 1, curr_station))
    # return cities


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
    return binascii.a2b_hex(cut0str).decode('gb2312')


def read_rain_20and30():
    """
    读取降水mdf数据并和雷达数据文件进行匹配 20、30分钟
    """
    rain_df30 = pd.read_csv('/Users/Cortana/PycharmProjects/weather/binary/2010-2013年第30分钟有雨数据集.csv', index_col=None,
                            header=None)
    folder = rada_des
    breakpoint_path = 'G:/Mete_Fore/breakpoint'
    train_data = np.zeros(21)
    for filename in os.listdir(folder):
        if filename.split('.')[0].endswith('30'):
            time30 = int(filename.split('.')[0])
            if len(rain_df30[rain_df30.loc[:, 3] == time30].index.tolist()) > 0:
                print('当前匹配的时间（20）：', time30)
                result = read_bin(folder + '/' + filename)
                nps = result['nps'][2:]
                startLon = result['startLon']
                startLat = result['startLat']
                for row in rain_df30[rain_df30.loc[:, 3] == time30].values:
                    try:
                        # 降雨量 经/纬度
                        rainfall = int(row[4])
                        longitude = float(row[1])
                        latitude = float(row[2])
                        # 在图像上取值的位置 = (给出的经(纬)度 - 雷达起始的经(纬)度) / 0.01
                        longitudeNum = int(abs(longitude - float(startLon)) / 0.01)  # x轴上取值
                        latitudeNum = int(abs(latitude - float(startLat)) / 0.01)  # y轴上取值
                        # TODO mdf文件存在错误数据
                        # 保存某一条降雨数据对应17层矩阵上的数值数组
                        head_info = [time30, latitude, longitude]
                        once_trian_data = []
                        for np_item in nps:
                            once_trian_data.append(np_item[latitudeNum, longitudeNum])
                        # 删除都为0的情况
                        if np.sum(once_trian_data) == 0:
                            continue
                        once_trian_data = head_info + once_trian_data
                        once_trian_data.append(rainfall)
                        train_data = np.vstack((train_data, once_trian_data))
                    except Exception:
                        print('Error Time：', time30)
                        break
                break_name = breakpoint_path + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '_' + str(time30)
                pd.DataFrame(train_data[1:]).to_csv(break_name + '.csv', index=None, columns=None, header=None)
                # 保存结果
            pd.DataFrame(train_data[1:]).to_csv('20-30分钟匹配结果.csv', index=None, columns=None, header=None)

        else:
            continue


def get_pure_binary():
    """
    清洗原始数据，为每一个bin文件单独创建文件夹
    原始文件路径source_folder和目标文件路径des_folder需要修改
    """
    # source_folder = '/Users/Cortana/Desktop/SWAN_RADAMOSAIC_PRODUCTS'
    # des_folder = '/Users/Cortana/PycharmProjects/weather/data/_des_2010'
    source_folder = rada_dir
    des_folder = rada_des
    for top, dirs, files in os.walk(source_folder):
        for file in files:
            if file.startswith('.'):
                continue
            file_name = file.split('_')[-1]
            print(file_name)
            # ==============
            # 为每一个雷达文件创建单独的文件夹并保存
            # os.mkdir(des_folder + '/' + file_name.split('.')[0])
            # shutil.copyfile(os.path.join(top, file), des_folder + '/' + file_name.split('.')[0] + '/' + file_name)
            # ==============
            copy_file = des_folder + '/' + file_name
            if not os.path.exists(copy_file):
                if file_name.endswith('.bin'):
                    shutil.copyfile(os.path.join(top, file), copy_file)
            else:
                print('pass')


if __name__ == '__main__':
    # get_pure_binary()
    read_rain_20and30()
