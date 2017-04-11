# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

dataframe = pd.read_csv("DSAM24_PM2_LDS2.csv")

dataframe = dataframe.drop('Unnamed: 0', axis=1)  # 시간 열 제거
dataframe = dataframe.dropna()  # 데이터 없는 row제거

array_dataframe = dataframe.values
textfiile = open("result.txt", "w")


def select_Event_label_0_3(frequency_dic):
    f500 = np.asarray(frequency_dic[500])  # 500HZ근처에 존재하는 (Hz, g√Hz) 값들의 모임
    f1000 = np.asarray(frequency_dic[1000])  # 예: [(960,0.25),(964,1.35),(970,2.33),,,,,]
    f1500 = np.asarray(frequency_dic[1500])
    f2000 = np.asarray(frequency_dic[2000])
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


column = {}
col = dataframe.columns
for k, dd in enumerate(col):
    column[k] = int(dd)

for i, list in enumerate(array_dataframe):

    frequency_dic = {500: [], 1000: [], 1500: [], 2000: []}

    for k, value in enumerate(list):
        Hz = column[k]
        if Hz > 450 and Hz < 620:  # 500HZ 근처의 데이터들 모으기 ( Hz, g√Hz) 형식
            frequency_dic[500].append([Hz, value])
        elif Hz > 950 and Hz < 1130:  # 1000HZ
            frequency_dic[1000].append([Hz, value])
        elif Hz > 1450 and Hz < 1600:  # 1500HZ
            frequency_dic[1500].append([Hz, value])
        elif Hz > 1950 and Hz < 2100:  # 2000HZ
            frequency_dic[2000].append([Hz, value])

    textfiile.write(str(select_Event_label_0_3(frequency_dic)))
    textfiile.write("\n") #엑셀에서 text데이터 불러오기로 업로드 하면 됨
