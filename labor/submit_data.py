import requests

code_dict = {
    '劳动⼒流向及就业指数': 'BN0001',
    '企业家活跃度指数说明⽂档': 'BN0002',
    '数据异常检测说明⽂档': 'BN0003',
    '⽹络消费价格指数数据展示说明': 'BN0004',
    '微观经济预警说明⽂档': 'BN0005',
    '微观经济指数预测说明⽂档': 'BN0006',
    '消费者活跃指数呈现⽅式': 'BN0007',
    '异常原因分析说明⽂档': 'BN0008'}

token_url = 'https://www.wizdom.cn/dczd-admin/ynu/getToken'
upload_url = 'https://www.wizdom.cn/dczd-admin/ynu/oss/upload'


def post_file(code, file_name, file_path, token, isAll):
    # with open(file_path, mode="r", encoding="utf8") as f:
    with open(file_path, mode="rb") as f:
        file = {
            "file": (file_name, f.read()),
        }
        data = {
            "code": code,
            "isAll": isAll,   # 数类型上传⽂件的全量、增量标识:  0 增量     1全量
        }
        headers = {"token": token}
        return requests.post(url=upload_url, headers=headers, data=data, files=file).json()


def submit_data_file(code, file_name, file_path, isAll):
    """
    提交统计数据结果文件
    :code: 指数代码
    :param file_name：文件的名称，接收方将保存的文件名称
    :param file_path：上传文件的绝对路径/相对本文件的路径
    """
    token_params = {'code': code}
    token_result = requests.get(token_url, token_params).json()
    if token_result['code'] == 0:
        token = token_result['data']['token']
        result = post_file(code, file_name, file_path, token, isAll)
        print(result['msg'])
    else:
        print(token_result['msg'])


if __name__ == '__main__':
        labor_code = code_dict['劳动⼒流向及就业指数']
        filename = "劳动力指数数据v1.0.xlsx"           # 接收方保存的文件名称，无所谓，对方已经重命名了文件名
        file_path = "C:\\Users\\shuch\\Desktop\\劳动力指数数据v1.0.xlsx"   # 传输的文件路径
        submit_data_file(labor_code, filename, file_path, isAll=0)
