# author:Xdmony
# contact: jerkyadmon@gmail.com
# datetime:2020/4/22 1:13 下午
# software: PyCharm
# description:

"""
文件说明：任务列表框，clear可以清空任务列表，add添加任务框
"""
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget, QListWidget, QListView, QListWidgetItem, QPushButton, QHBoxLayout
import global_var

size = QSize(80, 60)


class TaskProgress(QWidget):
    def __init__(self):
        super(TaskProgress, self).__init__()
        self.taskList = QListWidget()  # 列表框控件，显示任务流程
        self.taskList.setFlow(QListView.LeftToRight)  # 设置List样式
        # self.btn_add = QPushButton("添加")  # 添加任务框
        # self.btn_add.clicked.connect(self.add_task_input)
        self.btn_clear = QPushButton("清空")  # 清空任务
        self.btn_clear.clicked.connect(self.task_clear)
        # 布局设置
        layout = QHBoxLayout()
        layout.addWidget(self.taskList)
        layout.addWidget(self.btn_clear)
        # layout.addWidget(self.btn_add)
        layout.setStretch(0, 6)
        layout.setStretch(1, 1)
        layout.setStretch(2, 1)
        self.setLayout(layout)

    def add_data(self, data_name):
        """
        添加数据
        :param data_name: 数据集
        :return:
        """
        if self.taskList.count() == 0:
            widget = QPushButton(data_name)
            item = QListWidgetItem()
            item.setSizeHint(size)
            self.taskList.addItem(item)
            self.taskList.setItemWidget(item, widget)

    def add_task_input(self):
        """
        添加任务输入框用于添加任务
        :return:
        """
        if self.taskList.count() >= 1:
            item = QListWidgetItem()
            self.taskList.addItem(item)

    def add_task(self, taskName):
        """
        添加任务
        :param taskName: 任务
        :return:
        """
        # if type(self.taskList.currentItem()) == QListWidgetItem:
        #     item = self.taskList.currentItem()
        #     taskWidget = QPushButton(taskName)
        #     self.taskList.setItemWidget(item, taskWidget)
        taskWidget = QPushButton(taskName)
        item = QListWidgetItem()
        item.setSizeHint(size)
        self.taskList.addItem(item)
        self.taskList.setItemWidget(item, taskWidget)

    def task_clear(self):
        """
        清空任务
        :return:
        """
        global_var.currentTask.__init__()  # 清空任务指针
        self.taskList.clear()


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    progress = TaskProgress()
    progress.show()
    sys.exit(app.exec_())
