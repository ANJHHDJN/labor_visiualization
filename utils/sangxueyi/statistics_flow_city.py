from numpy.lib.function_base import append
import pandas as pd
import sys

# import sys

from pandas.io import api
from db.db_j import read_table
import numpy as np
import json
from utils.sangxueyi.statistics_job_industry import gnrt_date

def write_data():
    list_id = []
    list_month = []
    list_city = []
    list_flow_num = []

    df = pd.read_csv('utils\sangxueyi\data\data_city.csv', usecols=[0, 1, 41, 42])
    df.columns = ['id', 'month', 'identity', 'city']
    for i in df.columns:
        df = df[~df[i].isin(['None'])]
    df = df[df['identity'].isin([1])]
    df = df.drop('identity', axis=1)
    df = df.sort_values(by=['id', 'month'])

    list_id = list(set(df['id']))
    list_month = list(set(df['month']))
    list_city = list(set(df['city']))
    flow_num = np.zeros((len(list_month), len(list_city), len(list_city)))
    flow_num_city = np.zeros((len(list_month), len(list_city), 2))

    for i in range(len(list_id)):
        df_id = df[df['id'] == list_id[i]]
        list_message = df_id.values.tolist()
        for j in range(len(list_message)-1):
            if not list_message[j][2] == list_message[j+1][2]:
                flow_num[list_month.index(list_message[j+1][1])][list_city.index(list_message[j][2])][list_city.index(list_message[j+1][2])] += 1

    for i in range(len(list_month)):
        for j in range(len(list_city)):
            for k in range(len(list_city)):
                flow_num_city[i][j][0] += flow_num[i][k][j]
                flow_num_city[i][j][1] += flow_num[i][j][k]

    list_flow_message=[]
    for i in range(len(list_month)):
        list_flow_city = []
        for j in range(len(list_city)):
            di_1 = dict(item=list_city[j], 劳动力流入=flow_num_city[i][j][0], 劳动力流出=flow_num_city[i][j][1])
            list_flow_city.append(di_1)
        di_2 = dict(month=list_month[i], data=list_flow_city)
        list_flow_message.append(di_2)
    di = dict(message=list_flow_message)


            

    jsObj = json.dumps(di, indent=4,ensure_ascii=False)  # indent参数是换行和缩进
    fileObject = open(r'utils\sangxueyi\data\flow_data.json', 'w',encoding='utf-8') 
    fileObject.write(jsObj) 
    fileObject.close()  #最终写入的json文件格式:
    print(di)

def get_labor_flow_data(month):
    year='2020'
    date=gnrt_date(year,month)
    # o_data = data_preprocess(r'utils\sangxueyi\data\fired_num_distrbtion.csv')
    o_data=read_table('labor_flow_count')
    data = o_data[o_data['month'] == date]
    # print(data)
    data=data.to_dict(orient='records')

    print(data)
    data_return=list()
    for i in data:
        # print(i)
        a=dict()
        for j in i.keys():
            # a=dict()
            if j == 'month':
                continue
            if j == 'city':
                a['item']=i[j]
            if j == 'labor_in':
                a['劳动力流入']=float(i[j])
            if j == 'labor_out_':
                a['劳动力流出']=float(i[j])
            # a[j]=j
            # a['value']=float(i[j].strip('%'))/100
        data_return.append(a)

    return data_return


# def get_labor_flow_data(month):
#     year='2020'
#     date=gnrt_date(year,month)
#     with open(r'utils\sangxueyi\data\flow_data.json','r',encoding='utf-8')as fp:
#         json_data = json.load(fp)
#         # print(json_data)

#     data_return=[]
#     for i in json_data:
#         if i['month']==date:
#             data_return=i['data']


    # return data_return

if __name__=='__main__':
    print(get_labor_flow_data('3'))
