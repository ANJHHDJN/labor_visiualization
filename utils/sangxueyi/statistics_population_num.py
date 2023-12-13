import os

import sys
sys.path.append(r'C:\Users\HiWin10\Desktop\labor-coefficient-all\labor-coefficient-server')
from utils import web_util, file_util
import random

from constant.area_dict import area_to_code
from entity.vo.defined_class import Map
from utils import string_util
from resources import app_conf


import os
from db.db_j import read_table
import pandas as pd
# 第一列是月份，第二列是城市，第三列是未就业人数，第四列是就业人数
# df = pd.read_csv(r'utils\sangxueyi\data\job_num.csv')
# MONTHS中存取所有出现的月份
df=read_table('job_num')
months = df['月份'].drop_duplicates().tolist()
MONTHS = list({}.fromkeys(months).keys())

# for i in range(len(MONTHS)):
#     MONTHS[i]=int(MONTHS[i])

# print(MONTHS)
# AREAS中存取所有出现的地区
areas = df['地区'].drop_duplicates().tolist()
# print(df)

AREAS = list({}.fromkeys(areas).keys())
areas_num = len(AREAS)
total_messages = len(df)

def get_data_total(month):
    # month = int(month)
    total = []
    for i in range(total_messages):
        if df.iloc[i][0] == month:
            total.append({'name':'就业','月份':df.iloc[i][1],'月均降雨量':int(df.iloc[i][3])})
            total.append({'name':'失业','月份':df.iloc[i][1],'月均降雨量':int(df.iloc[i][2])})
    return total

# 把同一个地区按月份把工作变化量整合到一起
# [{'name': '昆明市', 'job_num': [5639, 6085, 6385, 7107, 7809, 8488]}]
def getJobNum(df,areas_num,total,job_col,city_col):
    city_job = []

    for i in range(areas_num):
        job_num = []
        for j in range(i,total,areas_num):
            num = int(df.iloc[j,job_col])
            job_num.append(num)
        city_job.append({'name':df.iloc[i,city_col],'job_num':job_num})
    return city_job

# 计算不同月份之间工作数量的改变值
def cacluate_change_num(num_str,name_str,lost_jobs):
    change_list = []
    for i in lost_jobs:
        add_num_list = []
        num = len(i[num_str])
        for j in range(num - 1):
            add_num = i[num_str][j+1] - i[num_str][j]
    #         print(add_num)
            add_num_list.append(add_num)
        change_list.append({'name':i[name_str],'change_add_num':add_num_list})
    return change_list

# 把数据按照月份，城市名称，就业改变量，失业改变量整合到一起
def combine_get_lost(total_has_job,total_lost_job,has_col,lost_col):
    lostjob = []
    for i in total_lost_job:
        lostjob.append(i[has_col])
    n = len(lostjob)
    for i in range(n):
        total_has_job[i][lost_col] = lostjob[i]
    total = []
# for month in months:
    for i in total_has_job:
        for j in range(len(MONTHS)-1):
            total.append({'month':j,'name':i['name'],'get_job_add':i[has_col][j],'lost_job_add':i[lost_col][j]})
#     num = len(total)
    for i in range(len(total)):
        total[i]['month'] = months[total[i]['month']]
    return total

def get_data_change(month):
    # month = int(month)
    lost_jobs = getJobNum(df,areas_num,total_messages,2,1)
    has_jobs = getJobNum(df,areas_num,total_messages,3,1)
    # print(lost_jobs)
    total_has_job = cacluate_change_num('job_num','name',has_jobs)
    total_lost_job = cacluate_change_num('job_num','name',lost_jobs)
    total = combine_get_lost(total_has_job,total_lost_job,'change_add_num','change_lost_num')
    # print(total)
    data = []
    view_need = []
    # for month in MONTHS:
    #     view_need = []
    #     for i in total:
    #         if i['month'] == month:
    #             view_need.append({'name':'就业','月份':i['name'],'月均降雨量':i['get_job_add']})
    #             view_need.append({'name':'失业','月份':i['name'],'月均降雨量':i['lost_job_add']})
    #     data.append({'month':month,'data':view_need})
    for i in total:
        if i['month'] == month:
            view_need.append({'name': '就业', '月份': i['name'], '月均降雨量': int(i['get_job_add'])})
            view_need.append({'name': '失业', '月份': i['name'], '月均降雨量': int(i['lost_job_add'])})
    # data.append({'month': month, 'data': view_need})
    # print(view_need)
    return view_need

# year_month = '202002'
def get_population_data(month_year):
    if not string_util.all_is_empty(month_year):
        return get_data_total(month_year)
    else:
        return "请求参数格式错误"

def  get_population_change_data(month_year):
    '''
    :author 江帆
    就业人口改变量估计
    :return: 就业率数据格式
     数据格式：const data = [{name: 'London',月份: 'Jan.',月均降雨量: 18.9,},{name: 'London',月份: 'Feb.',月均降雨量:}]
    '''

    if not string_util.all_is_empty(month_year):
        return get_data_change(month_year)
    else:
        return "请求参数格式错误"



if __name__ == '__main__':
     print(get_population_data('202002'))
     print(get_population_change_data('202003'))
