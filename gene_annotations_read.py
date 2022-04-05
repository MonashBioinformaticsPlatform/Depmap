from __future__ import annotations
from email.policy import default
from os import device_encoding, linesep
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
import sys
from bioservices.uniprot import UniProt


rec=pd.read_pickle('rec.txt')

with open('rec.csv','w') as f:
    rec.to_csv(f)

print(rec.columns)
print(rec.index)
output_dict={name:rec.loc[name]['Gene ontology (GO)'] for name in rec.index}

with open("rec_test.csv",'w') as f:
    w = csv.DictWriter(f,output_dict.keys())
    w.writeheader()
    w.writerow(output_dict)


#print(rec.loc['KTBL1_HUMAN'])
#print(output_dict)
