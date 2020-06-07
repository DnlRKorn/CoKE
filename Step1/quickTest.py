import os

data_dir = os.path.join(os.path.dirname(os.getcwd()),"data")
sars_cov = {}
#with open("../
with open(os.path.join(data_dir,"cv19_scc.tsv"),'r') as f:
    next(f) #Ignore header file.
    for line in f:
        fields = line.split('\t')
        doc_id = fields[0]
        tags = fields[3]
        for tag in tags.split("|"):
            if("SARSCOV#" in tag):
                s = sars_cov.get(tag,set())
                s.add(doc_id)
                sars_cov[tag] = s

l2=[]
for x in sars_cov:
    l2.append((len(sars_cov[x]),x))
l2.sort()
for a in l2:
    print(a)
