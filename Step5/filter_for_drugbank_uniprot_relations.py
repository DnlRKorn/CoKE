import csv
import os
human_proteins = set()
corona_proteins = set()

"human_proteins.tsv"
with open("data/human_proteins.tsv") as f:
  next(f)
  for line in f:
    prot_idx = line.split('\t')[0]
    human_proteins.add(prot_idx)

"corona_virus_proteins.tsv"
with open("data/corona_virus_proteins.tsv") as f:
  next(f)
  for line in f:
    prot_idx = line.split('\t')[0]
    corona_proteins.add(prot_idx)

"structure_links.csv"
drug_bank = set()
with open("data/structure_links.csv") as f:
  reader = csv.DictReader(f)
  for d in reader:
    chem_idx = d['ChEMBL ID'].strip()
    drug_bank.add(chem_idx)



fname = "CORD19_co-occurrence_pairs.csv.txt"



with open(fname) as f:
  for line in f:
    x = line.split(',')[0]
    y = line.split(',')[1]
    if( "CVPROT#" in x and "DRUG#" in y):
        prot_idx = x.split("#")[1]
        drug_idx = y.split("#")[1]
        if(prot_idx not in human_proteins and prot_idx not in corona_proteins):continue
        if(drug_idx not in drug_bank):continue
        sys.stdout.write(line)
