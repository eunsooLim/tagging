# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import csv

dataframe = pd.read_csv("DSAM24_PM2_LDS2.csv")
datafra=dataframe
dataframe = dataframe.dropna()  # 데이터 없는 row제거
dataframe = dataframe.drop('Unnamed: 0', axis=1)  # 시간 열 제거

array_dataframe = dataframe.values


def select_Event_label_0to3(frequency_dic):
    f500 = np.asarray(frequency_dic[500])  # 500HZ근처에 존재하는 (Hz, g√Hz) 값들의 모임
    f1000 = np.asarray(frequency_dic[1000])  # 예: [(960,0.25),(964,1.35),(970,2.33),,,,,]
    f1500 = np.asarray(frequency_dic[1500])
    f2000 =np.asarray(frequency_dic[2000])
    EventLabel = []
    ###############frequency 500####################
    # f500[0:, 0] => 주파수 Hz
    # f500[:, 1] => g√Hz
    if (f500[:, 1] >= f500[0:, 0] * 0.029).sum() > 0:
        EventLabel.append(3)  # 빨간 위험선을 넘는 경우가 하나라도 있으면 레이블3
    else:
        if (f500[:, 1] >= f500[0:, 0] * 0.018).sum() > 0 or (f500[:, 1] >= f500[0:, 0] * 0.018 - 1.2).sum() > 2:
            EventLabel.append(2)  # 노란선을 넘는 경우가 하나라도 있거나, 넘지 않아도 그근방에 있는 경우가 3번이상인 경우
        else:
            if (f500[:, 1] >= f500[0:, 0] * 0.0025).sum() > 1:
                EventLabel.append(1)
            else:
                EventLabel.append(0)
    ###############frequency 1000####################
    if (f1000[:, 1] >= f1000[0:, 0] * 0.029 - 2).sum() > 0:
        EventLabel.append(3)
    else:
        if (f1000[:, 1] >= f1000[0:, 0] * 0.018 - 4.2).sum() > 0:
            EventLabel.append(2)
        else:
            if (f1000[:, 1] >= f1000[0:, 0] * 0.0028).sum() > 1:
                EventLabel.append(1)
            else:
                EventLabel.append(0)
    ###############frequency 1500####################
    if (f1500[:, 1] >= f1500[0:, 0] * 0.029 - 5).sum() > 0:
        EventLabel.append(3)
    else:
        if (f1500[:, 1] >= f1500[0:, 0] * 0.018 - 7.2).sum() > 0:
            EventLabel.append(2)
        else:
            if (f1500[:, 1] >= f1500[0:, 0] * 0.0030).sum() > 1:
                EventLabel.append(1)
            else:
                EventLabel.append(0)
    ###############frequency 2000####################
    if (f2000[:, 1] >= f2000[0:, 0] * 0.029 - 10).sum() > 0:
        EventLabel.append(3)
    else:
        if (f2000[:, 1] >= f2000[0:, 0] * 0.018 - 9.2).sum() > 0:
            EventLabel.append(2)
        else:
            if (f2000[:, 1] >= f2000[0:, 0] * 0.0032).sum() > 2:
                EventLabel.append(1)
            else:
                EventLabel.append(0)

    return EventLabel



if __name__ == '__main__':

    column = {}
    column_reverse = {}
    for k, dd in enumerate(dataframe.columns):
        column[k] = int(dd)
        column_reverse[int(dd)] = k

    #500피크는 450HZ~650HZ에 있는 값들을 모아서 조사 (나머지 피크도 같은 형식)
    Hz_index_dic={500:(450,650),1000:(950,1100),1500:(1450,1620),2000:(1950,2100)}
    Hz_index={}
    for Hz,Hz_value in Hz_index_dic.items(): #
        Hz_index[Hz] = (map(int,filter(lambda x: int(x) > Hz_value[0] and int(x) < Hz_value[1], dataframe.columns)))
        Hz_index_dic[Hz]=(column_reverse[Hz_index[Hz][0]],column_reverse[Hz_index[Hz][-1]])

    print "\n각 피크에서 조사할 주파수들 : "
    for peak,hz_set in Hz_index.items():
        print peak
        print hz_set
    print "\n각 피크 조사할 시작 index와 끝index "
    print "\nHz_index_dic : ",Hz_index_dic

    event_label_df = pd.DataFrame(columns=["Event Label"])

    for i, list in enumerate(array_dataframe):
        #피크별 근처 주파수들의 (Hz, g√Hz) 모음을 할당
        frequency_dic = {500: [], 1000: [], 1500: [], 2000: []}
        frequency_dic[500]=(zip(Hz_index[500],list[Hz_index_dic[500][0]:Hz_index_dic[500][1]+1]))
        frequency_dic[1000]=(zip(Hz_index[1000],list[Hz_index_dic[1000][0]:Hz_index_dic[1000][1]+1]))
        frequency_dic[1500]=(zip(Hz_index[1500],list[Hz_index_dic[1500][0]:Hz_index_dic[1500][1]+1]))
        frequency_dic[2000]=(zip(Hz_index[2000],list[Hz_index_dic[2000][0]:Hz_index_dic[2000][1]+1]))

        event_label_df.loc[i] = [str(select_Event_label_0to3(frequency_dic))]

    resultcsv=open("resultcsv.csv","wb")
    event_label_df['time']=datafra['Unnamed: 0']
    event_label_df=event_label_df.set_index('time')
    event_label_df.to_csv(resultcsv, encoding='utf-8')
    print "\ndone"