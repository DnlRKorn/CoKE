import os
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
    prot_names[prot_idx] = prot_name

with open(os.path.join(data_dir,"corona_virus_proteins.tsv"),'r') as f:
  next(f)
  for line in f:
    prot_idx = line.split('\t')[0]
    prot_name = line.split('\t')[3].split('(')[0]
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
with open("test.html",'w') as f: f.write(rendered)


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
with open("test.html",'w') as f: f.write(rendered)
    
d = { "idx":"singleton", "protein_name":"All Targets" }
rendered = template.render(tables_info=[d])
with open("test.html",'w') as f: f.write(rendered)
