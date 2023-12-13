import pandas as pd
import numpy as np
import operator
import sys

from functools import reduce

from db.db_j import read_table

PURE_CITYS = [
    '昆明市', '曲靖市', '玉溪市', '保山市', '昭通市', '丽江市', '普洱市', '临沧市', '德宏州', '怒江州',
    '迪庆州', '大理州', '楚雄州', '红河州', '文山州', '西双版纳州'
]


def data_preprocess(path):
    """ 生成数据帧，添加本月所在城市 """
    data = pd.read_csv(path)
    # testdata = data[:100]
    # data.sort_values(by=['月份'], ascending=True, inplace=True)

    # 确定本月所在城市
    # city_data = data[['序号', '活动区域1_城市', '活动区域2_城市', '活动区域3_城市']]
    # city_lst = []
    # for index, row in city_data.iterrows():
    #     c1 = row["活动区域1_城市"]
    #     c2 = row['活动区域2_城市']
    #     c3 = row['活动区域3_城市']
    #     lst = [c1, c2, c3]

    #     num=len(set(lst))
    #     if num == 3:
    #         city_lst.append(c1)
    #     else:
    #         city_lst.append(max(lst, key=lst.count))

    # # data['就业情况'] = ''
    # data['所在城市'] = city_lst

    # data.to_csv(r'data\data_city.csv',
    #           sep=',',
    #           header=True,
    #           index=False,
    #           encoding='utf-8')
    print('Data Ready')
    return data


def gnrt_date(year, month):
    """ 返回查询用的日期 str
        输入：str
    """
    if len(month) == 1:
        month = '0' + month
    sdate = year + month

    return sdate


def srch_emp_by_date(year, month, area, data):
    """ 返回对应年月地区的就业/未就业人数 """
    # 每个月全省的就业情况
    sdate = gnrt_date(year, month)
    test_month = data[(data['月份'] == sdate)]
    unemp_num = len(test_month[(test_month['客户身份_工作情况'] == 0)
                               & (test_month['所在城市'] == area)])
    emp_num = len(test_month[(test_month['客户身份_工作情况'] == 1)
                             & (test_month['所在城市'] == area)])
    return emp_num, unemp_num


def gnrt_emp_csv(data):
    """ 获取就业人数csv """
    year = '2020'
    date_list = []
    city_list = []
    unemp_list = []
    emp_list = []
    for i in range(1, 13):
        i = str(i)
        for j in PURE_CITYS:
            date_list.append(gnrt_date(year, i))
            city_list.append(j)
            emp_num, unemp_num = srch_emp_by_date(year, i, j, data)
            emp_list.append(emp_num)
            unemp_list.append(unemp_num)
    df = pd.DataFrame()
    df['月份'] = date_list
    df['地区'] = city_list
    df['未就业人数'] = unemp_list
    df['就业人数'] = emp_list

    df.to_csv(r'data\job_num.csv',
              sep=',',
              header=True,
              index=False,
              encoding='utf-8')


def gnrt_indus_type(data):
    """ 提取行业类别 """
    industry_df = data[['集团行业类别']]
    industry_list = np.array(industry_df).tolist()

    new_numbers = []
    for x in industry_list:
        if x not in new_numbers:
            new_numbers.append(x)

    industry = reduce(operator.add, new_numbers)
    return industry


def indus_sta(year, month, city, data):
    """ 统计行业人数 
        data:[{}]
        """
    # data=data[['月份','集团行业类别','所在城市']].to_dict(orient='records')
    # data=data[:100]
    # data
    industry = {}
    for i in data:
        if i['集团行业类别'] in industry:
            continue
        industry[i['集团行业类别']] = 0

    date1 = gnrt_date(year, month)
    # city='昭通市'

    data_deleted_1 = []
    for i in data:
        if i['所在城市'] != city:
            data_deleted_1.append(i)

    data_deleted_2 = []
    for i in data_deleted_1:
        if i['月份'] == date1:
            data_deleted_2.append(i)

    for i in data_deleted_2:
        a = i['集团行业类别']
        for j in industry.keys():
            if a == j:
                industry[j] += 1
    return industry


def get_indux_csv(data):
    data = data[['月份', '集团行业类别', '所在城市']].to_dict(orient='records')
    year = '2020'
    data_df = pd.DataFrame()
    for i in range(2, 8):
        i = str(i)
        for j in PURE_CITYS:
            dic = indus_sta(year, i, j, data)
            dic['月份'] = gnrt_date(year, i)
            dic['地区'] = j
            data_df = data_df.append(dic, ignore_index=True)
    data_df.to_csv(r'utils\sangxueyi\data\industry_num.csv',
                   sep=',',
                   header=True,
                   index=False,
                   encoding='utf-8')


# def get_popution_data(month):
#     # o_data = data_preprocess(r'utils\sangxueyi\data\job_num.csv')
#     # print(o_data)
#     o_data=read_table('job_num')
#     year='2020'
#     # o_data=o_data.drop()
#     date=gnrt_date(year,month)
#     data = o_data[(o_data['月份'] == date)].drop(['地区'],1)
#     # print(data)
#     data=data.to_dict(orient='records')


    # for i in data:
    #     for j in i.keys():
    #         if j in ['月份','地区','\\N']:
    #             del[i[j]]
    return data
 

def get_industry_data(month):
    """ input:str """
    # print('In get_industry_data')
    # o_data = data_preprocess(r'utils\sangxueyi\data\industry_num.csv')
    o_data=read_table('industry_num')
    year='2020'

    # o_data=o_data.drop()
    date=gnrt_date(year,month)+'.0'
    data = o_data[o_data['月份'] == date].drop(['月份','地区','None'],1)
    data=data.to_dict(orient='records')
    # sum_li=list()
    a=dict()
    for i in data:
        for j in i.keys():
            if j in a.keys():
                a[j]=a[j]+float(i[j])
            else:
                a[j]=0

    data_return=list()

    for j in a.keys():
        b=dict()
        b['type']=j
        b['value']=a[j]
        data_return.append(b)

    # for i in data:
    #     for j in i.keys():
    #         if j in ['月份','地区','\\N']:
    #             del[i[j]]
    return data_return

def get_industry_tool(month):
    """ input:str """
    # print('In get_industry_data')
    # o_data = data_preprocess(r'utils\sangxueyi\data\industry_num.csv')
    o_data=read_table('industry_num')
    year='2020'

    # o_data=o_data.drop()
    date=gnrt_date(year,month)+'.0'
    data = o_data[o_data['月份'] == date].drop(['月份','地区','None'],1)
    data=data.to_dict(orient='records')
    # sum_li=list()
    a=dict()
    for i in data:
        for j in i.keys():
            if j in a.keys():
                a[j]=a[j]+float(i[j])
            else:
                a[j]=0

    month_sum_li=sum(a.values())

 
    return a,month_sum_li


def form_change():
    li=list()
    for i in range(2,8):
        dic,su=get_industry_tool(str(i))
        for j in dic.keys():
            a=dict()
            a['日期（年月）']=gnrt_date('2020',str(i))
            a['行业类别']=j
            a['比率']=dic[j]/su
            li.append(a)
    df=pd.DataFrame(li)
    df.to_csv(r'C:\Users\HiWin10\Desktop\labor-coefficient-all\labor-coefficient-server\utils\sangxueyi\data\industry_rate.csv',
                   sep=',',
                   header=True,
                   index=False,
                   encoding='utf-8')
        


if __name__ == '__main__':
    # month = '2'
    # year = '2020'
    # area = '昆明市'
    # path = r'utils\sangxueyi\data\data_city.csv'
    # data = data_preprocess(path)
    # get_indux_csv(data)

    # print(get_industry_tool('2'))
    # print(get_popution_data('3'))
    # print(form_change())
    form_change()


    # testdata = data[:100]
    # gnrt_emp_csv(testdata)
    # indus_sta(data)
