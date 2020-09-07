import os
import pandas as pd
import numpy as np
os.chdir(r'C:\Users\04895\Desktop')

rawdata = pd.read_excel('考勤日报表.xlsx', header=6, converters={
                        '工号': str, '考勤日期': np.datetime64})

length = int(rawdata['考勤日期'].dt.day.max())

am, pm, overtime = [['' for _ in range(length+1)] for _ in range(3)]

data = rawdata[rawdata['工号'] == '05096'].reset_index(drop=True)

# 正常出勤
for i in range(length):
    if data['实出勤时数'][i] == 8:
        am[i] = pm[i] = '√'
        # am[-1] = pd.value_counts(am)['√']

# 正常休息
for i in range(length):
    if data['应出勤时数'][i] == 0:
        am[i] = pm[i] = '休息'

# 出差(假设出差出一整天，不考虑上下午)
for i in range(length):
    if data['省内出差时数'].notnull()[i] or data['省外出差天数'].notnull()[i] or data['国外出差天数'].notnull()[i]:
        am[i] = pm[i] = '出差'

# 调休


print(data['省内出差时数'])
