import pandas as pd
import numpy as np
from pandas.core.indexes.base import ensure_index 
from upsetplot import UpSet
from matplotlib import pyplot as plt
##########
import tissues.py
##########

B=list()
C=list()
for cellLine_Name in cell_lines_ids_df.index:
    try:
        B.append(make_pref_essential_df(cellLine_Name,df,10))
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