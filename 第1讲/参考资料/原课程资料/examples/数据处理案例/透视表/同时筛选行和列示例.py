#同时筛选行和列示例.py

import pandas as pd
# 假设有 5 个人，分别参加了 4 门课程，获得了对应的分数
data = {'name' : pd.Series(['Alice', 'Bob', 'Cathy', 'Dany', 'Ella']),
        'Math_A' : pd.Series([1.1, 2.2, 3.3, 4.4, 5]),
        'English_A' : pd.Series([3, 2.6, 2, 1.7, 3]),
        'Math_B' : pd.Series([1.7, 2.5, 3.6, 2.4, 5]),
        'English_B' : pd.Series([5, 2.6, 2.4, 1.3, 3]),
     }

df = pd.DataFrame(data)
print("df：\n",df)
print()

#通过切片 df.loc[ : , : ]筛选
#df_sel1=df.loc[:2,'English_A':'English_B']
df_sel1=df.loc[:,'English_A':'English_B']     #所有行，'English_A'~'English_B'列
print("筛选后df_sel1：\n",df_sel1)
print()
# 注意，这里的切片 与 Python 本身的不同，包含了结尾！
# 所以这个例子中包含了 第 2 行 和 'English_B' 列

#通过选择 序号 选择列 df.iloc[ : , : ] 筛选
df_sel2=df.iloc[:2, [0,3]]    # 注意，这里的切片没有包含第 2 行！同时选择了 第 0 列 和 第 3 列
print("筛选指定的几列，df_sel2：\n",df_sel2)
print()

df_sel3=df.iloc[:2, 0:4]    # 选择连续几列，同时选择了 第 0 列 ~ 第 3 列【不包括上限】
print("筛选连续几列，df_sel3：\n",df_sel3)

'''
df：
     name  Math_A  English_A  Math_B  English_B
0  Alice     1.1        3.0     1.7        5.0
1    Bob     2.2        2.6     2.5        2.6
2  Cathy     3.3        2.0     3.6        2.4
3   Dany     4.4        1.7     2.4        1.3
4   Ella     5.0        3.0     5.0        3.0

筛选后df_sel1：
   English_A  Math_B  English_B
0        3.0     1.7        5.0
1        2.6     2.5        2.6
2        2.0     3.6        2.4

筛选指定的几列，df_sel2：
     name  Math_B
0  Alice     1.7
1    Bob     2.5

筛选连续几列，df_sel3：
     name  Math_A  English_A  Math_B
0  Alice     1.1        3.0     1.7
1    Bob     2.2        2.6     2.5
'''
