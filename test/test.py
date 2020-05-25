from apyori import apriori
import pandas as pd

data = [['豆奶','莴苣'],
        ['莴苣','尿布','葡萄酒','甜菜'],
        ['豆奶','尿布','葡萄酒','橙汁'],
        ['莴苣','豆奶','尿布','葡萄酒'],
        ['莴苣','豆奶','尿布','橙汁']]

df = pd.DataFrame(data)

result = list(apriori(transactions=df))
print(result)