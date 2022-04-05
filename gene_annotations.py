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


db_genes=pd.read_pickle('genes/db_genes.txt')
#print(db_genes)

# *Always* tell NCBI who you are
Entrez.email = "benjamin.reames@monash.edu"


def retrieve_annotation(id_list):

    """Annotates Entrez Gene IDs using Bio.Entrez, in particular epost (to
    submit the data to NCBI) and esummary to retrieve the information.
    Returns a list of dictionaries with the annotations."""

    request = Entrez.epost("gene", id=",".join(id_list))
    try:
        result = Entrez.read(request)
    except RuntimeError as e:
        # FIXME: How generate NAs instead of causing an error with invalid IDs?
        print("An error occurred while retrieving the annotations.")
        print("The error returned was %s" % e)
        sys.exit(-1)

    webEnv = result["WebEnv"]
    queryKey = result["QueryKey"]
    #db='function'
    #db='gene'
    data = Entrez.esummary(db='function', webenv=webEnv, query_key=queryKey)
    annotations = Entrez.read(data)

    print("Retrieved %d annotations for %d genes" % (len(annotations), len(id_list)))

    return annotations

db_genes_dict={v:(k.strip('(')).strip(')') for [v,k] in db_genes}
#print(db_genes_dict)
ids_list=list(db_genes_dict.values())
ids_list_b1=ids_list[0:9999]
ids_list_b2=ids_list[9999:len(ids_list)]
#print(ids_list)

'''
annotations_b1=retrieve_annotation(ids_list_b1)
annotations_b2=retrieve_annotation(ids_list_b2)
print(annotations_b1['DocumentSummarySet']['DocumentSummary'][2].keys())
print(annotations_b1['DocumentSummarySet']['DocumentSummary'][2]['NomenclatureStatus'])
print(annotations_b2['DocumentSummarySet']['DocumentSummary'][2]['Description'])
'''

'''
ids_list=['57643','57688','125150']

x=retrieve_annotation(ids_list)
print((x['DocumentSummarySet']['DocumentSummary'][2])['LocationHist'])
'''

from bioservices.uniprot import UniProt
u = UniProt(verbose=False)
entrez_ids = ids_list
mapping = u.mapping(fr="P_ENTREZGENEID", to="ID", query=entrez_ids)

#print(mapping)
#uniprot_accs = [mapping[e][0] for e in entrez_ids]
uniprot_accs=[]
for e in entrez_ids:
    try:
        uniprot_accs.append(mapping[e][0])
        #print(uniprot_accs)
    except:
        pass
        #sys.exit(-1)
rec = u.get_df(uniprot_accs)
rec = rec.set_index('Entry name', drop=False)
print(rec)

with open('rec.txt','wb') as f:
    pickle.dump(rec,f)

##output=list(rec.loc[uniprot_accs[0]]['Gene ontology (GO)'])
##print(output)
