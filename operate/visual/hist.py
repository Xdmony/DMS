"""
直方图调整中，当下只对iris生效
"""
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QDialog, QPushButton, QHBoxLayout,QLabel,QWidget
from PyQt5 import Qt
import matplotlib.pyplot as plt
import sys
from PyQt5.QtGui import QPixmap
import pandas as pd
import global_var
from sklearn.datasets import load_iris


class Histshow(QWidget):
    def __init__(self):
        super(Histshow,self).__init__()
        layout = QHBoxLayout()
        self.lab1=QLabel()      
        layout.addWidget(self.lab1)
        self.setLayout(layout)

        colList = global_var.currentData.data.columns.tolist()
        name=[]

        for col in colList:
            name.append(col)
        iris = load_iris()
        data= "D:\data\iris.data"
        dataset = pd.read_csv(data,names=name)
        dataset.hist() #数据直方图histograms
        plt.title("属性直方图")
        plt.savefig('n1.png')
        self.lab1.setPixmap(QPixmap('n1.png'))


if __name__ == "__main__":
    app=0
    app = QtWidgets.QApplication(sys.argv)
    my = Histshow()
    my.show()
    sys.exit(app.exec_())
