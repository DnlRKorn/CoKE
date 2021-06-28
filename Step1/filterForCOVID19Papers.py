import os

data_dir = os.path.join(os.path.dirname(os.getcwd()),"data")
covid_papers = set()
total_papers = set()
test = {}
#with open("../
with open(os.path.join(data_dir,"cv19_scc.tsv"),'r') as f:
    next(f) #Ignore header file.
    for line in f:
        fields = line.split('\t')
        doc_id = fields[0]
        tags = fields[3]
        total_papers.add(doc_id)
        if(doc_id in covid_papers):continue
        for tag in tags.split("|"):
            (key,value)=tag.split("#")
            if("SARSCOV#NCBITaxon" in tag): 
                covid_papers.add(doc_id)
            elif("INDICATION#" in tag):
                if(value in ["D018352","D045473","D045169"]):
                    covid_papers.add(doc_id)
                    s = test.get(tag,set())
                    s.add(doc_id)
                    test[tag] = s
            elif("SPECIES#" in tag):
                if(value in ["D045473","D017934"]):
                    covid_papers.add(doc_id)
                    s = test.get(tag,set())
                    s.add(doc_id)
                    test[tag] = s
for x in test:
    print(x,len(test[x]))
print("We have identified %d papers in CORD19 which contain a tag related to COVID-19. Out of %d papers." % (len(covid_papers),len(total_papers) ) )

with open(os.path.join(data_dir,"filtered_papers_cnt.txt"),'w') as f:
    f.write(str(len(covid_papers)))


with open(os.path.join(data_dir,"cv19_scc.tsv"),'r') as f, open(os.path.join(data_dir,"cv19_scc_filtered_for_COVID.tsv"),'w') as filtered_file:
    header = next(f)
    filtered_file.write(header)
    for line in f:
        fields = line.split('\t')
        doc_id = fields[0]
        if(doc_id in covid_papers):
            filtered_file.write(line)
    
scibite_tags_cnt = 0
with open(os.path.join(data_dir,"cv19_scc.tsv"),'r') as f:
    next(f) #Ignore header file.
    for line in f:
        fields = line.split('\t')
        doc_id = fields[0]
        tags = fields[3]
        if(doc_id not in covid_papers):continue
        for tag in tags.split("|"):
            scibite_tags_cnt+=1
print("We have identified %d ontological tags from SciBite." % scibite_tags_cnt)

