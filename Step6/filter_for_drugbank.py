import csv
import os

data_dir = os.path.join(os.path.dirname(os.getcwd()),"data")


drug_bank = set()
with open(os.path.join(data_dir,"structure_links.csv"),'r') as f:
  reader = csv.DictReader(f)
  for d in reader:
      drugbank_idx = d['DrugBank ID'].strip()
      chem_idx = d['ChEMBL ID'].strip()
      drug_bank.add(chem_idx)
     


fname = os.path.join(data_dir,"CORD19_co-occurrence_pairs_scored_filtered_uniprot.csv")
outfname = os.path.join(data_dir,"CORD19_co-occurrence_pairs_scored_filtered_db_uniprot.csv")

cnt=0
total_cnt=0
with open(fname,'r') as f, open(outfname,'w') as outf:
    header = next(f)
    outf.write(header)
    for line in f:
        total_cnt+=1
        x = line.split(',')[0]
        y = line.split(',')[1]
        if( "CORONAPROT#" in x and "DRUG#" in y):
            drug_idx = y.split("#")[1]
            if(drug_idx not in drug_bank):continue
            outf.write(line)
            cnt+=1

print("We read in %d tuples." % total_cnt)
print("We have %d tuples after filtering for small molecules in DrugBank!" % cnt)
