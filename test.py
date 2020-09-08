"""author: yanziming"""
# 正常<早退=迟到<缺勤<年假=调休=出差<休息<加班


import os
import numpy as np
import pandas as pd
os.chdir(r'C:\Users\Jimmy\Desktop')


def get_eid_attendence(eid, data):
    """get attendence with each eid"""

    days = int(data['考勤日期'].dt.day.max())
    eid_info = data[data['工号'] == eid].reset_index(drop=True)
    a_m, p_m, overtime = [['' for _ in range(days + 3)] for _ in range(3)]
    a_m[0], p_m[0], overtime[0] = '上午', '下午', '加班工时'

    def fill(keyword, str1, str2):
        def choose_to_fill():
            if str1 == '':
                p_m[date] = str2
            elif str2 == '':
                a_m[date] = str1
            else:
                a_m[date], p_m[date] = str1, str2

        for date in range(1, days + 1):
            for col in eid_info.columns[eid_info.columns.str.contains(keyword)]:
                if eid_info[col].notnull()[date - 1]:
                    choose_to_fill()


    # 正常出勤
    fill('上班1', '√', '')
    fill('下班1', '', '√')

    # 出差(假设出差出一整天，不考虑上下午)
    fill('出差', '出', '差')

    # 年假
    fill('年休假', '年', '假')

    # 调休
    fill('调休', '调', '休')

    # 正常休息
    # fill('应出勤', '休', '息')
    for date in range(1, days + 1):
        if eid_info['应出勤时数'][date - 1] == 0:
            a_m[date] = '休'
            p_m[date] = '息'

    eid_attendence = pd.DataFrame(
        [a_m, p_m, overtime],
        index=[eid for _ in range(3)],
        columns=list(range(days + 1)) + ['正常出勤'] + ['周末加班工时']
    )

    return eid_attendence


def get_all_attendence(eid_list, data):
    """get all attendence with eid_list"""

    all_attendence = pd.DataFrame()
    for eid in eid_list:
        try:
            all_attendence = pd.concat(
                [all_attendence, get_eid_attendence(eid, data)])
        except KeyError:
            print(f'工号 {eid} 有问题')
    return all_attendence


EIDs = pd.read_excel(
    '考勤表.xlsx',
    sheet_name='办公室 ',
    header=2,
    converters={'员工编号': str}
)['员工编号'].drop_duplicates(keep=False)

rawdata = pd.read_excel(
    '考勤日报表.xlsx',
    header=6,
    converters={'工号': str, '考勤日期': np.datetime64}
)

info = get_all_attendence(EIDs, rawdata)

with pd.ExcelWriter('test.xlsx') as writer:  # pylint: disable=abstract-class-instantiated
    info.to_excel(writer)

os.system('pause')
