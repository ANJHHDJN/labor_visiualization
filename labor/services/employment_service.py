import random
import sys
sys.path.append(r'F:\labor-coefficient-server_sxy\labor-coefficient-server')
from constant.area_dict import area_to_code
from entity.vo.defined_class import Map
from utils import string_util
import pandas as pd
import csv
from db.db_j import read_table
# F:\lipstick\jiangfan\data\data_utf8.csv

# df = pd.read_csv(r'F:/data/data_utf8_addCity.csv')
# df = df[~df['城市名称'].isin(['\\N'])]
CSV_PATH = './data/jobpercent.csv'
TABLENAME = 'jobpercent'


CITYS=[{'name': '昆明市','districtAndCounty': ['盘龙区', '五华区', '官渡区', '西山区', '东川区', '安宁市', '呈贡县', '龙城镇', '晋宁县', '昆阳镇', '富民县', '永定镇', '宜良县', '匡远镇', '嵩明县', '嵩阳镇', '石林彝族自治县', '鹿阜镇', '禄劝彝族苗族自治县', '屏山镇', '寻甸回族彝族自治县', '仁德镇']},
       {'name': '曲靖市','districtAndCounty': ['麒麟区', '宣威市', '马龙县', '通泉镇', '沾益县', '西平镇', '富源县', '中安镇', '罗平县', '罗雄镇', '师宗县', '丹凤镇', '陆良县', '中枢镇', '会泽县', '金钟镇']},
       {'name': '玉溪市','districtAndCounty': ['红塔区', '江川县', '大街镇', '澄江县', '凤麓镇', '通海县', '秀山镇', '华宁县', '宁州镇', '易门县', '龙泉镇', '峨山彝族自治县', '双江镇', '新平彝族傣族自治县', '桂山镇', '元江哈尼族彝族傣族自治县', '澧江镇']},
       {'name': '保山市','districtAndCounty': ['隆阳区', '施甸县', '甸阳镇', '腾冲县', '腾越镇', '龙陵县', '龙山镇', '昌宁县', '田园镇']},
       {'name': '昭通市','districtAndCounty': ['昭阳区', '鲁甸县', '文屏镇', '巧家县', '新华镇', '盐津县', '盐井镇', '大关县', '翠华镇', '永善县', '溪落渡镇', '绥江县', '中城镇', '镇雄县', '乌峰镇', '彝良县', '角奎镇', '威信县', '扎西镇', '水富县', '向家坝镇']},
       {'name': '丽江市','districtAndCounty': ['古城区', '永胜县', '永北镇', '华坪县', '中心镇', '玉龙纳西族自治县', '黄山镇', '宁蒗彝族自治县', '大兴镇']},
       {'name': '普洱市','districtAndCounty': ['思茅区', '宁洱哈尼族彝族自治县', '宁洱镇', '墨江哈尼族自治县', '联珠镇', '景东彝族自治县', '锦屏镇', '景谷傣族彝族自治县', '威远镇', '镇沅彝族哈尼族拉祜族自治县', '恩乐镇', '江城哈尼族彝族自治县', '勐烈镇', '孟连傣族拉祜族佤族自治县', '娜允镇', '澜沧拉祜族自治县', '勐朗镇', '西盟佤族自治县', '勐梭镇']},
       {'name': '临沧市','districtAndCounty': ['临翔区', '凤庆县', '凤山镇', '云县', '爱华镇', '永德县', '德党镇', '镇康县', '南伞镇', '双江拉祜族佤族布朗族傣族自治县', '勐勐镇', '耿马傣族佤族自治县', '耿马镇', '沧源佤族自治县', '勐董镇']},
       {'name': '德宏州','districtAndCounty': ['芒市','潞西市', '瑞丽市', '梁河县', '遮岛镇', '盈江县', '平原镇', '陇川县', '章凤镇']},
       {'name': '怒江州','districtAndCounty': ['泸水县六库镇', '泸水县', '六库镇', '福贡县', '上帕镇', '贡山独龙族怒族自治县', '茨开镇', '兰坪白族普米族自治县', '金顶镇']},
       {'name': '迪庆州','districtAndCounty': ['香格里拉县', '建塘镇', '德钦县', '升平镇', '维西傈僳族自治县', '保和镇']},
       {'name': '大理州','districtAndCounty': ['大理市', '祥云县', '祥城镇', '宾川县', '金牛镇', '弥渡县', '弥城镇', '永平县', '博南镇', '云龙县', '诺邓镇', '洱源县', '茈碧湖镇', '剑川县', '金华镇', '鹤庆县', '云鹤镇', '漾濞彝族自治县', '苍山西镇', '南涧彝族自治县', '南涧镇', '巍山彝族回族自治县', '南诏镇']},
       {'name': '楚雄州','districtAndCounty': ['楚雄市', '双柏县', '妥甸镇', '牟定县', '共和镇', '南华县', '龙川镇', '姚安县', '栋川镇', '大姚县', '金碧镇', '永仁县', '永定镇', '元谋县', '元马镇', '武定县', '狮山镇', '禄丰县', '金山镇']},
       {'name': '红河州','districtAndCounty': ['蒙自县', '文澜镇', '个旧市', '开远市', '绿春县', '大兴镇', '建水县', '临安镇', '石屏县', '异龙镇', '弥勒县', '弥阳镇', '泸西县', '中枢镇', '元阳县', '南沙镇', '红河县', '迤萨镇', '金平苗族瑶族傣族自治县', '金河镇', '河口瑶族自治县', '河口镇', '屏边苗族自治县', '玉屏镇']},
       {'name': '文山州','districtAndCounty': ['文山县', '开化镇', '砚山县', '江那镇', '西畴县', '西洒镇', '麻栗坡县', '麻栗镇', '马关县', '马白镇', '丘北县', '锦屏镇', '广南县', '莲城镇', '富宁县', '新华镇']},
       {'name': '西双版纳州','districtAndCounty': ['景洪市', '勐海县', '勐海镇', '勐腊县', '勐腊镇']}]
AREA_COL = ['活动区域1','活动区域2','活动区域3']
PURE_CITYS = ['昆明市','曲靖市','玉溪市','保山市','昭通市','丽江市','普洱市','临沧市','德宏州','怒江州','迪庆州','大理州','楚雄州','红河州','文山州','西双版纳州']

# 取出地理名称的前两个字符
def standerize_name_s(areas):
    n = len(areas)
    for i in range(n):
        areas[i] = areas[i][0:2]
    return areas

# def standerize_name(citys,col):
#     for city in citys:
#         small_citys = city[col]
#         citys = standerize_name_s(small_citys)
#     return citys
def standerize_name(citys,col):
    for city in citys:
        small_citys = city[col]
        n = len(small_citys)
        for i in range(n):
            small_citys[i] = small_citys[i][0:2]
    return citys

# 将区县和地级市进行匹配
def match_city(two_areas,citys):
    match_result = []
    for area in two_areas:
        is_found = False
        for city in citys:
            city_name = city['name']
            small_citys = city['districtAndCounty']
            for i in small_citys:
                if area == i:
                    match_result.append([i,city_name])
                    is_found = True
                    break
            if is_found:
                break
        if not is_found:
              #打印“元素未找到”消息
            match_result.append([area,'None'])
    return match_result

# 在原始的表格中增加原始活动区域中对应的地级市
# 传入活动区域的列名，要增加的地区的表格，标准化后的表格数据
def add_area2city(col_name,df,citys):
    areas1 = df[col_name].tolist()
    areas1 = standerize_name_s(areas1)
    city_change1 = match_city(areas1,citys)
    result = []
    for i in city_change1:
        result.append(i[1])
    new_col = col_name + '_城市'
    df[new_col] = result

# 获取在表格中出现的所有区/县（不重复）
def get_all_area(area_col,df):
    area = []
    for i in area_col:
        area.extend(df[i].drop_duplicates().tolist())
    area = {}.fromkeys(area).keys()
    area = list(area)
    return area

def change_month(all_jobpercent):
    for i in all_jobpercent:
        i[0] = str(i[0])
        i[0] = i[0][:4] + '-' + i[0][4:]
    return all_jobpercent

def save2csv(datalist,filepath):
    month = []
    for i in datalist:
    #     print(i[0])
        month.append(i[0])
    month = sorted(list({}.fromkeys(month).keys()))
    final = []
    for j in month:
        for i in datalist:
            if i[0] == j:
                final.append([i[0],i[1],i[2]])
    name=['月份','城市','就业率']
    test=pd.DataFrame(columns=name,data=final)#数据有三列
    test.to_csv(filepath,index=False, encoding='utf-8')

def get_final(all_jobpercent):
    final = {}
    month = []
    for i in all_jobpercent:
    #     print(i[0])
        month.append(i[0])
    month = sorted(list({}.fromkeys(month).keys()))
    # print(month)
    # print(sorted(month))

    for j in month:
        y = []
        for i in all_jobpercent:
            if i[0] == j:
                y.append({'city':i[1],'value':i[2]})
        final[j] = y

    return final

def job_percent(month, area,df):
    # df = pd.read_csv(r'E:\lipstick\data\data_utf8.csv')
    # df = df[~df['城市名称'].isin(['\\N'])]
    total = len(df[(df['月份'] == month) & ((df['活动区域1_城市'] == area) | (df['活动区域2_城市'] == area) | (df['活动区域3_城市'] == area))])
    lost = len(df[(df['月份'] == month) & (df['客户身份'] == 0) & (
                (df['活动区域1_城市'] == area) | (df['活动区域2_城市'] == area) | (df['活动区域3_城市'] == area))])

    job_percent = (1 - lost / total) * 100
    return job_percent

def calculate_jobpercent(months,citys,df_add):
    all_jobpercent = []
    for i in months:
        for city in citys:
            all_jobpercent.append([i,city,job_percent(i,city,df_add)])
    return all_jobpercent

def generate_csv():
    df = pd.read_csv(r'./data/data_utf8_addCity.csv')
    df = df[~df['城市名称'].isin(['\\N'])]
    # 获取出现的所有区县
    area_list = get_all_area(AREA_COL, df)
    #
    # 表格的地区列表中只保留前两个字
    area_list = standerize_name_s(area_list)
    # 官方城市列表中的区县只保留前两个字
    df_stand_city = standerize_name(CITYS, 'districtAndCounty')
    # 将区县和城市进行匹配，得到匹配的结果
    # area_city_matchlist = match_city(area_list,stander_area_list)

    df_add = df
    for i in AREA_COL:
        add_area2city(i, df_add, df_stand_city)
    # month = ['月份']
    month = get_all_area(['月份'], df_add)

    all_jobpercent = calculate_jobpercent(month, PURE_CITYS, df_add)
    all_jobpercent = change_month(all_jobpercent)
    save2csv(all_jobpercent,CSV_PATH)

def readTable(table_name):
    # df_csv = pd.read_csv(csv_path,encoding='utf-8')
    df_csv = read_table(table_name)
    # print(df_csv)

    month = get_all_area(['月份'],df_csv)
    # print(month)

    # csv_file = open(csv_path, encoding='utf-8')  # 打开csv文件
    # csv_reader_lines = csv.reader(csv_file)  # 逐行读取csv文件
    # date = []  # 创建列表准备接收csv各行数据
    # for one_line in csv_reader_lines:
    #     date.append(one_line)
    # date = date[1:]
    date = []
    for indexs in df_csv.index:
        date.append(list(df_csv.loc[indexs].values[0:]))
    final = {}
    for j in month:
        y = []
        for i in date:
            if i[0] == j:
                y.append({'city':i[1],'value':(round(float(i[2]),2))})
        final[j] = y
    return final




def count_employment_rate(area_code, year, month):
    '''
    :author 江帆
    统计就业率的业务实现
    :return: 就业率数据格式
    '''
    if string_util.all_is_empty(area_code, year, month):
        return query_all_employment_rate()
    else:
        return "请求参数格式错误"

'''
    不传参数，查询全省的就业数据统计
'''
def  query_all_employment_rate():
    '''
    :author 江帆
    统计就业率的业务实现
    :return: 就业率数据格式
    '''
    '''  数据格式 
        { 2020-01：[{“城市”:“昆明”, "就业率":98%},{“城市”:“曲靖”, "就业率":95%}，...],
          2020-02：[{“城市”:“昆明”, "就业率":91%},{“城市”:“曲靖”, "就业率":93%}，...],
          ...
        }
    '''
    data = readTable(TABLENAME)
    print(data)
    return data


if __name__ == '__main__':
  print(query_all_employment_rate())