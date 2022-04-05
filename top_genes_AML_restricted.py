import pandas as pd
import numpy as np
from pandas.core.indexes.base import ensure_index 
from upsetplot import UpSet
from matplotlib import pyplot as plt

#Make function to get all gene Ids from gene names
#AML_cell_lines="/Users/brea0004/Desktop/Gilan Lab/cell lines in AML.csv"
#ALL_cell_lines="/Users/brea0004/Desktop/Gilan Lab/top_genes_ALL.py"
AML_cell_lines_restricted="/Users/brea0004/Desktop/Gilan Lab/cell lines in AML_restricted.csv"

cell_lines_df=pd.read_csv(AML_cell_lines_restricted,index_col=1)
cell_lines_ids_df=cell_lines_df.drop(columns=['Primary Disease','Tumor Type'])
print(cell_lines_ids_df)
print(cell_lines_ids_df.index)
def get_cellLine_ID(cell_line):
    cell_lines_dict=(cell_lines_ids_df.to_dict())['Depmap Id']
    return cell_lines_dict[cell_line]
#test
#print(get_cellLine_ID('MOLM13'))



# Calculate MSS for each cell line

#gene effect data
#I'm sure you can read in where you ignore header line etc should learn one day
gene_effect="/Users/brea0004/Desktop/Gilan Lab/CRISPR_gene_effect.csv"
df=pd.read_csv(gene_effect)
df=df.set_index('DepMap_ID')
#print(df.head(10))



# This view lets you see gene_effect table for a given cell line
def make_gene_effect_df(cellLine_Name, my_df):
    cellLine_Id=get_cellLine_ID(cellLine_Name) 
    #print(cellLine_Id)
    gene_effect_df=(my_df.loc[cellLine_Id]).to_frame()
    #print(gene_effect_df.head(10))
    #gene_effect_df=gene_effect_df.set_index(cellLine_Id)
    #gene_effect_df=gene_effect_df.to_frame()
    gene_effect_df=gene_effect_df.rename(columns={cellLine_Id:cellLine_Name})
    return gene_effect_df

# This view lets you see mean gene effect for each gene across all cell lines
def make_mean_gene_effect_df(my_df):
    mean_gene_effect_df=my_df.mean().to_frame()
    mean_gene_effect_df=mean_gene_effect_df.rename(columns={0:'Mean All Lines'})
    #print(mean_gene_effect_df.head(10))
    return mean_gene_effect_df

# This view lets you see gene effect for a cell line beside mean effect across cell lines
def make_gene_effect_diff_df(cellLine_Name, my_df):
    gene_effect_diff_df=pd.concat([make_gene_effect_df(cellLine_Name,my_df),make_mean_gene_effect_df(my_df)],axis=1)
    #gene_effect_diff_df=gene_effect_diff_df.rename(columns={0:'cellLine_Name'})
    #print(gene_effect_diff_df.head(10))
    return gene_effect_diff_df

# This view gives you MSS for each gene for a given cell line sorted from most essential to least, filtered on N
def make_pref_essential_df(cellLine_Name,my_df,N):
    mean_subtracted_df=((make_gene_effect_diff_df(cellLine_Name,my_df)[cellLine_Name]-make_gene_effect_diff_df(cellLine_Name,my_df)['Mean All Lines']).to_frame()).rename(columns={0:'MSS_'+ cellLine_Name})
    pref_essential_df=mean_subtracted_df.sort_values(by=['MSS_'+ cellLine_Name]).head(N)
    return pref_essential_df

#MOLM_df=make_gene_effect_df('MOLM13',df)
#a=make_mean_gene_effect_df(df)
#b=make_gene_effect_diff_df('MOLM13',df)
#print(MOLM_df.columns)
#print(MOLM_df.head(5))
#print(make_gene_effect_df('MOLM13',df))
#print(make_gene_effect_diff_df('MOLM13',df))

#=make_pref_essential_df('MOLM13',df,50)
#print(A)

# N.B. Some of the AML cell lines are not represented in the dataset...hench the try/catch

'''
###This is good syntax for some future use but easier here to be simpler?

def catch(func, *args, handle=lambda e : e, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        return str(handle(e))

B=[catch(make_pref_essential_df,*(cellLine_Name,df,50)) for cellLine_Name in cell_lines_ids_df.index]
print(B[-1])
'''
B=list()
C=list()
for cellLine_Name in cell_lines_ids_df.index:
    try:
        B.append(make_pref_essential_df(cellLine_Name,df,150))
    except KeyError:
        C.append(cellLine_Name)
B=pd.concat(B,axis=1)
#B=B.T
#print(B)
#print(C)


D=(B.notnull()).rename(columns=lambda x: x[4:] + '*')
D.to_pickle("./AML_restricted_mat.pkl")
#print(D)



E=pd.concat([B,D],axis=1)
E=E.set_index(list(D.columns))
#print(E)


upset = UpSet(E, subset_size='count', intersection_plot_elements=5,min_degree=0)
#upset.add_catplot(value='median_value', kind='strip', color='blue')
#upset.add_catplot(value='AGE', kind='strip', color='black')
upset.plot()
plt.title("UpSet with catplots")
plt.show()
print(C)

'''

###Now can avoid the regular expressions?

import re
my_pattern=re.compile('ACH')
matches=[my_pattern.match(str(entry)) for entry in B]
#matches=[re.search(my_pattern,str(entry)) for entry in B]
print(matches)
#C=catch(pd.concat,*(B,'axis=1'))
#print(B)

'''

'''
print(df.mean())
genes_mean_df=(df.mean()).to_frame()
print(genes_mean_df.columns)
genes_mean_df=genes_mean_df.rename(columns={0:'Mean All Genes'})
frames_df=pd.concat([genes_MOLM_df,genes_mean_df], axis=1)

print(frames_df.head(5))

mean_subtracted_df=((frames_df['ACH-000362']-frames_df['Mean All Genes']).to_frame()).rename(columns={0:'MSS'})
pref_essential_df=mean_subtracted_df.sort_values(by=['MSS'])
print(pref_essential_df.head(50))

'''

