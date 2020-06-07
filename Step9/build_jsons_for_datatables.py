import csv
import json
import os

data_dir = os.path.join(os.path.dirname(os.getcwd()),"data")

def convertDict(d):
    d2 = {}
    targ = d["Target"]
    drug = d["ChEMBL ID"]

    d2["Target"] = '<a href="https://www.uniprot.org/uniprot/%s">%s</a>' % (targ,targ)
    d_b = d["DrugBank ID"]
    d2["DrugBank ID"] = '<a href="https://www.drugbank.ca/drugs/%s">%s</a>' % (d_b,d_b)
    d2["ChEMBL ID"] = '<a href="https://www.ebi.ac.uk/chembl/compound_report_card/%s">%s</a>' % (d["ChEMBL ID"],d["ChEMBL ID"])
    d2["SMILES"] = d["SMILES"]
    d2["Name"] = d["Name"]
    d2["Other Targets"] = '<a href="https://www.drugbank.ca/drugs/%s#targets">%s</a>' % (d_b,d["Other Targets"])

    li_txt = '<div style="height:100px; overflow-y:scroll;">'
    for paper in d["Papers"].split("|"):
        link = "http://coke.mml.unc.edu/highlight?paper=%s&term1=CVPROT%%23%s&term2=DRUG%%23%s" % (paper.strip().replace('"',""),targ,drug)
        li_txt+='<a href="%s">%s</a></br></br>' %(link,paper.strip().replace('"',''))

    li_txt += "</div>"
    d2["Paper Links"] = li_txt
    d2["Score"] = "%.2f" % float(d["Score"])
    return d2

#["Target","Name","DrugBank ID","ChEMBL ID","SMILES","Other Targets","Score","Papers"]
for csv_fname in os.listdir(os.path.join(data_dir,'csv')):
    print(csv_fname)
    json_fname = csv_fname.split(".")[0] + ".json"
    json_rows = []
    with open(os.path.join(data_dir,'csv',csv_fname),'r') as csv_file:
         reader = csv.DictReader(csv_file)
         for row in reader:
             l = []
             d = convertDict(row)
             for x in ["Target","Name","DrugBank ID","ChEMBL ID","SMILES","Other Targets","Score","Paper Links"]:
               l.append(d[x])
             json_rows.append(l)
    json_data = {"data":json_rows}
    with open(os.path.join(data_dir,'json',json_fname),'w') as f:
        json.dump(json_data,f)
