import seaborn as sns
heat=sns.heatmap(fin);
plt.show()
heat2=sns.heatmap(C);
plt.show()

workbook = xlsxwriter.Workbook('tissues_genes.xlsx')
worksheet1=workbook.add_worksheet("genes_for_tissues")
worksheet2=workbook.add_worksheet("tissues_for_genes")
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
            row+=1
    row += 1

workbook.close()