from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import *
import pandas as pd
import numpy as np
import global_var
from layout.widgets.dataTable import DataTable
from PyQt5 import Qt

class DataCol(QWidget):###需要一个check
    def __init__(self):
        super(DataCol,self).__init__()
        self.dataColBox = QComboBox()
        colList = global_var.currentData.data.columns.tolist()
        colList.insert(0, "")
        for col in colList:
            self.dataColBox.addItem(col)
        layout = QHBoxLayout()
        layout.addWidget(self.dataColBox)
        self.setLayout(layout)

class CleanEdit(QWidget):  # 参数设置UI
    addTask_ = pyqtSignal(str)

    def __init__(self):
        super(CleanEdit, self).__init__()
        layout_v1 = QVBoxLayout()
        self.label = QLabel("样本中空值占比：")  # 000
        self.contents = QTextEdit()  # 000
        layout_v1.addWidget(self.label)
        layout_v1.addWidget(self.contents)
        self.btn_choose = QPushButton("添加到任务")  # 000
        self.btn_choose.clicked.connect(self.add_task_clicked)
        self.delete_data = DataCol()
        self.b2=QLabel("选择需要删除的一个属性：")
        layout_v2= QVBoxLayout()
        layout_v2.addWidget(self.b2)
        layout_v2.addWidget(self.delete_data)
        layout_v2.addWidget(self.btn_choose)
        layout = QHBoxLayout()
        layout.addLayout(layout_v1)
        layout.addLayout(layout_v2)
        layout.setStretch(0, 5)
        layout.setStretch(1, 1)
        self.setLayout(layout)

        data = pd.read_csv(global_var.filePath)
        total = data.isnull().sum().sort_values(ascending=False)
        percent = (data.isnull().sum() / data.isnull().count()).sort_values(ascending=False)
        missing_data = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
        f = open('D:\codeitest\hel222.txt', 'w')
        print(missing_data.head(20), file=f)
        f.close()

        f1 = open('D:\codeitest\hel222.txt', 'r')
        with f1:
            data = f1.read()
            self.contents.setText(data)

    def add_task_clicked(self):
        #将要删除的属性保存在list中便于操作
        X = list()
        if self.delete_data.dataColBox.currentText() != "":
            X.append(self.delete_data.dataColBox.currentText())
        columns=X
        global_var.currentTask.operateData.dataatr=columns
        global_var.currentTask.resultType = global_var.DataPreType.CLEAN  # 数据清洗
        global_var.currentTask.operateList.append(global_var.allOperateList[0][0])
        self.addTask_.emit(global_var.allOperateList[0][0])
        
class CleanOut(QWidget):#输出UI
    def __init__(self, result=global_var.ResultCluster()):
        super(CleanOut, self).__init__()
        data = result.data
        self.table = DataTable(data)
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

def cleaning_atr(taskData):
    data = taskData.operateData.data  # 操作数据
    alist=global_var.currentTask.operateData.dataatr
    feature = alist[0]
    if feature!= "":
        data=data.drop([feature],axis=1)
    result = global_var.ResultClean()
    result.data = data
    global_var.currentTask.operateData.data = data
    #####如何更新operateData????

        
        
        
        
        

