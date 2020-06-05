import psycopg2
from psycopg2.extras import execute_values
import os

data_dir = os.path.join(os.path.dirname(os.getcwd()),"data")

db_pass = os.environ["DB_PASS"]

conn = psycopg2.connect("dbname='highlight' user='dbuser' host='localhost' password='%s'"%db_pass)
cur = conn.cursor()

sents = []
fname = os.path.join(data_dir,"cv19_scc.tsv")
insert_query = "INSERT INTO sentences (paper_idx, location, para_num, sent_num, sent_start, sent_end, terms) VALUES %s"
cnt=-1
with open(fname,'r') as f:
    next(f)
    print("Starting loop")
    for line in f:
        cnt+=1
        if(cnt<-1):continue
        if(cnt%10000==0):
            print(cnt)
            psycopg2.extras.execute_values( cur, insert_query, sents, template=None, page_size=100)
            sents = []
            conn.commit()
        l = line.strip().split('\t')
        #l[0] paperid
        #l[1] body/abstract_PARA_SENT
        #l[2] LINKS.split("|")
        #l[3] Terms.split("|")
        #l[4] sent_start - sent_end
        paper_idx = l[0]
        if(paper_idx=="eb5c7f3ff921ad6469b79cc8a3c122648204ece4"):continue
        if('title' in l[1]):
           (loc,sent_num) = l[1].split("_")
           para_num = 0
        else:
           (loc,para_num,sent_num) = l[1].split("_")
        para_num = int(para_num)
        sent_num = int(sent_num)
        try:
           (start,end) = l[4].split("-")
        except:
            (_,start,end) = l[4].split("-")
        start = int(start)
        end = int(end)

        terms = l[3].strip().split("|")
        terms.sort()
               
        sents.append((paper_idx,loc,para_num,sent_num,start,end,terms))
           

insert_query = "INSERT INTO sentences (paper_idx, location, para_num, sent_num, sent_start, sent_end, terms) VALUES %s"
#insert_query = "INSERT INTO sentences (paper_idx, location, para_num, sent_num, sent_start, sent_end, term1, term2) VALUES %s"
psycopg2.extras.execute_values( cur, insert_query, sents, template=None, page_size=1000)

conn.commit()

conn.close()
