# author:Xdmony
# contact: jerkyadmon@gmail.com
# datetime:2020/4/22 1:24 下午
# software: PyCharm
# description:

"""
文件说明：决策树分类
"""
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QPushButton
from sklearn import tree, model_selection
import pandas as pd
import global_var
from layout.widgets.dataTable import DataTable


class DTC_Edit(QWidget):
    addTask_ = pyqtSignal(str)

    def __init__(self):
        super(DTC_Edit, self).__init__()
        layout = QVBoxLayout()
        layout_add = QHBoxLayout()
        layout_edit = QHBoxLayout()
        label = QLabel("样本占比：")
        self.scale_input = QLineEdit()
        layout_edit.addWidget(label)
        layout_edit.addWidget(self.scale_input)
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
        global_var.currentTask.scale = eval(self.scale_input.text())
        global_var.currentTask.resultType = global_var.DataMiningType.CLASSIFY  # 分类
        global_var.currentTask.operateList.append(global_var.allOperateList[3][0])
        self.addTask_.emit(global_var.allOperateList[3][0])


class DTC_Out(QWidget):
    def __init__(self, result=global_var.ResultClassify()):
        super(DTC_Out, self).__init__()
        data_test = result.data_test
        data_pre = result.data_predict
        data_test["predict"] = data_pre.iloc[:, -1]
        self.table = DataTable(data_test)
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)


def decision_tree_classify(taskData):
    """
    决策树分类
    :param taskData:
    :return:
    """
    data = taskData.operateData.data  # 操作数据
    scale = taskData.scale  # 样本占比
    columns = taskData.operateData.dataColumns
    col_len = len(columns)
    X_feature = columns[0:-1]  # 样本特征
    y_feature = columns[-1]  # 样本结果（target）
    X = data[X_feature].values.reshape(-1, col_len - 1)
    y = data[y_feature].values.reshape(-1, 1)
    X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=scale)
    clf = tree.DecisionTreeClassifier()
    clf.fit(X_train, y_train)
    y_predict = clf.predict(X_test)
    data_test = pd.DataFrame(columns=columns[0: -1])  # 测试集
    data_predict = pd.DataFrame(columns=columns[0: -1])  # 预测值
    for index in range(len(X_test)):
        data_test.loc[index] = X_test[index]
        data_predict.loc[index] = X_test[index]
    data_test[columns[-1]] = y_test
    data_predict[columns[-1]] = y_predict
    result = global_var.ResultClassify()
    result.model = clf
    result.data_test = data_test
    result.data_predict = data_predict
    result.columns = columns
    global_var.currentTask.result = result  # 结果保存