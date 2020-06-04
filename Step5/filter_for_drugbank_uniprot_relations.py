import csv
import os

data_dir = os.path.join(os.path.dirname(os.getcwd()),"data")

outfname = os.path.join(data_dir,"CORD19_co-occurrence_pairs_scored_filtered.csv")

human_proteins = set()
corona_proteins = set()

with open(os.path.join(data_dir,"human_proteins.tsv"),'r') as f:
  next(f)
  for line in f:
    prot_idx = line.split('\t')[0]
    human_proteins.add(prot_idx)

with open(os.path.join(data_dir,"corona_virus_proteins.tsv"),'r') as f:
  next(f)
  for line in f:
    prot_idx = line.split('\t')[0]
    corona_proteins.add(prot_idx)

drug_bank = set()
with open(os.path.join(data_dir,"structure_links.csv"),'r') as f:
  reader = csv.DictReader(f)
  for d in reader:
    chem_idx = d['ChEMBL ID'].strip()
    drug_bank.add(chem_idx)



fname = os.path.join(data_dir,"CORD19_co-occurrence_pairs_scored_filtered.csv")
outfname = os.path.join(data_dir,"CORD19_co-occurrence_pairs_scored_filtered_db_uniprot.csv")

with open(fname,'r') as f, open(outfname,'w') as outf:
    header = next(f)
    outf.write(header)
    for line in f:
        x = line.split(',')[0]
        y = line.split(',')[1]
        if( "CVPROT#" in x and "DRUG#" in y):
            prot_idx = x.split("#")[1]
            drug_idx = y.split("#")[1]
            if(prot_idx not in human_proteins and prot_idx not in corona_proteins):continue
            if(drug_idx not in drug_bank):continue
            outf.write(line)
