def count_labor_flow(year_month):
    '''
    统计劳动力流向的业务实现
    :return: 就业率数据格式

    :author 吴依寒
    '''

    with open("./data/" + str(year_month) + ".csv", "r", encoding='utf-8') as file:  # 打开文件
        data = file.read()
    return data