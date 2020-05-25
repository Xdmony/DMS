# author:Xdmony
# contact: jerkyadmon@gmail.com
# datetime:2020/4/22 1:22 下午
# software: PyCharm
# description:

"""
文件说明：线性回归Tab，和处理
"""
import sys
import webbrowser

from PyQt5.QtCore import *
# from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from sklearn import linear_model, model_selection
import pandas as pd
import numpy as np
from math import sqrt
from pyecharts.charts import Scatter
from pyecharts.render import make_snapshot
from snapshot_pyppeteer import snapshot
# import cv2
from PIL import Image

import global_var
from layout.widgets.dataTable import DataTable


class LinearEdit(QWidget):  # 参数设置UI
    addTask_ = pyqtSignal(str)

    def __init__(self):
        super(LinearEdit, self).__init__()
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
        global_var.currentTask.resultType = global_var.DataMiningType.REGRESSION  # 线性回归
        global_var.currentTask.operateList.append(global_var.allOperateList[4][0])
        self.addTask_.emit(global_var.allOperateList[4][0])


class LinearOut(QWidget):  # 输出UI
    def __init__(self, result=global_var.ResultRegression()):
        super(LinearOut, self).__init__()
        self.model = result.model
        data_test = result.data_test
        y_test = data_test.iloc[:, -1].values
        data_predict = result.data_predict
        y_predict = data_predict.iloc[:, -1].values
        mse = np.sum((y_predict - y_test) ** 2) / len(y_test)
        rmse = sqrt(mse)
        self.label_intercept = QLabel("intercept: ")
        intercept = result.intercept
        self.intercept = QLabel(str(intercept))
        self.label_coef = QLabel("coef: ")
        coef = result.coef
        self.coef = QLabel(str(coef))
        layout_1 = QHBoxLayout()
        layout_1.addWidget(self.label_intercept)
        layout_1.addWidget(self.intercept)
        layout_1.addWidget(self.label_coef)
        layout_1.addWidget(self.coef)
        self.label_MSE = QLabel("MSE: ")
        self.MSE_txt = QLabel(str(mse))
        self.label_RMSE = QLabel("RMSE: ")
        self.RMSE_txt = QLabel(str(rmse))
        layout_2 = QHBoxLayout()
        layout_2.addWidget(self.label_MSE)
        layout_2.addWidget(self.MSE_txt)
        layout_2.addWidget(self.label_RMSE)
        layout_2.addWidget(self.RMSE_txt)
        self.label_test = QLabel("测试集：")
        self.label_predict = QLabel("预测值：")
        self.table_test = DataTable(data_test)
        self.table_predict = DataTable(data_predict)
        layout_test = QVBoxLayout()
        layout_test.addWidget(self.label_test)
        layout_test.addWidget(self.table_test)
        layout_test.setStretch(0, 1)
        layout_test.setStretch(1, 5)
        layout_predict = QVBoxLayout()
        layout_predict.addWidget(self.label_predict)
        layout_predict.addWidget(self.table_predict)
        layout_predict.setStretch(0, 1)
        layout_predict.setStretch(1, 5)
        layout_3 = QHBoxLayout()
        layout_3.addLayout(layout_test)
        layout_3.addLayout(layout_predict)
        layout = QVBoxLayout()
        layout.addLayout(layout_1)
        layout.addLayout(layout_2)
        layout.addLayout(layout_3)
        self.setLayout(layout)


def linear_regression(taskData):
    """
    线性回归
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
    model = linear_model.LinearRegression()
    model.fit(X_train, y_train)
    y_predict = model.predict(X_test)
    data_test = pd.DataFrame(columns=columns[0: -1])  # 测试集
    data_predict = pd.DataFrame(columns=columns[0: -1])  # 预测值
    for index in range(len(X_test)):
        data_test.loc[index] = X_test[index]
        data_predict.loc[index] = X_test[index]
    data_test[columns[-1]] = y_test
    data_predict[columns[-1]] = y_predict
    result = global_var.ResultRegression()
    result.model = model
    result.data_test = data_test
    result.data_predict = data_predict
    result.columns = columns
    global_var.currentTask.result = result  # 结果保存
    # 可视化图表
    # Scatter().add_xaxis(xaxis_data=y_test).add_yaxis("实际值", y_test).add_yaxis("预测值", y_predict).render("linear.html")
    x = data_test.iloc[:, -1]
    y1 = x
    y2 = data_predict.iloc[:, -1]
    Scatter() \
        .add_xaxis(x) \
        .add_yaxis(
        "实际值",
        y1,
    ).add_yaxis(
        "预测值",
        y2,
    ).render("linear.html")
    # imgkit.from_file("./linear.html", "./linear.jpg")
    make_snapshot(snapshot, "./linear.html", "./linear.png")
    # img = cv2.imread("./linear.png")
    img = Image.open("./linear.png")
    re_img = img.resize((450, 400), Image.BILINEAR)
    # cv2.imwrite("./linear_resize.png", re_img)
    re_img.save("./linear_resize.png")


class LinearVisual(QWidget):
    def __init__(self):
        super(LinearVisual, self).__init__()
        # self.browser = QWebEngineView()
        # self.browser.load(QUrl('./linear.html'))
        layout = QVBoxLayout()
        pic_label = QLabel()
        pix = QPixmap("./linear_resize.png")
        pic_label.setPixmap(pix)
        pic_label.setScaledContents(False)
        pix.scaled(450, 400, aspectRatioMode=Qt.KeepAspectRatio)
        btn = QPushButton("show in browser")
        btn.clicked.connect(self.show_in_browser)
        # layout.addWidget(self.browser)
        layout.addWidget(pic_label)
        layout.addWidget(btn)
        self.setLayout(layout)

    def show_in_browser(self):
        import os
        url = "file://" + os.path.abspath("./linear.html")
        webbrowser.get('chrome').open(url, new=2)


