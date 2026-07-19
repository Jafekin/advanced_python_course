#例-合并.py

import pandas as pd
import numpy as np

#1、创建二维数据表
data1={'时间': ['2022-03', '2022-04', '2022-05', '2022-06'], 
       '东南亚': [148.26, 186.95, 196.61, 202.2]}
data2={'时间': ['2022-07', '2022-08', '2022-09', '2022-10'], 
       '东南亚': [223.77, 214.95, 207.38, 230.66]}
df1 = pd.DataFrame(data1,index=range(4))  
df2 = pd.DataFrame(data2,index=range(4,8))

print("df1:\n",df1)
print("df2:\n",df2)
print()

#2、merge方法合并两个数据集，并返回合并后数据集
df_outer=pd.merge(df1,df2,how='outer')       #并集
print("df1与df2合并后的df_outer：\n",df_outer)

df_inner=pd.merge(df1,df2,how='inner')       #交集
print("df1与df2合并后的df_inner：\n",df_inner)

'''
  import pandas as pd
df1:
         时间     东南亚
0  2022-03  148.26
1  2022-04  186.95
2  2022-05  196.61
3  2022-06  202.20
df2:
         时间     东南亚
4  2022-07  223.77
5  2022-08  214.95
6  2022-09  207.38
7  2022-10  230.66

df1与df2合并后的df_outer：
         时间     东南亚
0  2022-03  148.26
1  2022-04  186.95
2  2022-05  196.61
3  2022-06  202.20
4  2022-07  223.77
5  2022-08  214.95
6  2022-09  207.38
7  2022-10  230.66
df1与df2合并后的df_inner：
 Empty DataFrame
Columns: [时间, 东南亚]
Index: []



'''