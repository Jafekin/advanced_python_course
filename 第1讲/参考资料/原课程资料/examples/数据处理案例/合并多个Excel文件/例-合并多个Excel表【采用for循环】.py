#例-合并多个Excel表【采用for循环】.py
#当有许多个Excel表时，分别采用for循环进行数据导入和多个二维数据表的合并

import pandas as pd

#1、导入Excel文件
#name=['df1','df2','df3']          #用列表存储二维数据表的名称【文件较少时直接写出数据表的名称】
name=[]
for i in range(0,3):              #用列表存储二维数据表的名称【文件较多时采用for循环写出数据表的名称】
    name.append('df'+str(i+1))

for i in range(0,3):
    name[i]=pd.read_excel('数据表'+str(i+1)+'.xlsx')        #读入Excel文件，返回一个二维数据表
    #注意:因为这里Excel文件为Microsoft Excel工作表，其后缀为.xlsx，故read_excel()函数中，文件名后缀不能是“.xls”
print('df1:\n',name[0])
print('df2:\n',name[1])
print('df3:\n',name[2])
print()

#2、merge方法合并三个数据集，并返回合并后数据集
df=name[0]                                #初始数据表
for i in range(1,3):                      #【如果有n个Excel文件，只需修改range的上限为n】   
    df=pd.merge(df,name[i],how='outer')   #合并df和name[i]，并集
print('合并后的\'一带一路\'贸易指数:\n',df)

#3、修改行索引【因为合并后数据集的行索引有重复，均为0~9】
df_count=df['时间'].count()                 #二维数据表的行数
print('合并后的\'一带一路\'贸易指数表的行数:',df_count)
df.index = [i+1 for i in range(0,df_count)]  #修改行索引为1、2、3……

#4、导出数据
df.to_excel('合并后的一带一路贸易指数表new.xlsx')         #写入Excel文件





