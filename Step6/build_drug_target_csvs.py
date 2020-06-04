import csv
import os

data_dir = os.path.join(os.path.dirname(os.getcwd()),"data")
csv_dir = os.path.join(os.path.dirname(os.getcwd()),"data","csv")

drugs = set() 
pairs = {} 
papers = {}
scores = {}

cord19_fname = os.path.join(data_dir,"CORD19_co-occurrence_pairs_scored_filtered_db_uniprot.csv")
with open(cord19_fname) as f:
  next(f)
  for line in f:
      drug = line.split(',')[1]
      drug = drug.split("#")[1]
      drugs.add(drug)
      targ = line.split(",")[0]
      targ = targ.split("#")[1]
      s = pairs.get(targ,set())
      s.add(drug)
      pairs[targ] = s
      papers[(targ,drug)] = line.strip().split(",")[6:] 
      scores[(targ,drug)] = line.strip().split(",")[5]

bank_ids = set()
chembl_to_bank = {}
bank_ids_to_uni = {}

with open(os.path.join(data_dir,"structure_links.csv"),'r') as f:
  reader = csv.DictReader(f)
  for d in reader:
    chem = d['ChEMBL ID'].strip()
    if(chem in drugs):
      d_bank = d["DrugBank ID"]
      bank_ids.add(d_bank)
      chembl_to_bank[chem] = d_bank

for x in bank_ids:
  bank_ids_to_uni[x] = set()

#Count the number of targets a drug has on UniProt.
with open(os.path.join(data_dir,"uniprot_links.csv"),'r') as f:
  reader = csv.DictReader(f)
  for d in reader:
    bank = d["DrugBank ID"]
    if(bank in bank_ids):
      s = bank_ids_to_uni[bank]
      s.add(d["UniProt ID"])
      bank_ids_to_uni[bank] = s

for x in bank_ids_to_uni:
    print(x,len(bank_ids_to_uni[x]))

#["Target","Name","DrugBank ID","ChEMBL ID","SMILES","Other Targets","Score","Paper Links"]:
all_tuples = []
for targ in pairs:
   outfname = os.path.join(data_dir,'csv',"%s.csv"%targ)
   with open(outfname,'w') as csvfile:
       writer = csv.DictWriter(csvfile,fieldnames=["Target","Name","DrugBank ID","ChEMBL ID","SMILES","Other Targets","Score","Papers"])
       writer.writeheader()
       with open(os.path.join(data_dir,"structure_links.csv")) as f2:
             reader = csv.DictReader(f2)
             for d in reader:
               chem = d['ChEMBL ID'].strip()
               if(chem in pairs[targ]):
                   bank_id = d["DrugBank ID"]
                   targs = len(bank_ids_to_uni[bank_id])
                   
                   write_dict = {}
                   write_dict["Target"] = targ
                   write_dict["Name"] = d["Name"]
                   write_dict["SMILES"] = d["SMILES"]
                   write_dict["DrugBank ID"] = bank_id
                   write_dict["ChEMBL ID"] = chem
                   write_dict["Other Targets"] = targs
                   write_dict["Score"] = scores[(targ,chem)] 
                   write_dict["Papers"] = '|'.join(papers[(targ,chem)])

                   writer.writerow(write_dict)
                   all_tuples.append(write_dict)
                   
outfname = os.path.join(data_dir,'csv',"singleton.csv")
with open(outfname,'w') as csvfile:
    writer = csv.DictWriter(csvfile,fieldnames=["Target","Name","DrugBank ID","ChEMBL ID","SMILES","Other Targets","Score","Papers"])
    writer.writeheader()
    for d in all_tuples: writer.writerow(d)
'''
j = []
for targ in pairs:
   with open("data/structure_links_filtered.csv") as f2:
         reader = csv.DictReader(f2)
         for d in reader:
           chem = d['ChEMBL ID'].strip()
           if(chem in pairs[targ]):
             #tup_count+=1
             bank = d["DrugBank ID"]
             cnt = d["Targets"]
             smile = d["SMILES"]
             d["Target"] = targ
             d["Other Targets"] = cnt
             d = convertDict(d)
             l = []
             for x in ["Target","Name","DrugBank ID","ChEMBL ID","SMILES","Other Targets","Score","Paper Links"]:
               l.append(d[x])
             j.append(l)
json_data = {"data":j}
with open("data/singleton.json",'w') as f:
   json.dump(json_data,f)
'''
