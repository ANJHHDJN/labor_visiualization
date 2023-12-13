import os
from entity.vo.defined_class import Map

# 环境变量
basedir  = os.path.abspath(os.path.dirname(__file__)) + os.path.sep

# 路径配置
path = Map()
path.report_dir = basedir + "report_dir"