from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QFormLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox
)
import pandas as pd
import numpy as np
import global_var
from layout.widgets.dataTable import DataTable
from PyQt5 import Qt
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA

class PCAEdit(QWidget):  # 参数设置UI
    addTask_ = pyqtSignal(str)

    def __init__(self):
        super(PCAEdit, self).__init__()
        self.tableRange: dict = {}  # key为button，value为范围tuple
        self.tableRangeLabel: dict = {}  # key为button，value为对应label控件
        self._tableRangeLabel = QLabel()
        self.dimLineEdit = QLineEdit()

        # 设置提示输入文本
        self._tableRangeLabel.setText('全表')
        self.dimLineEdit.setPlaceholderText("可选参数，默认为2（必须小于样本数）")
        # 设置显示效果
        self.dimLineEdit.setEchoMode(QLineEdit.Normal)
        # 提交按钮
        self.add_button = QPushButton()
        self.add_button.setText('添加至任务列表')
        self.add_button.clicked.connect(self.add_task_clicked)
        # 数据划分按钮
        self.split_button = QPushButton()
        self.split_button.setText('划分数据')
        self.split_button.clicked.connect(self.on_show_split_panel)

        #布局
        data_select_layout1 = QHBoxLayout()
        data_select_layout1.addWidget(self._tableRangeLabel)
        # 创建一个表单布局
        flayout = QFormLayout()
        # 把文本框添加到布局，第一个参数为左侧的说明标签
        flayout.addRow("数据范围", data_select_layout1)
        flayout.addRow("目标维数", self.dimLineEdit)

        down_layout = QHBoxLayout()
        down_layout.addWidget(self.split_button)
        down_layout.addWidget(self.add_button)

        self.layout = QVBoxLayout()
        self.layout.addLayout(flayout)
        self.layout.addLayout(down_layout)
        self.layout.setStretch(1, 1)
        # 把设置的布局加载到窗口
        self.setLayout(self.layout)


    def add_task_clicked(self):
        global_var.currentTask.resultType = global_var.DataPreType.PCAA  # 数据清洗
        global_var.currentTask.operateList.append(global_var.allOperateList[0][2])
        self.addTask_.emit(global_var.allOperateList[0][2])

    def on_show_split_panel(self):
        self.dataSplit = DataSplit(self)
        self.dataSplit.show()
        self.dataSplit.confirmed.connect(self.on_confirm_split_panel)

    def on_confirm_split_panel(self):  ####确认数据划分
        range_dict: dict = self.dataSplit.get_data_range()
        self._tableRangeLabel.setText(
            '行{%d:%d}，列{%d:%d}' % range_dict['in_train'])
        self.dataSplit = None

    
class PCAOut(QWidget):#输出UI
    def __init__(self, result=global_var.ResultCluster()):
        super(PCAOut, self).__init__()
        data = result.data
        self.table = DataTable(data)
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

def get_pca(taskData):
    data = taskData.operateData.data  # 操作数据
    n=global_var.currentTask.n
    features = data.columns.tolist()
    mdl = np.array(data[features])
    pca= PCA(n_components=n)
    pca.fit_transform(mdl)
    data =  pca.fit_transform(mdl)  # 类别标记
    result = global_var.ResultPCA()
    #result.model = pca
    result.data = data
    global_var.currentTask.operateData.data = data



