# 缺失值的生成与判断

import pandas as pd
import numpy as np
 
df = pd.DataFrame(np.random.randn(10,6))    #二维数据表共10行，6列
# Make a few areas have NaN values
df.iloc[1:3,1] = np.nan      #第1行、第2行的第1列生成NaN【不能直接写nan或NaN】
#df.iloc[1:3,1] = pd.NaT      #第1行、第2行的第1列生成NaT【不能写成pd.nat】
df.iloc[5,3] = np.nan        #第5行、第3列生成NaN
df.iloc[7:9,5] = np.nan      #第7行、第8行的第5列生成NaN
df.columns = ['a','b','c','d','e','f'] #修改列索引
print("df：\n",df)
print()

#2、判断是否有缺失值
result_with_null = df.isnull()     #返回DateFrame,元素为空或者NA就显示True，否则显示False
print("返回标记元素为空或者NA的DateFrame，result_with_null：\n",result_with_null)
print()

#3、找到包含空值的行
result_with_null = df.isnull().any(axis=1)  
#axis=1表示按行显示。返回的是一个Series，其索引为df的行号；每行的值为True（包含空值）或False（不包含空值）
print("每行是否包含空值的结果：")
print(result_with_null)
print()
rows_with_null = df[df.isnull().any(axis=1)]
print("所有包含空值的行：")
print(rows_with_null)
print()

#4、找到包含空值的列
columns_with_null = df.isnull().any()   
#默认axis=0，表示按列显示。返回的是一个Series，其索引为df的列号；每行的值为True（包含空值）或False（不包含空值）
print("包含空值的列：")
print(columns_with_null)
print()

# 5、获取包含空值的行列名，并保存在一个列表中
null_indices = df.isnull().stack()
print("\n包含空值的行列名：")
print(null_indices)

# 6、用空值的前一个值【本列中某空值上一行的值】填充空值
df.b=df.b.fillna(method="ffill")             #修改第b’列的值，填充空值。df['b']表示'b'列，同df.b
print("\n用空值的前一个值填充b列后，df：\n",df)
df.to_excel("用空值的前一个值填充b列后.xlsx")

#7、用一列的非空值填充另一列对应行的空值
df.loc[df['d'].isnull(),'d']=df[df['d'].isnull()]['a']   #用'a'列的非空值填充'd'列的空值
print("\n用一列的非空值填充另一列对应行的空值后，df：\n",df)

'''
df：
           a         b         c         d         e         f
0  3.133360  2.800814 -1.054013  0.490795  0.989456  2.145158
1  0.764450       NaN  0.913545  1.661622 -0.069769 -0.442298
2  1.290654       NaN  1.115407  0.436551  0.389376 -0.120280
3  1.752582  1.415331  1.821160 -0.350061  0.552231  0.080941
4  0.533792  0.698710 -0.881925 -0.986384  1.512841 -0.790807
5 -0.499003 -0.488162 -1.362521       NaN  0.540322  2.138577
6 -0.638436 -0.873295  1.156515  1.008900 -0.169405 -0.430629
7  0.168660 -0.046631  0.446283  1.544401  0.453591       NaN
8 -2.547088 -1.346964 -0.105812  0.511952  0.010335       NaN
9  0.959437 -2.607264  0.915461 -0.858582  2.254896  0.173703

返回标记元素为空或者NA的DateFrame，result_with_null：
        a      b      c      d      e      f
0  False  False  False  False  False  False
1  False   True  False  False  False  False
2  False   True  False  False  False  False
3  False  False  False  False  False  False
4  False  False  False  False  False  False
5  False  False  False   True  False  False
6  False  False  False  False  False  False
7  False  False  False  False  False   True
8  False  False  False  False  False   True
9  False  False  False  False  False  False

每行是否包含空值的结果：
0    False
1     True
2     True
3    False
4    False
5     True
6    False
7     True
8     True
9    False
dtype: bool

所有包含空值的行：
          a         b         c         d         e         f
1  0.764450       NaN  0.913545  1.661622 -0.069769 -0.442298
2  1.290654       NaN  1.115407  0.436551  0.389376 -0.120280
5 -0.499003 -0.488162 -1.362521       NaN  0.540322  2.138577
7  0.168660 -0.046631  0.446283  1.544401  0.453591       NaN
8 -2.547088 -1.346964 -0.105812  0.511952  0.010335       NaN

包含空值的列：
a    False
b     True
c    False
d     True
e    False
f     True
dtype: bool


包含空值的行列名：
0  a    False
   b    False
   c    False
   d    False
   e    False
   f    False
1  a    False
   b     True
   c    False
   d    False
   e    False
   f    False
2  a    False
   b     True
   c    False
   d    False
   e    False
   f    False
3  a    False
   b    False
   c    False
   d    False
   e    False
   f    False
4  a    False
   b    False
   c    False
   d    False
   e    False
   f    False
5  a    False
   b    False
   c    False
   d     True
   e    False
   f    False
6  a    False
   b    False
   c    False
   d    False
   e    False
   f    False
7  a    False
   b    False
   c    False
   d    False
   e    False
   f     True
8  a    False
   b    False
   c    False
   d    False
   e    False
   f     True
9  a    False
   b    False
   c    False
   d    False
   e    False
   f    False
dtype: bool

用空值的前一个值填充b列后，df：
           a         b         c         d         e         f
0  3.133360  2.800814 -1.054013  0.490795  0.989456  2.145158
1  0.764450  2.800814  0.913545  1.661622 -0.069769 -0.442298
2  1.290654  2.800814  1.115407  0.436551  0.389376 -0.120280
3  1.752582  1.415331  1.821160 -0.350061  0.552231  0.080941
4  0.533792  0.698710 -0.881925 -0.986384  1.512841 -0.790807
5 -0.499003 -0.488162 -1.362521       NaN  0.540322  2.138577
6 -0.638436 -0.873295  1.156515  1.008900 -0.169405 -0.430629
7  0.168660 -0.046631  0.446283  1.544401  0.453591       NaN
8 -2.547088 -1.346964 -0.105812  0.511952  0.010335       NaN
9  0.959437 -2.607264  0.915461 -0.858582  2.254896  0.173703

用一列的非空值填充另一列对应行的空值后，df：
           a         b         c         d         e         f
0  3.133360  2.800814 -1.054013  0.490795  0.989456  2.145158
1  0.764450  2.800814  0.913545  1.661622 -0.069769 -0.442298
2  1.290654  2.800814  1.115407  0.436551  0.389376 -0.120280
3  1.752582  1.415331  1.821160 -0.350061  0.552231  0.080941
4  0.533792  0.698710 -0.881925 -0.986384  1.512841 -0.790807
5 -0.499003 -0.488162 -1.362521 -0.499003  0.540322  2.138577
6 -0.638436 -0.873295  1.156515  1.008900 -0.169405 -0.430629
7  0.168660 -0.046631  0.446283  1.544401  0.453591       NaN
8 -2.547088 -1.346964 -0.105812  0.511952  0.010335       NaN
9  0.959437 -2.607264  0.915461 -0.858582  2.254896  0.173703


'''