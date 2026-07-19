#例-透视表

import pandas as pd

# 导入数据
df=pd.read_excel('航天进出口额.xlsx')

# 从指标中提取国家和地区
df['指标'] = df['指标'].str.split('_').str[-2]

# 重命名列名为国家和地区
df = df.rename(columns={'指标': '国家和地区'})

# 创建pivot_table
pivot_df = pd.pivot_table(df, 
                          index=['国家和地区'], 
                          columns=['进出口'],
                          values=['2023-12', '2023-11', '2023-10'], 
                          aggfunc='sum', 
                          fill_value=0)

print(pivot_df)
print()

pivot_df = pd.pivot_table(df, 
                          index=['国家和地区', '进出口'], 
                          values=['2023-12', '2023-11', '2023-10'], 
                          aggfunc='sum', 
                          fill_value=0)

print(pivot_df)

rolling_avg = df.rolling(window=3, 
                         axis=1, 
                         min_periods=1, 
                         center=False, 
                         win_type=None).mean()

print(rolling_avg)

