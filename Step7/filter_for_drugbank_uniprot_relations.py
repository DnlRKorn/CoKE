import csv
import os
from bs4 import BeautifulSoup

data_dir = os.path.join(os.path.dirname(os.getcwd()),"data")


amino_acids = set()
with open(os.path.join(data_dir,"DBCAT000021"),'r') as htmlfile:
    soup = BeautifulSoup(htmlfile.read(), 'html.parser')
    table = soup.find("table")
    arefs = table.find_all("a")
    for a in arefs:
        drugbank_id = a['href'].split("/")[2]
        amino_acids.add(drugbank_id)

amino_drugs = set()
with open(os.path.join(data_dir,"structure_links.csv"),'r') as f:
  reader = csv.DictReader(f)
  for d in reader:
      drugbank_idx = d['DrugBank ID'].strip()
      chem_idx = d['ChEMBL ID'].strip()
      if(drugbank_idx in amino_acids):
          amino_drugs.add(chem_idx)
     

fname = os.path.join(data_dir,"CORD19_co-occurrence_pairs_scored_filtered_db_uniprot.csv")
outfname = os.path.join(data_dir,"CORD19_co-occurrence_pairs_scored_filtered_db_uniprot_amino.csv")

cnt=0
total_cnt=0
with open(fname,'r') as f, open(outfname,'w') as outf:
    header = next(f)
    outf.write(header)
    for line in f:
        total_cnt+=1
        x = line.split(',')[0]
        y = line.split(',')[1]
        if( "CVPROT#" in x and "DRUG#" in y):
            prot_idx = x.split("#")[1]
            drug_idx = y.split("#")[1]
            if(drug_idx in amino_drugs):continue
            outf.write(line)
            cnt+=1
print("We read in %d tuples." % total_cnt)
print("We have %d tuples after filtering out amino acids!" % cnt)
