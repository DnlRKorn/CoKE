import csv
import os

data_dir = os.path.join(os.path.dirname(os.getcwd()),"data")

drugs = set()
for csv_fname in os.listdir(os.path.join(data_dir,'csv')):
    print(csv_fname)
    with open(os.path.join(data_dir,'csv',csv_fname),'r') as csv_file:
         reader = csv.DictReader(csv_file)
         keys = ["DrugBank ID","ChEMBL ID","Name","SMILES"]
         for row in reader:
             l = [row[k] for k in keys]
             drugs.add(tuple(l))

drugs = list(drugs)
drugs.sort()

with open(os.path.join(data_dir,'drug_list.csv'),'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(keys)
    for row in drugs:
        writer.writerow(row)
