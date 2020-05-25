# author:Xdmony
# contact: jerkyadmon@gmail.com
# datetime:2020/4/22 1:25 下午
# software: PyCharm
# description:

"""
文件说明：显示数据集信息
"""
from PyQt5 import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QHBoxLayout, QPushButton, QComboBox, QLabel
import pandas as pd
import global_var
from layout.widgets.dataTable import DataTable


class DataTail(QWidget):
    add_ = pyqtSignal(str)
    def __init__(self, dataSet):
        super(DataTail, self).__init__()
        self.data = dataSet
        self.table = DataTable(dataSet.data)
        self.btn_add_data = QPushButton("添加到任务")
        self.btn_add_data.clicked.connect(self.add_data_to_task)
        self.features = dataSet.dataColumns
        layout_feature = QVBoxLayout()
        layout_feature.setSpacing(5)
        self.all_check = QCheckBox("全选")
        self.all_check.setChecked(True)
        self.all_check.stateChanged.connect(self.all_checked)
        layout_feature.addWidget(self.all_check)
        for feature in self.features:
            checkbox = QCheckBox(feature)
            checkbox.setObjectName(feature)
            checkbox.setChecked(True)
            layout_feature.addWidget(checkbox)
        layout_target = QHBoxLayout()
        target_label = QLabel("Target: ")
        self.target_combo = QComboBox()
        comboList = list()
        comboList.append("")
        comboList = comboList + self.features
        self.target_combo.addItems(comboList)
        layout_target.addWidget(target_label)
        layout_target.addWidget(self.target_combo)
        layout_feature.addLayout(layout_target)
        layout_feature.addWidget(self.btn_add_data)
        # layout_operate = QVBoxLayout()
        # layout_operate.addLayout(layout_feature)
        # layout_operate.addWidget(self.btn_add_data)
        # layout_operate.setStretch(0, 8)
        # layout_operate.setStretch(1, 1)
        layout = QHBoxLayout()
        layout.addWidget(self.table)
        layout.addLayout(layout_feature)
        layout.setStretch(0, 5)
        layout.setStretch(1, 1)
        self.setLayout(layout)

    def all_checked(self):
        """
        全选
        :return:
        """
        if self.all_check.isChecked():
            for feature in self.features:
                checkbox = self.findChild(QCheckBox, feature)
                checkbox.setChecked(True)
        elif not self.all_check.isChecked():
            for feature in self.features:
                checkbox = self.findChild(QCheckBox, feature)
                checkbox.setChecked(False)

    def add_data_to_task(self):
        """
        添加数据到任务
        :return:
        """
        X = list()  # 特征选择
        for feature in self.features:
            checkbox = self.findChild(QCheckBox, feature)
            if checkbox.isChecked():
                X.append(feature)
        columns = X
        if "" != self.target_combo.currentText():
            y = self.target_combo.currentText()
            columns.append(y)
        global_var.currentTask.operateData.dataColumns = columns
        data = pd.DataFrame()
        for feature in columns:
            data[feature] = self.data.data[feature]
        global_var.currentTask.operateData.data = data
        global_var.currentTask.taskData = global_var.currentTask.operateData
        self.add_.emit(self.data.dataName)

