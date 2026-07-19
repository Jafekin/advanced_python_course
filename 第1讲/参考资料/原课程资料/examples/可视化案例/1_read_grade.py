# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

data=pd.read_excel('grade_data.xlsx')
print(data.info())

# 去除有异常值的行
condition = data['大学物理B1'] > 100
# condition是一个Boolean列表
# 取反即为保留正常值
data = data[~condition]
print(data.info())

data.dropna(axis=0, how='any', subset=None, inplace=True)

#print(data.info())
print(data)

