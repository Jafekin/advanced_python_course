#any函数与any方法

import pandas as pd
     
# 示例1：使用any()函数判断列表中是否存在至少一个为True的元素
lst = [False, False, True]
result = any(lst)
print(result)  # 输出: True
     
# 示例2：使用any(axis=1)方法判断DataFrame的每一行是否存在至少一个为True的元素
df = pd.DataFrame({'A': [False, False, True], 'B': [True, False, False]})
result = df.any(axis=1)

print("df：\n",df)
print()
print(result)

'''
 输出:
df：
        A      B
0  False   True
1  False  False
2   True  False

0     True
1    False
2     True
'''



