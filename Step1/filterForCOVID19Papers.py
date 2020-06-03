import os

data_dir = os.path.join(os.path.dirname(os.getcwd()),"data")
covid_papers = set()
#with open("../
with open(os.path.join(data_dir,"cv19_scc.tsv"),'r') as f:
    next(f) #Ignore header file.
    for line in f:
        fields = line.split('\t')
        doc_id = fields[0]
        tags = fields[3]
        if(doc_id in covid_papers):continue
        for tag in tags.split("|"):
            if("SARSCOV#" in tag): covid_papers.add(doc_id)
print("We have identified %d papers in CORD19 which contain a tag related to COVID-19." % len(covid_papers))

with open(os.path.join(data_dir,"cv19_scc.tsv"),'r') as f, open(os.path.join(data_dir,"cv19_scc_filtered_for_COVID.tsv"),'w') as filtered_file:
    header = next(f)
    filtered_file.write(header)
    for line in f:
        fields = line.split('\t')
        doc_id = fields[0]
        if(doc_id in covid_papers):
            filtered_file.write(line)
    
