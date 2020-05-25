# author:Xdmony
# contact: jerkyadmon@gmail.com
# datetime:2020/4/22 1:15 下午
# software: PyCharm
# description:

"""
文件说明：编辑区
"""
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QTabWidget, QWidget


class OperateTab(QTabWidget):
    def __init__(self):
        QTabWidget.__init__(self)
        self.setTabsClosable(True)
        self.setTabShape(QTabWidget.Triangular)
        self.setDocumentMode(True)
        self.tabCloseRequested.connect(self.close_Tab)
        self.setMovable(True)

    def close_Tab(self, index):
        self.removeTab(index)

    def add_Tab(self, tab, title):
        self.addTab(tab, title)

    def find_tab(self, title):
        tab = self.findChild(QWidget, title)
        if tab == QWidget:
            self.setCurrentWidget(tab)
            return True
        elif tab == None:
            return False
