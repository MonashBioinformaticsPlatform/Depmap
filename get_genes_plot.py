import numpy as np
import pandas as pd
import pprint
from pandas.core.indexing import convert_missing_indexer
import xlsxwriter

mat1=pd.read_pickle("/Users/brea0004/Desktop/Gilan Lab/AML_mat.pkl")
mat2=pd.read_pickle("/Users/brea0004/Desktop/Gilan Lab/ALL_mat.pkl")
mat3=pd.read_pickle("/Users/brea0004/Desktop/Gilan Lab/AML_restricted_mat.pkl")
shp1=mat1.shape
shp2=mat2.shape
shp3=mat3.shape

A=mat1.astype(int)
B=mat2.astype(int)
C=mat3.astype(int)
#df.somecolumn = df.somecolumn.replace({True: 1, False: 0})

A_sum=A.sum(axis=1)
B_sum=B.sum(axis=1)
C_sum=C.sum(axis=1)

A_genes=(A_sum[A_sum>=10]).index.values
B_genes=(B_sum[B_sum>=8]).index.values
C_genes=(C_sum[C_sum>=1]).index.values
print(A_genes)
print(B_genes)
print(C_genes)

my_dict={}
for i in range(len(A_genes)):
    temp=mat1.loc[A_genes[i]].squeeze()
    temp_list=temp[temp==True].index.values
    my_dict[A_genes[i]]=temp_list

#C=pd.DataFrame(data=my_dict)

my_dict2={}
for i in range(len(B_genes)):
    temp=mat2.loc[B_genes[i]].squeeze()
    temp_list=temp[temp==True].index.values
    my_dict2[B_genes[i]]=temp_list
#D=pd.DataFrame(data=my_dict2)

my_dict3={}
for i in range(len(C_genes)):
    temp=mat3.loc[C_genes[i]].squeeze()
    temp_list=temp[temp==True].index.values
    my_dict3[C_genes[i]]=temp_list

'''
with pd.ExcelWriter('upset_shared.xlsx') as writer: 
    C.to_excel(writer,sheet_name='AML>=10')
    D.to_excel(writer,sheet_name='ALL>=10')
'''

workbook = xlsxwriter.Workbook('upset_shared.xlsx')
worksheet1=workbook.add_worksheet("AML>=10")
worksheet2=workbook.add_worksheet("ALL>=8")
worksheet3=workbook.add_worksheet("AML_restricted>=1")

row = 0
col = 0
for key in my_dict.keys():
    row += 1
    worksheet1.write(row, col, key)
    for item in my_dict[key]:
        worksheet1.write(row, col + 1, item)
        row += 1
row=0
col=0
for key in my_dict2.keys():
    row += 1
    worksheet2.write(row, col, key)
    for item in my_dict2[key]:
        worksheet2.write(row, col + 1, item)
        row += 1
row=0
col=0
for key in my_dict3.keys():
    row += 1
    worksheet3.write(row, col, key)
    for item in my_dict3[key]:
        worksheet3.write(row, col + 1, item)
        row += 1

workbook.close()