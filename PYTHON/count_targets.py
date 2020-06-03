import csv

human_proteins = set()
corona_proteins = set()

with open("data/human_proteins.tsv") as f:
  next(f)
  for line in f:
    prot_idx = line.split('\t')[0]
    human_proteins.add(prot_idx)

with open("data/corona_virus_proteins.tsv") as f:
  next(f)
  for line in f:
    prot_idx = line.split('\t')[0]
    corona_proteins.add(prot_idx)

drug_bank = set()
with open("data/structure_links.csv") as f:
  reader = csv.DictReader(f)
  for d in reader:
    chem_idx = d['ChEMBL ID'].strip()
    drug_bank.add(chem_idx)

targs = {}
with open("data/pair_counts_dtd_drugbank_uni_1_2_scored.txt") as f:
  next(f)
  for line in f:
    l = line.split(',')
    prot = l[0].split("#")[1]
    chem = l[1].split("#")[1]
    if("CHEMBL" not in chem):
      print("BAD",line)
      exit()
    if(chem not in drug_bank):
      raise ValueError("Drug not in referenced DrugBank database.",chem)
    if(prot not in human_proteins and prot not in corona_proteins):
      raise ValueError("Target not in referenced UniProt database.",prot)
    s = targs.get(prot,set())
    s.add(chem)
    targs[prot] = s 

keys = list(targs.keys())
keys.sort()
for k in keys:
  print(k,len(targs[k]))

def updateDict(d):
  d2 = {}
  for x in d:
    d2[x] = d[x]
  d2["Entry"] = '<a href="https://www.uniprot.org/uniprot/%s">%s</a>' %(d["Entry"],d["Entry"])
  d2["Drug_Count"] = '<a href="http://coke.mml.unc.edu/static/dtd_table.html#%s">%s</a>' %(d[ "Entry"],d["Drug_Count"])
#  d2["Entry name"] = '<a href="https://www.uniprot.org/uniprot/%s">%s</a>' %(d["Entry"],d["Entry"])
  return d2

table = []
with  open("target_info.html",'w') as f2:
  csvfile = open("data/corona_virus_proteins.tsv")
  reader = csv.DictReader(csvfile,delimiter='\t')
  targets = list(reader)
  csvfile.close()

  fields = reader.fieldnames
  csvfile = open("data/human_proteins.tsv")
  reader = csv.DictReader(csvfile,delimiter='\t')
  targets.extend(list(reader))
  csvfile.close()

  fields.append("Drug_Count")
  table.append(fields)
  f2.write('''<style>
  table {
    border-collapse: collapse;
    }

    table, th, td {
      border: 1px solid black;
      }
          </style>
          ''')
  f2.write("<table>\n<tr>")
  for x in fields:
    f2.write("<th>%s</th>"%x)
  f2.write("</tr>\n")
  
  for d in targets:
    cnt = len(targs.get(d['Entry'],[]))

    d['Drug_Count'] = cnt
    if(cnt==0):continue
    d = updateDict(d)
    f2.write("<tr>")
    for x in fields:
      f2.write("<th>%s</th>"%d[x])
    f2.write("</tr>\n")
#    writer.writerow(d)
#  f2.write("\n\n")
#  csvfile = open("uniprot_targs2.txt")
#  reader = csv.DictReader(csvfile,delimiter='|')
  for d in targets:
    #cnt = len(targs[d['Entry']])
    cnt = len(targs.get(d['Entry'],[]))

    d['Drug_Count'] = cnt
    if(cnt==0):continue

    d = updateDict(d)
    f2.write("<tr>")
    for x in fields:
      f2.write("<th>%s</th>"%d[x])
    f2.write("</tr>\n")
  f2.write("</table>")

#with open("targets.txt",'w') as f:
#  for x in keys:
#    #f.write(x + ',' + str(targs[x])+ '\n')
#    f.write(x + ',' + str(len(targs[x]))+ '\n')
#    # print(x,len(targs[x]))
