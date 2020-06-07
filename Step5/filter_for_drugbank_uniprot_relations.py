import csv
import os
from bs4 import BeautifulSoup

data_dir = os.path.join(os.path.dirname(os.getcwd()),"data")

outfname = os.path.join(data_dir,"CORD19_co-occurrence_pairs_scored_filtered.csv")

amino_acids = set()
with open(os.path.join(data_dir,"DBCAT000021"),'r') as htmlfile:
    soup = BeautifulSoup(htmlfile.read(), 'html.parser')
    table = soup.find("table")
    arefs = table.find_all("a")
    for a in arefs:
        drugbank_id = a['href'].split("/")[2]
        amino_acids.add(drugbank_id)

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
amino_drugs = set()
with open(os.path.join(data_dir,"structure_links.csv"),'r') as f:
  reader = csv.DictReader(f)
  for d in reader:
      drugbank_idx = d['DrugBank ID'].strip()
      chem_idx = d['ChEMBL ID'].strip()
      if(drugbank_idx in amino_acids):
          amino_drugs.add(chem_idx)
      else:
          drug_bank.add(chem_idx)
     




fname = os.path.join(data_dir,"CORD19_co-occurrence_pairs_scored_filtered.csv")
outfname = os.path.join(data_dir,"CORD19_co-occurrence_pairs_scored_filtered_db_uniprot.csv")

amino_hits = 0
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
            if(drug_idx in amino_drugs):amino_hits+=1
            if(drug_idx not in drug_bank):continue
            outf.write(line)
print("%d amino acids in our drug database"%amino_hits)
