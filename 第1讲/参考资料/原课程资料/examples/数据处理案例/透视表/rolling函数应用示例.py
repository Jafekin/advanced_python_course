# rolling函数应用示例.py

import pandas as pd

df = pd.DataFrame({"col1": list(range(10)), "col2": list(range(1, 11))}) #, "col3": ["xx"] * 10
print("df：\n",df)
print()

rolling_sum = df.rolling(window=3, min_periods=1, win_type="boxcar").sum()  
#滑动窗口求和（每三行）。默认axis=0，按列滚动计算；默认center=False，不将计算结果放在窗口的中间位置

print('rolling_sum：',rolling_sum)

"""
df：
    col1  col2
0     0     1
1     1     2
2     2     3
3     3     4
4     4     5
5     5     6
6     6     7
7     7     8
8     8     9
9     9    10

rolling_sum：
   col1  col2
0   0.0   1.0
1   1.0   3.0
2   3.0   6.0
3   6.0   9.0
4   9.0  12.0
5  12.0  15.0
6  15.0  18.0
7  18.0  21.0
8  21.0  24.0
9  24.0  27.0

【例如：对于col1列：
0   0.0   #0+0+=0=0
1   1.0   #0+0+1=1
2   3.0   #0+1+2=3
3   6.0   #1+2+3=6
4   9.0   #2+3+4=9
5  12.0   #3+4+5=12
6  15.0   #4+5+6=15
7  18.0   #5+6+7=18
8  21.0   #6+7+8=21
9  24.0   #7+8+9=24】

【若center=True，则计算结果放在窗口的中间位置：】
rolling_sum：    col1  col2
0   1.0   3.0
1   3.0   6.0
2   6.0   9.0
3   9.0  12.0
4  12.0  15.0
5  15.0  18.0
6  18.0  21.0
7  21.0  24.0
8  24.0  27.0
9  17.0  19.0

"""
