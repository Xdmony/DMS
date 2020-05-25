# author:Xdmony
# contact: jerkyadmon@gmail.com
# datetime:2020/4/22 12:31 下午
# software: PyCharm
# description:

"""
文件说明：数据存储
"""

import pandas as pd
from enum import Enum
import pickle

# 文件路径，除了本地导入数据，其他的都用不到
filePath = ""


# 枚举类，数据集类型（输入/输出）
class DataSetType(Enum):
    IN = 1
    OUT = 2
#枚举，数据预处理结果类型
class DataPreType(Enum):
    CLEAN=1 #数据清洗
    MAXMIN=2 #数据变换（归一化）
    PCAA=3 #数据规约
    
# 枚举，数据挖掘结果类型
class DataMiningType(Enum):
    ASSOCIATION = 1  # 关联规则
    CLASSIFY = 2  # 分类分析
    CLUSTER = 3  # 聚类分析
    REGRESSION = 4  # 回归分析


# 数据集信息
class DataSet:
    def __init__(self):
        self.dataName = ""  # 数据集名
        self.type = DataSetType.IN  # 数据类型输入/输出,默认为输入
        self.data = pd.DataFrame()  # 数据
        self.dataColumns = list()  # 样本特征集合
        self.dataatr=list()
        self.length = 0  # 数据量

    def convert(self):
        """
        类型转换，用于设置数据预处理结果为下次处理的输入
        :return:
        """
        if self.type == DataSetType.IN:
            self.type = DataSetType.OUT
        else:
            self.type = DataSetType.IN
#数据清洗结果
class ResultClean:
    def __init__(self):
        self.columns = list()
        self.data = pd.DataFrame()
#数据变换结果（归一化）
class ResultMaxMin:
    def __init__(self):
        self.model = None
        self.data = pd.DataFrame()

#数据规约（降维）
class ResultPCA:
    def __init__(self):
        self.model = None
        self.data = pd.DataFrame()



# 关联分析结果
class ResultAssociation:
    def __init__(self):
        self.rule = pd.DataFrame()


# 分类分析结果
class ResultClassify:
    def __init__(self):
        self.model = None
        self.data_test = pd.DataFrame()
        self.data_predict = pd.DataFrame()
        self.columns = list()


# 聚类分析结果
class ResultCluster:
    def __init__(self):
        self.model = None
        self.data = pd.DataFrame()


# 回归分析结果
class ResultRegression:
    def __init__(self):
        self.model = None
        self.data_test = pd.DataFrame()
        self.data_predict = pd.DataFrame()
        self.columns = list()
        self.intercept = None
        self.coef = None


# 任务信息
class TaskInfo:
    def __init__(self):
        self.taskId = 0  # 任务ID
        self.taskData = DataSet()  # 任务数据集，原始数据，任务不会对其更改
        self.operateData = DataSet()  # 数据，每执行一个预处理任务都会对其进行操作，由数据添加初始化
        self.operateList = list()  # 任务列表，存储进行的数据预处理，数据挖掘，可视化等操作
        self.min=0.0 #最大值
        self.max=1.0 #最小值
        self.n=2 #默认维度
        
        self.scale = 0.3  # 样本占比，默认7：3
        self.K = 4  # 聚类集群个数
        # 关联规则参数
        self.support = 0.01
        self.confidence = 0.0
        self.lift = 0.0

        self.resultType = None  # 数据挖掘类型
        self.result = None  # 分析结果


# 所有数据集存储
class AllData:
    def __init__(self):
        self.data_in = dict()  # 输入数据，显示在输入列表框
        self.data_out = dict()  # 输出数据，显示在输出列表框


# 当前使用数据指针
currentData = DataSet()  # 当前数据集
currentTask = TaskInfo()  # 当前任务

# 数据集集合
allDataSet = AllData()  # 程序的所有数据集

# 数据预处理，数据挖掘，数据可视化，需要添加对应的处理方法
pre_treatList = ["数据清洗", "数据变换", "数据规约"]
associationList = ["apriori关联规则"]
clusterList = ["k-means聚类"]
classificationList = ["决策树分类"]
regressionList = ["线性回归"]
visualList = ["散点图","直方图","柱状图","关联分析图"]
allOperateList = [pre_treatList, associationList, clusterList, classificationList, regressionList, visualList]


# 数据保存
def save():
    file = open("data/data.save", "wb")
    pickle.dump(allDataSet, file)
    file.flush()
    file.close()


# 读取数据
def read():
    file = open("data/data.save", "rb")
    global allDataSet
    allDataSet = pickle.load(file)
    file.close()


if __name__ == '__main__':
    type_test = DataSetType.IN
    print(type_test)
    save()
