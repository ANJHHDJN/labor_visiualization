import json

from flask import Flask, request, send_from_directory
from flask_cors import *

from constant.area_dict import code_to_area, area_to_code
from db.db_j import read_table
from entity.vo.resultvo import Result, SUCCESS, FAIL, REBUT
from resources import app_conf
from services import employment_service, labor_service, report_service
from utils.sangxueyi.statistics_job_industry import gnrt_date
# from urllib.parse import quote
from urllib.parse import urlencode
import pandas as pd
app = Flask(__name__)
CORS(app, supports_credentials=True)

data1_cache = None
data3_cache = None


@app.route('/api/employment_ratio', methods=['POST', 'GET'])
def get_employee_rate():
    '''
    获取就业率接口
    :param:  area_code 城市行政区划代码
    :param:  year 查询年份
    :param:  month 查询月份
    :return:

    :author 江帆
    '''

    # # 1.获取参数
    area_code = request.args.get('area_code')
    year = request.args.get('year')
    month = request.args.get('month')

    # 2.执行业务逻辑，返回数据结果
    data = employment_service.count_employment_rate(area_code, year, month)

    # 3.响应结果
    return Result(SUCCESS, "查询成功", data).tostring()


@app.route('/api/labor_flow', methods=['POST', 'GET'])
def get_labor_flow():
    '''
    获取劳动力流向
    :param:  year 查询年份
    :param:  month 查询月份
    :return:

    :author 吴依寒
    '''

    # 1.获取参数
    year_month = request.args.get('year_month')

    # 2.执行业务逻辑，返回数据结果
    data = labor_service.count_labor_flow(year_month)

    # 3.响应结果
    return Result(SUCCESS, "查询成功", data).tostring()


@app.route('/api/report')
def gnrt_report():
    area_code = request.args.get('area_code')
    year = request.args.get('year')
    month = request.args.get('month')
    year_month = gnrt_date(year, month)

    # print(year)
    li = report_service.get_data(
        area_code, year, month, year_month)
    data = {
        'emp_population_data': li[0],
        'emp_population_change_data': li[1],
        'industry_data': li[2],
        'emp_age_data': li[3],
        'fired_age_data': li[4],
        'labor_in_data': li[5],
    }
    return Result(SUCCESS, "查询成功", data).tostring()
    # pass


@app.route('/api/report_download', methods=['POST', 'GET'])
def report_download():
    '''
    下载分析报表
    :param:  area_code 城市行政区划代码
    :param:  year 查询年份
    :param:  month 查询月份
    :return:

    :author
    '''

    # 1.获取参数
    area_code = request.args.get('area_code')
    year = request.args.get('year')
    month = request.args.get('month')
    print(year, month, area_code)
    url = 'http://localhost:81/#/report?year=' + year + '&month=' + month + '&area_code=' + area_code
    print(url)

    # 2.执行业务逻辑，返回数据结果
    file_dir, filename = report_service.generate_report(
        area_code, year, month, url)

    # 3.响应结果
    print(file_dir, filename)
    return send_from_directory(directory=file_dir,
                               filename=filename,
                               as_attachment=True)


flow_types = ("to","from") #from 出发城市， out到达城市
@app.route('/api/labor_flow1', methods=['POST', 'GET'])
def 获取地图点击数据():
    area_code = request.args.get('area_code')
    year_month = request.args.get('year_month')
    flow_type = int(request.args.get('flow_type'))  # 0 计算该城市的流入，即out_为该城市    # 根据条件查询流入/流出的数据
    origin_df = read_table("labor_flow")
    the_month_df = origin_df.loc[origin_df['month']==year_month]
    rs_df = the_month_df.loc[the_month_df[flow_types[flow_type]]==code_to_area[area_code]]
    # 1. 飞线图
    fly_json_array = rs_df.to_json(orient='records')
    # r=fly_line&area_code=:area_code&year_month=202005&flow_type=:flow_type  /api/labor_flow1
    # 2.查询点的流向地标，用于更新标记地点，
    # flow_type=0 流入，查lat1，lng1。
    # flow_type=1 流出，查lat2，lng2。
    type = "1" if flow_type==0 else "2"
    rel_area_df = rs_df.loc[:, ['lat'+type, 'lng'+type, flow_types[flow_type]]]\
        .rename(columns={'lat'+type: 'lat', 'lng'+type: 'lng'})
    rel_area_json_array = rel_area_df.to_json(orient='records')

    # 3,地图提示框
    # 查出中心点的经纬度
    center_type = "2" if flow_type == 0 else "1"
    center_df = rs_df.sample(n=1).loc[:,['lat'+center_type, 'lng'+center_type]]\
        .rename(columns = {'lat'+center_type: "lat", 'lng'+center_type: "lng"})
    center_df['adcode'] = area_code
    center_df['city'] = code_to_area[area_code]
    center_df['month'] = year_month

    # 求总流入
    total_in = the_month_df.loc[the_month_df["to"]==code_to_area[area_code]]['value'].sum()
    # 求总流出
    total_out = the_month_df.loc[the_month_df["from"]==code_to_area[area_code]]['value'].sum()
    center_df['total_in'] = total_in
    center_df['total_out'] = total_out
    center_area_json_array = center_df.to_json(orient='records')

    # 4.流入/流出排行表
    flow_percent_df = rs_df.copy(deep=True).rename(columns = {flow_types[int(not flow_type)]: "city"})
    flow_percent_df['percent'] = (rs_df['value'] / rs_df['value'].sum())*100
    flow_percent_df['percent'] = flow_percent_df['percent'].round(2)
    flow_percent_df['area_code'] = flow_percent_df['city']
    for area,code in area_to_code.items():
        flow_percent_df.loc[flow_percent_df['area_code'] == area, "area_code"] = code
    flow_percent_df.sort_values('percent',ascending=False, inplace=True)
    flow_percent_json_array = flow_percent_df.to_json(orient='records')


    return {
        "fly_json_array": json.loads(fly_json_array),
        "rel_area_json_array":json.loads(rel_area_json_array),
        "center_area_json_array":json.loads(center_area_json_array),
        "flow_percent_json_array":json.loads(flow_percent_json_array)
    }

if __name__ == '__main__':
    app.run(host="0.0.0.0")  # 运行配置改才生效
