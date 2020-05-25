# author:Xdmony
# contact: jerkyadmon@gmail.com
# datetime:2020/4/22 1:18 下午
# software: PyCharm
# description:

"""
文件说明：数据集列表框
"""
from PyQt5.QtCore import QSize, pyqtSignal,Qt
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QPushButton

import global_var


itemSize = QSize(100, 30)


class List(QListWidget):
    update_ = pyqtSignal(str)

    def __init__(self):
        QListWidget.__init__(self)

    def add_item(self, dataName):
        item = QListWidgetItem()
        item.setSizeHint(itemSize)
        self.addItem(item)
        itemBtn = QPushButton(dataName)
        self.setItemWidget(item, itemBtn)
        itemBtn.clicked.connect(self.item_click)
        # itemBtn.setContextMenuPolicy(Qt.CustomContextMenu)
        # itemBtn.customContextMenuRequested.connect()

    def item_click(self):
        dataName = self.sender().text()
        self.update_.emit(dataName)

    def refresh(self):
        self.clear()
        for data in global_var.allDataSet.data_in:
            self.add_item(data)

    ##for 
