import os
import csv
import jinja2

data_dir = os.path.join(os.path.dirname(os.getcwd()),"data")

prot_drug_hits = {}
for csv_fname in os.listdir(os.path.join(data_dir,'csv')):
    print(csv_fname)
    prot_name = csv_fname.split(".")[0]
    with open(os.path.join(data_dir,'csv',csv_fname),'r') as f:
        next(f) #header
        num_drugs = 0
        for line in f:
            num_drugs+=1
        prot_drug_hits[prot_name] = num_drugs

prot_names = {}

with open(os.path.join(data_dir,"human_proteins.tsv"),'r') as f:
  next(f)
  for line in f:
    prot_idx = line.split('\t')[0]
    prot_name = line.split('\t')[3].split('(')[0]
    if(prot_idx.strip()=="P0DTC2"): prot_name = "Spike glycoprotein (SARS-CoV-2)"
    if(prot_idx.strip()=="P59594"): prot_name = "Spike glycoprotein (SARS-CoV)"
    prot_names[prot_idx] = prot_name

with open(os.path.join(data_dir,"corona_virus_proteins.tsv"),'r') as f:
  next(f)
  for line in f:
    prot_idx = line.split('\t')[0]
    prot_name = line.split('\t')[3].split('(')[0]
    if(prot_idx.strip()=="P0DTC2"): prot_name = "Spike glycoprotein (SARS-CoV-2)"
    if(prot_idx.strip()=="P59594"): prot_name = "Spike glycoprotein (SARS-CoV)"
    prot_names[prot_idx] = prot_name

    
protein_info = []
for prot in prot_drug_hits:
    if(prot=="singleton"):continue
    link = "https://coke.mml.unc.edu/static/dtd_table_json.html#%s" % prot 
    num_drugs = prot_drug_hits[prot]
    prot_name = prot_names[prot]
    d = { "link":link , "idx":prot, "name":prot_name, "hits":num_drugs }
    protein_info.append(d)

with open(os.path.join("templates","ui.html"),'r') as f: template = f.read()
template = jinja2.Template(template)
rendered = template.render(protein_info=protein_info)
with open(os.path.join(data_dir,"html","index.html"),'w') as f:
    f.write(rendered)


tables_info = []
for prot in prot_drug_hits:
    if(prot=="singleton"):continue
    link = "https://www.uniprot.org/uniprot/%s" % prot 
    prot_name = "(" + prot_names[prot].strip() + ")"
    d = { "idx":prot, "title":prot,  "uniprot_link":link, "protein_name":prot_name }
    tables_info.append(d)

with open(os.path.join("templates","dtd_table_json.html"),'r') as f: template = f.read()
template = jinja2.Template(template)
rendered = template.render(tables_info=tables_info)
with open(os.path.join(data_dir,"html","dtd_table.html"),'w') as f:
    f.write(rendered)
with open(os.path.join(data_dir,"html","dtd_table_json.html"),'w') as f:
    f.write(rendered)
    
d = { "idx":"singleton", "protein_name":"All Targets" }
rendered = template.render(tables_info=[d])
with open(os.path.join(data_dir,"html","dtd_table_singleton.html"),'w') as f:
    f.write(rendered)


### Build target_info.html.
target_infos = {} 
with  open(os.path.join(data_dir,"corona_virus_proteins.tsv"),'r') as csvfile:
  reader = csv.DictReader(csvfile,delimiter='\t')
  for row in reader:
      prot_idx = row["Entry"]
      target_infos[prot_idx] = row

with  open(os.path.join(data_dir,"human_proteins.tsv"),'r') as csvfile:
  reader = csv.DictReader(csvfile,delimiter='\t')
  for row in reader:
      prot_idx = row["Entry"]
      target_infos[prot_idx] = row

target_info_rows = []
for prot in prot_drug_hits:
    if(prot=="singleton"):continue
    target_info = target_infos[prot]
    d = {}
    d["prot_idx"] = prot
    d["entry_name"] = target_info["Entry name"]
    d["status"] = target_info["Status"]
    d["prot_name"] = target_info["Protein names"]
    d["gene"] = target_info["Gene names"]
    d["gene_length"] = target_info["Length"]
    d["organism"] = target_info["Organism"]
    d["drug_count"] = prot_drug_hits[prot]

    target_info_rows.append(d)

with open(os.path.join("templates","target_info.html"),'r') as f: template = f.read()
template = jinja2.Template(template)
rendered = template.render(targets=target_info_rows)
with open(os.path.join(data_dir,"html","target_info.html"),'w') as f:
    f.write(rendered)


downloads = []
for prot in prot_drug_hits:downloads.append(prot)
with open(os.path.join("templates","downloads.html"),'r') as f: template = f.read()
template = jinja2.Template(template)
rendered = template.render(downloads=downloads)
with open(os.path.join(data_dir,"html","downloads.html"),'w') as f:
    f.write(rendered)
