from email.policy import default
from os import device_encoding, linesep
from statistics import quantiles
import pandas as pd
import numpy as np
from pandas.core.indexes.base import ensure_index 
from upsetplot import UpSet
from matplotlib import pyplot as plt
from collections import defaultdict
import seaborn as sns
import xlsxwriter
from Bio import Entrez
from operator import itemgetter
import csv
import pickle

### Call in tissues and cell line files// create arrays

my_file=open("tissues_files.txt",'r')
file_list=my_file.readlines()
my_file.close()
file_list=sorted([x.split(",") for x in file_list],key=itemgetter(0))

def remove_tis(my_list,*args):
    temp=[]
    for element in my_list:
        if element[0] in args:
            #my_list.remove(element)
            pass
        else:
            temp.append(element)
    #print(my_list)
    return temp
my_file=open("to_remove.txt")
to_remove=my_file.readlines()
my_file.close()
to_remove=sorted([t.strip() for t in to_remove],key=itemgetter(0))

file_list=remove_tis(file_list,*to_remove)
tissues=[t[0] for t in file_list]
print(tissues)
cell_line_paths=[t[1].strip() for t in file_list]

### make data frames//call in database
## Could add the other scores?
tissue_dict={my_tissue: my_csv for (my_tissue,my_csv) in zip(tissues,cell_line_paths)}
cell_lines_dfs=[pd.read_csv(csv_file) for csv_file in cell_line_paths]
cell_lines_ids_df=[my_df.drop(columns=['Primary Disease','Tumor Type','Cell Line']) for my_df in cell_lines_dfs]
tissue_cell_dict={my_tissue: my_df for (my_tissue,my_df) in zip(tissues,cell_lines_ids_df)}
gene_effect="/Users/brea0004/Desktop/Gilan Lab/CRISPR_gene_effect.csv"
df=pd.read_csv(gene_effect)
df=df.set_index('DepMap_ID')

### Creating dictionaries from dataframe with genes and scores
ind=[]
for my_tis in tissues:
    tis_ind=tissue_cell_dict[my_tis].iloc[:,0].values
    tis_ind=zip([my_tis]*len(tis_ind),tis_ind)
    ind.append([list(x) for x in tis_ind])
def flatten_list(a_list):
    return [item for sublist in a_list for item in sublist]
ind=flatten_list(ind)


d_ind=defaultdict(list)
for [v,k] in ind:
    d_ind[k].append(v)
##Function Map gene to its tissue
def gene_to_tis(my_gene):
    tt=d_ind[my_gene]
    try:
        return tt[0]
    except:
        return "no tissue"
##Function for mapping genes to tuple (tissue,gene,score)
def gene_to_tis_tup(my_gene):
    return (gene_to_tis(my_gene),my_gene)

#Create Multiindex view
new_index = pd.MultiIndex.from_tuples([gene_to_tis_tup(g) for g in df.index], names=["tissue", "cell lines"])
df.index=new_index


#Create dataframes with means and means by tissues over genes
A=df.groupby("tissue").mean()
B=df.mean()

all_cell_lines_ge=[elem[1] for elem in df.index]
all_cell_lines=flatten_list([list(x["Depmap Id"]) for x in cell_lines_ids_df])
db_counts={tis:len(df.loc[tis,:]) for tis in [elem[0] for elem in df.index]}
with open('./cell_lines/db_counts.csv', 'w') as f:  # You will need 'wb' mode in Python 2.x
    w = csv.DictWriter(f, db_counts.keys())
    w.writeheader()
    w.writerow(db_counts)

db_genes=df.columns.values
db_genes=[x.split(' ') for x in db_genes]
with open('./genes/db_genes.txt', 'wb') as f:  # You will need 'wb' mode in Python 2.x
    pickle.dump(db_genes,f)
    
#print(len(set(all_cell_lines_ge)))
#print(len(set(all_cell_lines)))

### Test for Particular Genes
'''
gene1='MYB (4602)'
gene2='EP300 (2033)'
gene3='ESR1 (2099)'

C1=A[gene1]-B[gene1]
C2=A[gene2]-B[gene2]
C3=A[gene3]-B[gene3]



#print(df.index)
tis='Blood'
mytup= [ ]
for tis in C1.index:
    a=(tis, C1[tis], C2[tis],C3[tis])
    #try:
    mytup.append(a)
    #except:
    #    pass
    #print(C1[tis])
    #print(C2[tis])
    #print(C3[tis])


C=pd.DataFrame(mytup,columns=['tissue',gene1,gene2,gene3])
C.set_index('tissue',inplace=True)

MYB=C[gene1].sort_values(ignore_index=True)


heat2=sns.heatmap(C);
plt.show()

'''

## Make dictionary and inverse dictionary for genes passing threshold in each tissue

a=[]
for gene in df.columns:
    temp=(A[gene]-B[gene])
    a.append(temp)
fin=pd.concat(a,axis=1)

threshold=-.25
my_dict=defaultdict(list)
for gene in fin:
    #threshold=-.16
    for tis in fin.index:
        val=fin.loc[tis,gene]
        if (val<threshold):
            my_dict[gene].append((tis,val))


inv_dict=defaultdict(list)
for tis in fin.index:
    for gene in fin.columns:
        temp_dict=dict(my_dict[gene])
        my_list=[k[0] for k in my_dict[gene]]
        if tis in my_list:
            inv_dict[tis].append((gene,temp_dict[tis]))


### Make Boxplot of passing genes by tissues
keys=inv_dict.keys()
genes=[[t[0] for t in inv_dict[key]] for key in keys]
lengths=[len(elem) for elem in genes]
labels=(list(zip(keys,lengths)))
labels=[' '.join(map(str,elem)) for elem in labels]
scores=[[t[1] for t in inv_dict[key]] for key in keys]
my_plot=plt.violinplot(scores,vert=False, widths=1,showmeans=False, showmedians=True, bw_method='silverman')
plt.yticks(range(1,len(keys)+1), labels, fontsize=7, rotation=45)
for pc in my_plot['bodies']:
    pc.set_facecolor('#D43F3A')
    pc.set_edgecolor('black')
    pc.set_alpha(1)
plt.show()

### Make heatmaps
heat=sns.heatmap(fin);
plt.show()



### Write Results to Spreadsheet
workbook = xlsxwriter.Workbook('tissues_genes.xlsx')
worksheet1=workbook.add_worksheet("genes_for_tissues")
worksheet2=workbook.add_worksheet("tissues_for_genes")
worksheet3=workbook.add_worksheet("tissues_for_genes_na")
#worksheet3=workbook.add_worksheet("AML_restricted>=1")

my_dict=dict(my_dict)
inv_dict=dict(inv_dict)
#print(inv_dict["Blood"])
row = 0
col = 0
for key in my_dict.keys():
    row += 1
    worksheet1.write(row, col, key)
    for item in my_dict[key]:
            worksheet1.write(row,col+1,item[0])
            worksheet1.write(row, col + 2, item[1])
            row+=1
    row += 1
row=0
col=0
for key in inv_dict.keys():
    row += 1
    worksheet2.write(row, col, key)
    for item in inv_dict[key]:
            worksheet2.write(row,col+1,item[0])
            worksheet2.write(row, col + 2, item[1])
            worksheet3.write(row, col, key)
            worksheet3.write(row,col+1,item[0])
            worksheet3.write(row, col + 2, item[1])
            row+=1
    row += 1

workbook.close()
'''
row=0
col=0
for key in inv_dict.keys():
    row += 1
    worksheet3.write(row, col, key)
    for item in inv_dict[key]:
            worksheet3.write(row, col, key)
            worksheet3.write(row,col+1,item[0])
            worksheet3.write(row, col + 2, item[1])
            row+=1
    row += 1

workbook.close()
'''

'''
row=0
col=0
for key in inv_dict.keys():
    row += 1
    worksheet2.write(row, col, key)
    for item in enumerate(inv_dict[key]):
        worksheet2.write(row, col + item[0]+1, item[1])
        row += 1

workbook.close()
'''

#function for get cell_line ID from name
#this might have an error?

def get_cellLine_ID(cell_line):
    cell_lines_dict=(cell_lines_ids_df.to_dict())['Depmap Id']
    return cell_lines_dict[cell_line]


# This view lets you see gene_effect table for a given cell line

def make_gene_effect_df(cellLine_Id, my_df):
    #cellLine_Id=get_cellLine_ID(cellLine_Name) 
    #print(cellLine_Id)
    gene_effect_df=(my_df.loc[cellLine_Id]).to_frame()
    #print(gene_effect_df.head(10))
    #gene_effect_df=gene_effect_df.set_index(cellLine_Id)
    #gene_effect_df=gene_effect_df.to_frame()
    
    
  
    return gene_effect_df

# This view lets you see mean gene effect for each gene across all cell lines
def make_mean_gene_effect_tissue_df(my_df,tissue):
    
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

