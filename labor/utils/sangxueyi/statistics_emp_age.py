
import sys
# from utils.sangxueyi.statistics_job_industry import form_change
import pandas as pd
import numpy as np
from collections import Counter

from db.db_j import read_table
from services.employment_service import PURE_CITYS
from utils.sangxueyi.statistics_job_industry import gnrt_date

RANGE = ['18岁以下', '18-24岁', '24-35岁', '35-44岁', '44-54岁', '55岁以上']


def get_age_rate(year, month, city, data, flag):
    m1 = gnrt_date(year, month)
    m2 = gnrt_date(year, str(int(month) + 1))
    # compare_tar1=data[(data['所在城市']==city)]
    compare_tar = data[(data['月份'] == m1) | (data['月份'] == m2)]
    compare_tar = compare_tar[['序号', '月份', '年龄', '客户身份_工作情况', '所在城市']]

    # data_return=data.drop(data[(data.月份==m1)|(data.月份==m2)].index)
    id_list = dict()
    for index, row in compare_tar.iterrows():
        # print(type(row['序号']))
        if row['序号'] in id_list:
            id_list[row['序号']].append(row['客户身份_工作情况'])
        else:
            id_list[row['序号']] = [row['客户身份_工作情况']]
    fired_id_list = []
    emp_id_list = []
    for i in id_list.items():
        if len(i[1]) != 2:
            continue
    #     print(i[1][1])
        if i[1][0] == 1:
            if i[1][1] == 0:
                fired_id_list.append(i[0])
            else:
                continue
        if i[1][0] == 0:
            if i[1][1] == 1:
                emp_id_list.append(i[0])
            else:
                continue

    emp_df = compare_tar[(compare_tar['序号'].isin(emp_id_list))
                         & (compare_tar['所在城市'] == city)]
    fired_df = compare_tar[(compare_tar['序号'].isin(fired_id_list))
                           & (compare_tar['所在城市'] == city)]

    emp_age = list(emp_df['年龄'])
    fired_age = list(fired_df['年龄'])

    num_emp = len(emp_age)
    num_fired = len(fired_age)

    if flag == 0:

        l1 = 0
        l2 = 0
        l3 = 0
        l4 = 0
        l5 = 0
        l6 = 0
        for i in emp_age:
            if isinstance(i, str):
                i = int(i)
            if i <= 18:
                l1 += 1
            elif i <= 24:
                l2 += 1
            elif i <= 35:
                l3 += 1
            elif i <= 44:
                l4 += 1
            elif i <= 54:
                l5 += 1
            else:
                l6 += 1

        num_lst = [l1, l2, l3, l4, l5, l6]
        # emp_age_df=pd.DataFrame()
        # for i in range(len(RANGE)):
        #     try:
        #         emp_age_df[RANGE[i]]=["%.2f%%" % (num_lst[i]/num_emp * 100)]
        #     except:
        #         emp_age_df[RANGE[i]]=["%.2f%%" % (0 * 100)]

        for i in range(len(num_lst)):
            try:
                num_lst[i] = "%.2f%%" % (num_lst[i] / num_emp * 100)
            except:
                num_lst[i] = "%.2f%%" % (0 * 100)
        return num_lst

    else:
        l1 = 0
        l2 = 0
        l3 = 0
        l4 = 0
        l5 = 0
        l6 = 0
        for i in fired_age:
            if isinstance(i, str):
                i = int(i)
            if i <= 18:
                l1 += 1
            elif i <= 24:
                l2 += 1
            elif i <= 35:
                l3 += 1
            elif i <= 44:
                l4 += 1
            elif i <= 54:
                l5 += 1
            else:
                l6 += 1

        num_lst_2 = [l1, l2, l3, l4, l5, l6]
        # fired_age_df=pd.DataFrame()
        # for i in range(len(RANGE)):
        #     try:
        #         fired_age_df[RANGE[i]]=["%.2f%%" % (num_lst[i]/num_fired * 100)]
        #     except:
        #         fired_age_df[RANGE[i]]=["%.2f%%" % (0 * 100)]

        for i in range(len(num_lst_2)):
            try:
                num_lst_2[i] = "%.2f%%" % (num_lst_2[i] / num_fired * 100)
            except:
                num_lst_2[i] = "%.2f%%" % (0 * 100)

        return num_lst_2


def gnrt_emp_age_csv(data):
    """ 获取就业人数csv """
    year = '2020'
    date_list = []
    city_list = []
    l1 = []
    l2 = []
    l3 = []
    l4 = []
    l5 = []
    l6 = []
    for i in range(2, 8):
        i = str(i)
        for j in PURE_CITYS:
            date_list.append(gnrt_date(year, i))
            city_list.append(j)

            fired_lst = get_age_rate(year, i, j, data, 0)
            l1.append(fired_lst[0])
            l2.append(fired_lst[1])
            l3.append(fired_lst[2])
            l4.append(fired_lst[3])
            l5.append(fired_lst[4])
            l6.append(fired_lst[5])

    df = pd.DataFrame()
    df['月份'] = date_list
    df['地区'] = city_list
    df['18岁以下'] = l1
    df['18-24岁'] = l2
    df['24-35岁'] = l3
    df['35-44岁'] = l4
    df['44-54岁'] = l5
    df['55岁以上'] = l6

    df.to_csv(r'data\emp_num_distrbtion.csv',
              sep=',',
              header=True,
              index=False,
              encoding='utf-8')

    date_list = []
    city_list = []
    l1 = []
    l2 = []
    l3 = []
    l4 = []
    l5 = []
    l6 = []
    for i in range(2, 8):
        i = str(i)
        for j in PURE_CITYS:
            date_list.append(gnrt_date(year, i))
            city_list.append(j)

            fired_lst = get_age_rate(year, i, j, data, 1)
            l1.append(fired_lst[0])
            l2.append(fired_lst[1])
            l3.append(fired_lst[2])
            l4.append(fired_lst[3])
            l5.append(fired_lst[4])
            l6.append(fired_lst[5])

    df = pd.DataFrame()
    df['月份'] = date_list
    df['地区'] = city_list
    df['18岁以下'] = l1
    df['18-24岁'] = l2
    df['24-35岁'] = l3
    df['35-44岁'] = l4
    df['44-54岁'] = l5
    df['55岁以上'] = l6

    df.to_csv(r'data\fired_num_distrbtion.csv',
              sep=',',
              header=True,
              index=False,
              encoding='utf-8')


def get_emp_age_data(month):
    """ input:str """
    year='2020'
    date=gnrt_date(year,month)
    # o_data = data_preprocess(r'utils\sangxueyi\data\emp_num_distrbtion.csv')
    o_data=read_table('emp_num_month')
    data = o_data[o_data['月份'] == date].drop(['月份'],1)
    # print(data)
    data=data.to_dict(orient='records')
    data_return=list()
    for i in data:
        for j in i.keys():
            a=dict()
            a['type']=j
            a['value']=round(float(i[j].strip('%'))/100,2)
            data_return.append(a)

    return data_return

def get_fired_age_data(month):
    """ input:str """
    year='2020'
    date=gnrt_date(year,month)
    # o_data = data_preprocess(r'utils\sangxueyi\data\fired_num_distrbtion.csv')
    o_data=read_table('fired_num_month')
    data = o_data[o_data['月份'] == date].drop(['月份'],1)
    # print(data)
    data=data.to_dict(orient='records')
    data_return=list()
    for i in data:
        # print(i)
        for j in i.keys():
            a=dict()
            a['type']=j
            a['value']=round(float(i[j].strip('%'))/100,2)
            data_return.append(a)

    return data_return

def form_change_emp():
    df=pd.read_csv(r'C:\Users\HiWin10\Desktop\labor-coefficient-all\labor-coefficient-server\utils\sangxueyi\data\emp_num_distrbtion1.csv')
    li=df.to_dict(orient='records')
    li_return=list()
    for i in li:
        for j in i.keys():
            if j=='月份':
                continue
            a=dict()
            a['日期']=i['月份']
            a['年龄']=j
            a['新增就业比率']=round(float(i[j].strip('%'))/100,2)
            li_return.append(a)
    df=pd.DataFrame(li_return)
    df.to_csv(r'C:\Users\HiWin10\Desktop\labor-coefficient-all\labor-coefficient-server\utils\sangxueyi\data\emp_age.csv',
                   sep=',',
                   header=True,
                   index=False,
                   encoding='utf-8')
    # return li_return

def form_change_fired():
    df=pd.read_csv(r'C:\Users\HiWin10\Desktop\labor-coefficient-all\labor-coefficient-server\utils\sangxueyi\data\fired_num_distrbtion1.csv')
    li=df.to_dict(orient='records')
    li_return=list()
    for i in li:
        for j in i.keys():
            if j=='月份':
                continue
            a=dict()
            a['日期']=i['月份']
            a['年龄']=j
            a['新增就业比率']=round(float(i[j].strip('%'))/100,2)
            li_return.append(a)
    df=pd.DataFrame(li_return)
    df.to_csv(r'C:\Users\HiWin10\Desktop\labor-coefficient-all\labor-coefficient-server\utils\sangxueyi\data\fired_age.csv',
                   sep=',',
                   header=True,
                   index=False,
                   encoding='utf-8')



if __name__ == '__main__':
    # path = r'data\data_city.csv'
    # data = data_preprocess(path)
    # gnrt_emp_age_csv(data)
    form_change_emp()
    form_change_fired()

    # pass