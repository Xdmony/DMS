# author:Xdmony
# contact: jerkyadmon@gmail.com
# datetime:2020/4/22 10:31 下午
# software: PyCharm
# description:

"""
文件说明：任务控制器，执行选择的任务，输出数据为operateData
"""
import global_var
from operate.data_mining import linearRegression, decideTreeClassifier, k_meansCluster, associationApriori
from operate.data_pre import cleaning,maxmin,pcaa

def execute(operate):
    operates = global_var.allOperateList
    if operate == operates[0][0]:       # "数据清洗"
        taskData = global_var.currentTask
        cleaning.cleaning_atr(taskData)
        
    elif operate == operates[0][1]:     # 数据变换
        taskData = global_var.currentTask
        maxmin.get_maxmin(taskData)
       
    elif operate == operates[0][2]:     # 数据规约
        taskData = global_var.currentTask
        pcaa.get_pca(taskData)
   
    elif operate == operates[1][0]:     # 关联分析
        taskData = global_var.currentTask
        associationApriori.apriori_association(taskData)
    elif operate == operates[2][0]:     # 聚类分析
        taskData = global_var.currentTask
        k_meansCluster.k_means_cluster(taskData)
    elif operate == operates[3][0]:     # 分类分析
        taskData = global_var.currentTask
        decideTreeClassifier.decision_tree_classify(taskData)
    elif operate == operates[4][0]:     # 回归分析
        taskData = global_var.currentTask
        linearRegression.linear_regression(taskData)
    elif operate == operates[5][0]:     # 可视化
        pass



