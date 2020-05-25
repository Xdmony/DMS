# author:Xdmony
# contact: jerkyadmon@gmail.com
# datetime:2020/4/22 1:23 下午
# software: PyCharm
# description:

"""
文件说明：关联规则
"""
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import *
from apyori import apriori
import pandas as pd

import global_var
from layout.widgets.dataTable import DataTable


class AprioriAssociationEdit(QWidget):
    addTask_ = pyqtSignal(str)

    def __init__(self):
        super(AprioriAssociationEdit, self).__init__()
        layout1 = QHBoxLayout()
        layout2 = QHBoxLayout()
        layout3 = QHBoxLayout()
        label_supp = QLabel("最小支持度：")
        self.input_supp = QLineEdit()
        layout1.addWidget(label_supp)
        layout1.addWidget(self.input_supp)
        layout1.addStretch(1)
        label_conf = QLabel("最小置信度：")
        self.input_conf = QLineEdit()
        layout2.addWidget(label_conf)
        layout2.addWidget(self.input_conf)
        layout2.addStretch(1)
        label_lift = QLabel("最小提升度：")
        self.input_lift = QLineEdit()
        layout3.addWidget(label_lift)
        layout3.addWidget(self.input_lift)
        layout3.addStretch(1)
        layout = QVBoxLayout()
        layout.addLayout(layout1)
        layout.addLayout(layout2)
        layout.addLayout(layout3)
        layout4 = QHBoxLayout()
        add_task = QPushButton("添加到任务")
        add_task.clicked.connect(self.add_task)
        layout4.addStretch(2)
        layout4.addWidget(add_task)
        layout.addLayout(layout4)
        layout.addStretch(5)
        self.setLayout(layout)

    def add_task(self):
        """
        添加任务
        :return:
        """
        global_var.currentTask.support = eval(self.input_supp.text())
        global_var.currentTask.confidence = eval(self.input_conf.text())
        global_var.currentTask.lift = eval(self.input_lift.text())
        global_var.currentTask.resultType = global_var.DataMiningType.ASSOCIATION
        global_var.currentTask.operateList.append(global_var.allOperateList[1][0])
        self.addTask_.emit(global_var.allOperateList[1][0])



class AprioriAssociationOut(QWidget):
    def __init__(self, result=global_var.ResultAssociation()):
        super(AprioriAssociationOut, self).__init__()
        self.table = DataTable(result.rule)
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)


def apriori_association(taskData):
    """
    Apriori关联分析
    :param taskData:
    :return:
    """
    data = taskData.operateData.data  # 操作数据
    min_supp = global_var.currentTask.support
    min_conf = global_var.currentTask.confidence
    min_lift = global_var.currentTask.lift
    # transactions = data.to_numpy()
    items = (data['0'].unique())
    encoded_vals = []
    for index, row in data.iterrows():
        labels = {}
        uncommons = list(set(items) - set(row))
        commons = list(set(items).intersection(row))
        for uc in uncommons:
            labels[uc] = 0
        for com in commons:
            labels[com] = 1
        encoded_vals.append(labels)
    ohe_df = pd.DataFrame(encoded_vals)
    ap = list(apriori(transactions=ohe_df,
                      min_support=min_supp, min_confidence=min_conf, min_lift=min_lift))
    # 支持度（support），先输入空列表，再进行赋值
    supports = []
    # 置信度
    confidences = []
    # 提升度
    lifts = []
    # 基于项items_base
    bases = []
    # 推导项items_add
    adds = []

    for r in ap:
        for x in r.ordered_statistics:
            supports.append(r.support)
            confidences.append(x.confidence)
            lifts.append(x.lift)
            bases.append(list(x.items_base))
            adds.append(list(x.items_add))
    # 将结果存储为dataframe
    result = pd.DataFrame({
        'support': supports,
        'confidence': confidences,
        'lift': lifts,
        'base': bases,
        'add': adds
    })
    # result = result[~result['base'].isin(['[]'])]  # 删去base为空值的规则
    #
    # # 选择支持度大于0.1，自信度大于0.3
    # res = result[(result.lift > 0.0) & (result.support > 0.1) & (result.confidence > 0.3)]
    # res = res.reset_index(drop=True)  # 重置索引
    associaResult = global_var.ResultAssociation()
    associaResult.rule = result
    global_var.currentTask.result = associaResult
