
html = '''
<style>
  .flex-container {
  flex-direction: row-reverse;
    display: flex;
    flex-wrap: wrap;
    /*line-height: 75px;*/
    justify-content: center;
    padding: 0;
    margin: 0;
  }
  .flex-item {
    display: flex;
    position: relative;
    margin-top: 10px;
    margin-right: 10px;
	width: 20%
  }
   a.button-tile {
    background: #e6f2ff;
    padding: 15px;
    width: 85vw;
    min-height: 97px;
    max-height: 250px;
    text-align: center;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 4px 6px 0 hsla(0, 0%, 0%, 0.2);
  }
  a.button-tile:hover {
    background: #7aa9d391;
  } 
</style>
<div class="flex-container">
'''

'''
        <div class="flex-item">
          <a href="/disease/21-hydroxylase-deficiency/about/" class="button-tile">
            <h3 class="dark-title">About</h3>
            <p class="dark-text">Description and symptoms</p>
          </a>
        </div>
        <div class="flex-item">
          <a href="/disease/21-hydroxylase-deficiency/communities/" class="button-tile">
            <h3 class="dark-title">Communities</h3>
            <p class="dark-text">Support groups for 21-Hydroxylase Deficiency</p>
          </a>
        </div>
        <div class="flex-item">
          <a href="/disease/21-hydroxylase-deficiency/provider/" class="button-tile">
            <h3 class="dark-title">Providers</h3>
            <p class="dark-text">Healthcare providers in the area</p>
          </a>
        </div>

        <div class="flex-item">
          <a href="/disease/21-hydroxylase-deficiency/research/" class="button-tile">
            <h3 class="dark-title">Research</h3>
            <p class="dark-text">Various sources of research on 21-Hydroxylase Deficiency</p>
          </a>
        </div>
        <div class="flex-item">
          <a href="/disease/21-hydroxylase-deficiency/resources/" class="button-tile">
            <h3 class="dark-title">Financial Resources</h3>
            <p class="dark-text">Information about disability benefits from the Social Security Administration</p>
          </a>
        </div>
    </div>
'''
import csv

human_proteins = set()
corona_proteins = set()
prot_names = {}

with open("data/human_proteins.tsv") as f:
  next(f)
  for line in f:
    prot_idx = line.split('\t')[0]
    human_proteins.add(prot_idx)
    prot_name = line.split('\t')[3].split('(')[0]
    prot_names[prot_idx] = prot_name
with open("data/corona_virus_proteins.tsv") as f:
  next(f)
  for line in f:
    prot_idx = line.split('\t')[0]
    corona_proteins.add(prot_idx)
    prot_name = line.split('\t')[3].split('(')[0]
    prot_names[prot_idx] = prot_name

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

def buildFlex(k,targs):
    html = '''        <div class="flex-item">
          <a href="%s" class="button-tile">
            <h3 class="dark-title">%s</h3>
            <h4>%s</h4>
            <p class="dark-text">%d drugs found in our database.</p>
          </a>
        </div>
'''
    link = "https://coke.mml.unc.edu/static/dtd_table_json.html#%s" % k
    html = html % (link, k,prot_names[k],len(targs[k]))
    return html
for k in keys:
  x = buildFlex(k,targs)
  html += x
html += "    </div>"
with open("better_ui.html",'w') as f: f.write(html)
