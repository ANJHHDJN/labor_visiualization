import os
import sys
sys.path.append(r'C:\Users\HiWin10\Desktop\labor-coefficient-all\labor-coefficient-server')

from utils import web_util, file_util
from constant.area_dict import area_to_code
from utils.sangxueyi.statistics_job_industry import get_industry_data
from utils.sangxueyi.statistics_emp_age import get_emp_age_data,get_fired_age_data
from utils.sangxueyi.statistics_population_num import get_population_data,get_population_change_data
from utils.sangxueyi.statistics_flow_city import get_labor_flow_data
from resources import app_conf
import threading
from time import ctime,sleep

class MyThread(threading.Thread):

    def __init__(self, func, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result   # 如果子线程不使用join方法，此处可能会报没有self.result的错误
        except Exception:
            return None


def code_to_city(code):
    city = ''
    for i in area_to_code.items():
        if i[1] == code:
            city = i[0]
            break
    return city


def get_data(area_code, year, month,year_month):

    city = code_to_city(area_code)

    return_li=list()

    t1=MyThread(get_population_data,args=(year_month,))
    t2=MyThread(get_population_change_data,args=(year_month,))
    t3=MyThread(get_industry_data,args=(month,))
    t4=MyThread(get_emp_age_data,args=(month,))
    t5=MyThread(get_fired_age_data,args=(month,))
    t6=MyThread(get_labor_flow_data,args=(month,))

    thread=[t1,t2,t3,t4,t5,t6]
    
    for t in thread:
        t.setDaemon(True)
        t.start()
    

    for t in thread:
        t.join()
        return_li.append(t.get_result())
    

    # emp_population_data = get_population_data(year_month) # Down
    # emp_population_change_data = get_population_change_data(year_month) # Down

    # industry_data = get_industry_data(month, city)  # Down
    # emp_age_data = get_emp_age_data(month, city)  # Down
    # fired_age_data = get_fired_age_data(month, city)  # Down
    # labor_in_data=get_labor_flow_data(month) # Down

    return return_li



def generate_report(area_code, year, month, url):
    '''
    生成数据报表，并返回报表文件路径和名称
    :param area_code:
    :param year:
    :param month:
    :return:
    '''
    # 保存路径和文件名称
    save_dir = app_conf.path.report_dir
    filename = "report(%s.%s.%s.)" % (area_code, year, month)

    # 1.如果文件已存在，则直接返回
    if file_util.file_existed(save_dir + os.path.sep + filename+ ".pdf"):
    #     return save_dir, filename + ".pdf"
        os.remove(save_dir + os.path.sep + filename+ ".pdf")  


    
    # 2.生成数据报表文件,并存储
    web_util.print_web_to_file(url, save_dir, filename)

    # 3.返回数据报表文件名称
    return save_dir, filename + ".pdf"

if __name__=='__main__':
    li = get_data('530100','2020','5','202005')
    for i in li:
        print(i)