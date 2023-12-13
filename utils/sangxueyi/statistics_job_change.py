import os
from db.db_j import read_table
import pandas as pd

df = pd.read_csv(r'data\job_num.csv')
# MONTHS中存取所有出现的月份
months = df['月份'].drop_duplicates().tolist()
MONTHS = list({}.fromkeys(months).keys())
# AREAS中存取所有出现的地区
areas = df['地区'].drop_duplicates().tolist()
AREAS = list({}.fromkeys(areas).keys())
areas_num = len(AREAS)
total_messages = len(df)
# 把同一个地区按月份把工作变化量整合到一起
# [{'name': '昆明市', 'job_num': [5639, 6085, 6385, 7107, 7809, 8488]}]
def getJobNum(df,areas_num,total,job_col,city_col):
    city_job = []

    for i in range(areas_num):
        job_num = []
        for j in range(i,total,areas_num):
            num = df.iloc[j,job_col]
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

lost_jobs = getJobNum(df,areas_num,total_messages,2,1)
has_jobs = getJobNum(df,areas_num,total_messages,3,1)
total_has_job = cacluate_change_num('job_num','name',has_jobs)
total_lost_job = cacluate_change_num('job_num','name',lost_jobs)
total = combine_get_lost(total_has_job,total_lost_job,'change_add_num','change_lost_num')
final = pd.DataFrame(total)

final.to_csv(r'data\job_num_change.csv',
              sep=',',
              header=True,
              index=False,
              encoding='utf-8')