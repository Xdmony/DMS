"""
散点图选择
"""
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QDialog, QPushButton, QHBoxLayout,QMessageBox,QFormLayout,QWidget,QLabel,QComboBox
import matplotlib.pyplot as plt
from PyQt5.QtGui import QPixmap
import numpy as np
import pandas as pd
import seaborn as sns
import sys
from PyQt5 import Qt
import global_var

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

class SNShow(QWidget):
    def __init__(self):
        super().__init__()

        # 几个QWidgets
        #self.figure = plt.figure()  # 可选参数,facecolor为背景颜色
        #self.canvas = FigureCanvas(self.figure)
        self.button_draw = QPushButton("绘图")
        self.lab1=QLabel()
        self.c1 = DataCol()
        self.a1 = QLabel("x轴")
        self.c2 = DataCol()
        self.a2 = QLabel("y轴")
    

        # 连接事件
        self.button_draw.clicked.connect(self.Draw)

        # 设置布局
        layout1=QFormLayout()
        layout1.addRow(self.a1,self.c1)
        layout1.addRow(self.a2,self.c2)
        layout1.addRow(self.button_draw)
        layout = QHBoxLayout()
        layout.addWidget(self.lab1)
        layout.addLayout(layout1)
        self.setLayout(layout)

    def Draw(self):
        da = pd.read_csv(global_var.filePath)
        
        current_palette = sns.color_palette()
        sns.set(style="dark", palette="colorblind", color_codes=True)
        # 设置散点图x轴与y轴以及data参数
        if self.c1.dataColBox.currentText() != "" and self.c2.dataColBox.currentText() != "":
            x1=self.c1.dataColBox.currentText()
            y1=self.c2.dataColBox.currentText()
        else:
           QMessageBox.critical(self,'标题','定义错误',QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
        sns.relplot(x=x1, y=y1, data=da)
        plt.title('data visualize')
        # 保存画出来的图片
        plt.savefig('22.png')
        self.lab1.setPixmap(QPixmap('22.png'))


# 运行程序
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    s = SNShow()
    s.show()
    app.exec()



