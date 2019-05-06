import pandas as pd
import os
import _thread

directory = 'D:/zz_Mete_Fore/2010-2013csv-3.29'


def x_3sub2_2sub1(csv_file, csv_new_file, x, key, col_sub):  # 去掉不连续的
    df = pd.read_csv(csv_file)
    j = 1
    all = df.shape[0]
    nok = 0
    for index, row in df.iterrows():
        if j == 6:
            j = 0
        i = int(str(df.loc[index, 'ObservTimes'])[10:11])   # 2012，0719，2010
        if i == j:
            j += 1
        elif i == 1:
            j = 1
        else:
            nok += 1
            print(df.loc[index, key], '-', str(df.loc[index, 'ObservTimes']),'×', nok, 'i=', i, 'j=',j,'index=',index,'/',all)
            j = 1
            df.drop(index,inplace=True)
    df.to_csv(csv_new_file,index=False,header=True,mode='w')

    #     df = pd.read_csv(csv_file)
    #     df.drop(index=0, inplace=True)
    #     df.reset_index(inplace=True, drop=True)
    #     j = x
    #     for index, row in df.iterrows():
    #         if index == 0:
    #             print(df.loc[index, key])
    #             continue
    #         if index == df.shape[0]:
    #             break
    #         if df.loc[index, key] == df.loc[index - 1, key]:
    #             continue
    #         else:
    #             if index != 0:
    #                 print(df.loc[index, key])
    #                 df.drop(index=index, inplace=True)
    #                 df.reset_index(inplace=True, drop=True)
    #     # df.to_csv(csv_new_file, index=False, header=1, mode='w')

'''
             if (index + 1) % j == 0:
                i = j
                k = 0
                while i - 1 > 0:
                    if str(df.loc[index - 1 - k, col_sub]).isdigit() and str(df.loc[index - k, 'ObservTimes'])[10:] != '1000':
                        if str(df.loc[index - k, col_sub]).isdigit():
                            print(df.loc[index - k, key], '-', df.loc[index - k, 'ObservTimes'],'-',df.loc[index - k -1, 'ObservTimes'])
                            df.loc[index - k, col_sub] = int(df.loc[index - k, col_sub]) - int(df.loc[index - k - 1, col_sub])
                    else:
                        df.loc[index - k, col_sub] = 'error'
                    i -= 1
                    k += 1
'''


def drop_col(csv_file, csv_new_file, columns):
    df = pd.read_csv(csv_file)
    df[columns].to_csv(csv_new_file,index=0, header=1, mode='w')


def subpre_123450(csv_file, csv_new_file):  #做减法
    df = pd.read_csv(csv_file)
    i = 0
    head = df.columns.values.tolist()
    # print(head)
    df_1 = pd.DataFrame(columns=head)
    df_2 = pd.DataFrame(columns=head)
    for index, row in df.iterrows():
        shape = df.shape[0]
        s = df_1.shape[0]
        r = int(str(row[3])[10:11])
        # print(s+1,r)
        if r == s + 1:
            df_1.loc[s] = row
        elif s == 5 and r == 0:
            df_1.loc[s] = row
            temp = df_2
            if str(df_1.loc[5, 'Precipitation']).isdigit() and int(df_1.loc[5, 'Precipitation']) == 0:
                df_1.loc[5, 'Precipitation'] = 0
                df_1.loc[4, 'Precipitation'] = 0
                df_1.loc[3, 'Precipitation'] = 0
                df_1.loc[2, 'Precipitation'] = 0
                df_1.loc[1, 'Precipitation'] = 0
                df_1.loc[0, 'Precipitation'] = 0
            else:
                if str(df_1.loc[5, 'Precipitation']).isdigit() and str(df_1.loc[4, 'Precipitation']).isdigit():
                    df_1.loc[5, 'Precipitation'] = int(df_1.loc[5, 'Precipitation']) - int(df_1.loc[4, 'Precipitation'])
                else:
                    df_1.loc[5, 'Precipitation'] = 'error'
                if str(df_1.loc[4, 'Precipitation']).isdigit() and str(df_1.loc[3, 'Precipitation']).isdigit():
                    df_1.loc[4, 'Precipitation'] = int(df_1.loc[4, 'Precipitation']) - int(df_1.loc[3, 'Precipitation'])
                else:
                    df_1.loc[4, 'Precipitation'] = 'error'
                if str(df_1.loc[3, 'Precipitation']).isdigit() and str(df_1.loc[2, 'Precipitation']).isdigit():
                    df_1.loc[3, 'Precipitation'] = int(df_1.loc[3, 'Precipitation']) - int(df_1.loc[2, 'Precipitation'])
                else:
                    df_1.loc[3, 'Precipitation'] = 'error'
                if str(df_1.loc[2, 'Precipitation']).isdigit() and str(df_1.loc[1, 'Precipitation']).isdigit():
                    df_1.loc[2, 'Precipitation'] = int(df_1.loc[2, 'Precipitation']) - int(df_1.loc[1, 'Precipitation'])
                else:
                    df_1.loc[2, 'Precipitation'] = 'error'
                if str(df_1.loc[1, 'Precipitation']).isdigit() and str(df_1.loc[0, 'Precipitation']).isdigit():
                    df_1.loc[1, 'Precipitation'] = int(df_1.loc[1, 'Precipitation']) - int(df_1.loc[0, 'Precipitation'])
                else:
                    df_1.loc[1, 'Precipitation'] = 'error'
                if str(df_1.loc[0, 'Precipitation']).isdigit():
                    df_1.loc[0, 'Precipitation'] = int(df_1.loc[0, 'Precipitation'])
                else:
                    df_1.loc[0, 'Precipitation'] = 'error'
                print(index, '/', shape)
            df_2 = temp.append(df_1, ignore_index=True)
            df_1 = pd.DataFrame(columns=head)

        else:
            print('what? df_1=', df_1, 'row=', row)
            print('index=', index,'all=', all)
    df_2.to_csv(csv_new_file,index=False,header=True,mode='w')


def sub30_20_10(csv_file, csv_new_file):
    df = pd.read_csv(csv_file)
    i = 0
    head = df.columns.values.tolist()
    # print(head)
    df_1 = pd.DataFrame(columns=head)
    df_2 = pd.DataFrame(columns=head)
    for index, row in df.iterrows():
        shape = df.shape[0]
        s = df_1.shape[0]
        r = int(str(row[3])[10:11])
        # print(s+1,r)
        if r == s + 1 and s != 2:
            df_1.loc[s] = row
        elif s == 2:
            df_1.loc[s] = row
            temp = df_2
            if str(df_1.loc[2, 'Precipitation']).isdigit() and int(df_1.loc[2, 'Precipitation']) == 0:
                df_1.loc[2, 'Precipitation'] = 0
                df_1.loc[1, 'Precipitation'] = 0
            else:
                print(index, '/', shape)
                if str(df_1.loc[2, 'Precipitation']).isdigit() and str(df_1.loc[1, 'Precipitation']).isdigit():
                    df_1.loc[2, 'Precipitation'] = int(df_1.loc[2, 'Precipitation']) - int(df_1.loc[1, 'Precipitation'])
                else:
                    df_1.loc[2, 'Precipitation'] = 'error'
                if str(df_1.loc[1, 'Precipitation']).isdigit() and str(df_1.loc[0, 'Precipitation']).isdigit():
                    df_1.loc[1, 'Precipitation'] = int(df_1.loc[1, 'Precipitation']) - int(df_1.loc[0, 'Precipitation'])
                else:
                    df_1.loc[1, 'Precipitation'] = 'error'
            df_2.to_csv(csv_new_file, index=False, header=True, mode='a')
            df_1 = pd.DataFrame(columns=head)
        else:
            print('what? df_1=', df_1, 'row=', row)
            print('index=', index,'all=', shape)
    df_2.to_csv(csv_new_file, index=False, header=True, mode='w')


thr = 0
for dir_path, dir_name, file_names in os.walk(directory):
    for file_name in file_names:
        if file_name == 'All_short_123450.csv':
            thr += 1
            csv_file_in = os.path.join(dir_path, file_name)
            file_name_1 = 'All_10_60min_sub' + '.csv'
            csv_file_out = os.path.join(dir_path, file_name_1)

            if thr == 1:
                print('processing ' + csv_file_in)
                # sub30_20_10(csv_file_in,csv_file_out)
                subpre_123450(csv_file_in,csv_file_out)
            else:
                print('pass ' + csv_file_in)
            # _thread.start_new_thread(sub30_20_10,(csv_file_in,csv_file_out))