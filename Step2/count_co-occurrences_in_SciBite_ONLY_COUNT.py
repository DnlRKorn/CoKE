import csv
import sys
from itertools import combinations 
import os

data_dir = os.path.join(os.path.dirname(os.getcwd()),"data")

term_counts = {}
tup_counts = {}


def process_abstract(abstract_terms):
    
    abst_tuples = set()
    combs = combinations(abstract_terms,2)
    for comb in combs:
       if(len(comb)==1):continue
       if(comb[0] < comb[1]):abst_tuples.add(comb)
       else:abst_tuples.add((comb[1],comb[0]))
    return abst_tuples


def process_paragraphs(paragraph_dic):
    paragraph_tuples = {}
    filtered_para_tuples = set()
    for i in range(7108): 
        combs = combinations(paragraph_dic[i],2)
        tuples = set()
        for comb in combs:
            if(len(comb)!=2):continue
            if(comb[0] < comb[1]):tuples.add(comb)
            elif(comb[0] > comb[1]):tuples.add((comb[1],comb[0]))
        for t in tuples:
            paragraph_tuples[t] = True
    for t in paragraph_tuples:
        if(paragraph_tuples[t]>=3):filtered_para_tuples.add(t)
    return filtered_para_tuples 


def tuple_and_term_count(paperidx,terms,tuples):
 # for term in terms:
   # term_counts[term] = True 

  for tup in tuples:
    #Sanity checks on tuples. Ensure they are all have two distinct terms.
    if(len(tup)!=2): raise ValueError("Tuple not length two.",tup)
    if(tup[0]==tup[1]):raise ValueError("Tuple has two of the same element.",tup)
    tup_counts[tup] = True 

fname = os.path.join(data_dir,"cv19_scc_filtered_for_COVID.tsv")

total_sentence_count = 0
with open(fname, 'r') as f:
  next(f) #Ignore header.
  for line in f: total_sentence_count+=1
print("We are looking at %d sentences in the filtered SciBite annotations. Tup count %d."%(total_sentence_count,len(tup_counts)))

paragraph_dic = {}
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
            for i in range(10000): paragraph_dic[i] = set()
            tuples = set()
            terms = set()
            abstract_terms = set()
    
        #When the document changes, process the dataset. Give each paper it's vote.
        if(doc_id!=last_doc):
            abst_tuples = process_abstract(abstract_terms)
#            oldest_len = len(tuples)
            tuples.update(abst_tuples)
            para_tuples = process_paragraphs(paragraph_dic)
#            abst_len = len(tuples)
            tuples.update(para_tuples)
#            if(len(abst_tuples)!=0):
#                print(len(abst_tuples),"abst tups")
#                print(doc_id,"sentence",oldest_len,"abst",abst_len,"final",len(tuples))
            tuple_and_term_count(last_doc,terms,tuples)

            tuples = set()
            terms = set()
            abstract_terms = set()
            for i in range(7108): paragraph_dic[i] = set()
            last_doc=doc_id
    
        if('abstract' in sent_id):
            for x in plus_ids:
                terms.add(x)
                abstract_terms.add(x)
        if('body' in sent_id):
            (_,para_num,_) = sent_id.split("_")
            for x in plus_ids:
                terms.add(x)
                paragraph_dic[int(para_num)].add(x)

            combs = combinations(plus_ids,2)
            for comb in combs:
                if(len(comb)!=2):continue
                if(comb[0] < comb[1]):tuples.add(comb)
                elif(comb[0] > comb[1]):tuples.add((comb[1],comb[0]))
        if(cnt%10000==0):
            sys.stderr.write("Sentences processed:%d Percent Complete: %f Tup Cnt:%d\n"%(cnt,1.0*cnt / total_sentence_count,len(tup_counts)))
        cnt+=1
    abst_tuples = process_abstract(abstract_terms)
    tuples.update(abst_tuples)
    tuple_and_term_count(last_doc,terms,tuples)

    
print("We have %d tuples after filtering for protein/drug relationships!" % len(tup_counts))
