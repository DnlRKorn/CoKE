import csv
from itertools import combinations 


term_counts = {}
tup_counts = {}

papers = {}

def process_abstract(abstract_terms,terms,tuples):
   terms.update(abstract_terms)
   combs = combinations(abstract_terms,2)
   for comb in combs:
      if(len(comb)==1):continue
      if(comb[0] < comb[1]):tuples.add(comb)
      else:tuples.add((comb[1],comb[0]))
   return (terms, tuples)

def tuple_and_term_count(paperidx,terms,tuples):
  for term in terms:
    x = term_counts.get(term,0)
    term_counts[term] = x+1

  for tup in tuples:
    #Sanity checks on tuples. Ensure they are all have two distinct terms.
    if(len(tup)!=2): raise ValueError("Tuple not length two.",tup)
    if(tup[0]==tup[1]):raise ValueError("Tuple has two of the same element.",tup)
    x = tup_counts.get(tup,0)
    tup_counts[tup] = x+1
    s = papers.get(tup,set())
    s.add(paperidx)
    papers[tup] = s

fname="data/cv19_scc.tsv"
total_sentence_count = 0
with open(fname) as f:
  next(f) #Ignore header.
  for line in f: total_sentence_count+=1


with open(fname) as csvfile:
  reader = csv.DictReader(csvfile, delimiter='\t')
  last_doc = None

  cnt = 0
  for dic in reader:
    plus_ids = dic["entity_types_plus_ids"].split("|")
    doc_id = dic['document_id']
    sent_id = dic['sentence_id']

    if(last_doc==None):
      last_doc=doc_id
      tuples = set()
      terms = set()
      abstract_terms = set()

    #When the document changes, process the dataset. Give each paper it's vote.
    if(doc_id!=last_doc):
      (terms,tuples) = process_abstract(abstract_terms,terms,tuples)
      abstract_terms = set()
      tuple_and_term_count(last_doc,terms,tuples)
      tuples = set()
      terms = set()
      last_doc=doc_id

    if('abstract' in sent_id):
      for x in plus_ids:
         abstract_terms.add(x)
    if('body' in sent_id):
      terms.update(plus_ids)
      combs = combinations(plus_ids,2)
      for comb in combs:
         if(len(comb)!=2):continue
         if(comb[0] < comb[1]):tuples.add(comb)
         elif(comb[0]==comb[1]):continue
         else:tuples.add((comb[1],comb[0]))
    if(cnt%10000==0):
      print(cnt,cnt / total_sentence_count)
    cnt+=1

with open('CORD19_co-occurrence_pairs.csv','w') as f:
  f.write('Term1,Term2,Term1Cnt,Term2Cnt,Co-occurrenceCnt,Papers\n')
  for s in tup_counts:
    co_occur_cnt = tup_counts[s]
    k = s
    cnt1 = term_counts[k[0]]
    cnt2 = term_counts[k[1]]
    paps = papers[s]
    paps = list(paps)
    paps.sort()
    
    f.write(k[0]+','+k[1]+','+str(cnt1)+","+str(cnt2)+","  +str(co_occur_cnt)+ ',' + ','.join(paps) + '\n')

