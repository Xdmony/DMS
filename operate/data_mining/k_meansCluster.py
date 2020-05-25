# author:Xdmony
# contact: jerkyadmon@gmail.com
# datetime:2020/4/22 1:25 下午
# software: PyCharm
# description:

"""
文件说明：K-means聚类
"""
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QLabel, QLineEdit, QVBoxLayout
from sklearn.cluster import KMeans
import numpy as np

import global_var
from layout.widgets.dataTable import DataTable


class ClusterEdit(QWidget):
    addTask_ = pyqtSignal(str)

    def __init__(self):
        super(ClusterEdit, self).__init__()
        layout = QVBoxLayout()
        layout_add = QHBoxLayout()
        layout_edit = QHBoxLayout()
        label = QLabel("K：")
        self.K_input = QLineEdit()
        layout_edit.addWidget(label)
        layout_edit.addWidget(self.K_input)
        layout_edit.addStretch(1)
        add_task = QPushButton("添加到任务")
        add_task.clicked.connect(self.add_task_clicked)
        layout_add.addStretch(2)
        layout_add.addWidget(add_task)
        layout.addLayout(layout_edit)
        layout.addLayout(layout_add)
        layout.addStretch(6)
        self.setLayout(layout)

    def add_task_clicked(self):
        """
        添加任务按钮点击事件
        :return:
        """
        global_var.currentTask.K = eval(self.K_input.text())
        global_var.currentTask.resultType = global_var.DataMiningType.CLUSTER  # 聚类
        global_var.currentTask.operateList.append(global_var.allOperateList[2][0])
        self.addTask_.emit(global_var.allOperateList[2][0])


class ClusterOut(QWidget):
    def __init__(self, result=global_var.ResultCluster()):
        super(ClusterOut, self).__init__()
        data = result.data
        self.table = DataTable(data)
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)


def k_means_cluster(taskData):
    """
    聚类
    :param taskData:
    :return:
    """
    data = taskData.operateData.data  # 操作数据
    features = data.columns.tolist()
    mdl = np.array(data[features])
    K = global_var.currentTask.K
    seed = 9
    clf = KMeans(n_clusters=K, random_state=seed)
    clf.fit(mdl)
    data["label"] = clf.labels_  # 类别标记
    result = global_var.ResultCluster()
    result.model = clf
    result.data = data
    global_var.currentTask.result = result
