import numpy as np
import pandas as pd
import xlwt

mat1=pd.read_pickle("/Users/brea0004/Desktop/Gilan Lab/AML_mat.pkl")
mat2=pd.read_pickle("/Users/brea0004/Desktop/Gilan Lab/ALL_mat.pkl")
mat3=pd.read_pickle("/Users/brea0004/Desktop/Gilan Lab/AML_restricted_mat.pkl")
shp1=mat1.shape
shp2=mat2.shape
shp3=mat3.shape
#print(shp)

##### AML sheet


with pd.ExcelWriter('bloodlines.xlsx') as writer:   
    
    A=mat1.iloc[:,0]
    A=A[A]
    B={A.name: A.index.values}
    B=pd.DataFrame(data=B)

    for i in range(1,shp1[1]):
        A=mat1.iloc[:,i]
        A=A[A]
        B[A.name]=A.index.values
    B.to_excel(writer,sheet_name='AML')

##### ALL sheet

    A=mat2.iloc[:,0]
    A=A[A]
    B={A.name: A.index.values}
    B=pd.DataFrame(data=B)

    for i in range(1,shp2[1]):
        A=mat2.iloc[:,i]
        A=A[A]
        B[A.name]=A.index.values
    B.to_excel(writer,sheet_name='ALL')
    
##### AML restricted sheet

    A=mat3.iloc[:,0]
    A=A[A]
    B={A.name: A.index.values}
    B=pd.DataFrame(data=B)

    for i in range(1,shp3[1]):
        A=mat3.iloc[:,i]
        A=A[A]
        B[A.name]=A.index.values
    B.to_excel(writer,sheet_name='AML_restricted')




'''
for i in range(shp[1]):
    A=mat.iloc[:,i]
#B=A.where(A==True)
    B=A[A].to_frame()
    pd.DataFrame(columns=B.columns).to_csv("forgot.csv", index=False, mode='a')
    B.to_csv("forgot.csv", header=None,mode='a')
'''
