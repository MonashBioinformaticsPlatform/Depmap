#function for get cell_line ID from name
#this might have an error?

'''
def get_cellLine_ID(cell_line):
    cell_lines_dict=(cell_lines_ids_df.to_dict())['Depmap Id']
    return cell_lines_dict[cell_line]
'''

# This view lets you see gene_effect table for a given cell line

def make_gene_effect_df(cellLine_Id, my_df):
    #cellLine_Id=get_cellLine_ID(cellLine_Name) 
    #print(cellLine_Id)
    gene_effect_df=(my_df.loc[cellLine_Id]).to_frame()
    #print(gene_effect_df.head(10))
    #gene_effect_df=gene_effect_df.set_index(cellLine_Id)
    #gene_effect_df=gene_effect_df.to_frame()
    
    
    '''
    put names back in later
    gene_effect_df=gene_effect_df.rename(columns={cellLine_Id:cellLine_Name})
    '''
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


def invert_dict(fin_df):
    inv_dict=defaultdict(list)
    for tis in fin_df.index:
        for gene in fin_df.columns:
            temp_dict=dict(my_dict[gene])
            my_list=[k[0] for k in my_dict[gene]]
            if tis in my_list:
                inv_dict[tis].append((gene,temp_dict[tis]))


def write_tissues_genes_xls(my_dict,inv_dict):
    workbook = xlsxwriter.Workbook('tissues_genes.xlsx')
    worksheet1=workbook.add_worksheet("genes_for_tissues")
    worksheet2=workbook.add_worksheet("tissues_for_genes")

    my_dict=dict(my_dict)
    inv_dict=dict(inv_dict)
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
            row+=1
        row += 1

    workbook.close()