import csv
drugs = [] 
pairs = {} 
#with open("advanced_pair_counts_dtd_scored.csv") as f:
#  next(f)
with open("data/pair_counts_dtd_drugbank_uni_1_2_scored.txt") as f:
  next(f)
  for line in f:
    drug = line.split(',')[1]
    drug = drug.split("#")[1]
    drugs.append(drug)
    targ = line.split(",")[0]
    targ = targ.split("#")[1]
    s = pairs.get(targ,set())
    s.add(drug)
    pairs[targ] = s
print(len(drugs),len(set(drugs)))
drugs = set(drugs)
drug_bank = set()
with open("data/structure_links.csv") as f:
  reader = csv.DictReader(f)
  for d in reader:
    chem = d['ChEMBL ID'].strip()
#    if(chem in drugs):print('HI')
    if(len(chem)>2):
      #print(chem)
      drug_bank.add(chem)

print(len(drugs.intersection(drug_bank)))
with open("data/coke_filtered_drugs.txt",'w') as f:
  for drug in drugs.intersection(drug_bank):
    f.write(drug + '\n')
      
