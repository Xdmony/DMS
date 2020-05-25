# author:Xdmony
# contact: jerkyadmon@gmail.com
# datetime:2020/4/25 8:47 下午
# software: PyCharm
# description:

"""
文件说明：散点图，需设置横纵轴参数，用pyecharts实现
参考文档：https://pyecharts.org/#/zh-cn/intro
"""
from PyQt5.QtCore import QUrl
# from PyQt5.QtWebEngineWidgets import QWebEngineView
from PySide2.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication


class Visual(QWidget):
    def __init__(self):
        super(Visual, self).__init__()
        self.browser = QWebEngineView()
        self.browser.load(QUrl("www.baidu.com"))
        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        self.setLayout(layout)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    visual = Visual()
    visual.show()
    sys.exit(app.exec_())