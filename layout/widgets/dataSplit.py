import sys
import pandas as pd
from math import floor
from PyQt5.QtWidgets import (
    QWidget, QFormLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QApplication, QVBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from sklearn.tree import DecisionTreeClassifier
from layout.widgets.dataTable import PandasModel
import global_var



class DataSplit(QWidget):
    confirmed = pyqtSignal()

    def __init__(self, parent: QWidget = None):
        super(DataSplit, self).__init__(parent)
        self.mainWindow: layout.MainWindow.MainWindow = parent
        self.setWindowFlag(Qt.Window)
        self.control_init()
        self.layout_init()

    def control_init(self):
        """
        初始化控件
        """
        # 文本框(从几列到几列)
        self.inputLineEdit1 = QLineEdit()
        self.inputLineEdit2 = QLineEdit()

        # 设置显示效果
        self.inputLineEdit1.setEchoMode(QLineEdit.Normal)
        self.inputLineEdit2.setEchoMode(QLineEdit.Normal)

        # 提交按钮
        self.submit_button = QPushButton()
        self.submit_button.setText('确认')
        self.submit_button.clicked.connect(self.on_submit)
        # 数据划分按钮
        self.cancel_button = QPushButton()
        self.cancel_button.setText('取消')
        self.submit_button.clicked.connect(self.on_cancel)

    def layout_init(self) -> QVBoxLayout:
        self.data_select_layout1 = QHBoxLayout()
        self.data_select_layout1.addWidget(self.inputLineEdit1)
        self.data_select_layout1.addWidget(QLabel('列，至'))
        self.data_select_layout1.addWidget(self.inputLineEdit2)
        self.data_select_layout1.addWidget(QLabel('列'))

        # 创建一个表单布局
        self.flayout = QFormLayout()
        # 把文本框添加到布局，第一个参数为左侧的说明标签
        self.flayout.addRow("输入数据", self.data_select_layout1)

        # 底部布局
        downLayout = QHBoxLayout()
        downLayout.addWidget(self.cancel_button)
        downLayout.addWidget(self.submit_button)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.flayout)
        self.layout.addLayout(downLayout)
        self.layout.setStretch(1, 1)
        # 把设置的布局加载到窗口
        self.setLayout(self.layout)

    def on_submit(self):#点击确定
        self.confirmed.emit()
        self.close()

    def on_cancel(self):#点击取消
        self.close()

    def get_data_range(self):#设置范围
        ####得到此数据集行数
        out_dict: dict = {}
        data = pd.read_csv(global_var.filePath)
        a = len(data)
        n_tr_samples = a
        if self.inputLineEdit1 is not None and self.inputLineEdit2 is not None:
            in_tr_range: tuple = (
                0, n_tr_samples,
                int(self.inputLineEdit1.text()),
                int(self.inputLineEdit2.text()) )

            out_dict['in_train'] = in_tr_range
        return out_dict

    def del_datain_row(self):
        self.flayout.removeRow(self.data_select_layout1)
        self.data_select_layout1 = None
        self.inputLineEdit1 = None
        self.inputLineEdit2 = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = DataSplit()
    win.show()
    sys.exit(app.exec_())
