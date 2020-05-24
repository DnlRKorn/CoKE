
#PMC3320336.xml	body_2_2	US|https://id.nlm.nih.gov/mesh/D006678|https://id.nlm.nih.gov/mesh/D015658	COUNTRY#US|SPECIES#D006678|INDICATION#D015658	308-489
import psycopg2
from psycopg2.extras import execute_values
'''
try:
   conn = psycopg2.connect("dbname='covid-text' user='postgres' host='localhost'")
except:
   print "I am unable to connect to the database"
   '''


conn = psycopg2.connect("dbname='covid_text' user='dbuser' host='localhost' password='dbpass'")
cur = conn.cursor()

sents = []
fname = "/home/dkorn_unc_edu/CORD19/sentence-co-occurrence-CORD-19/1.2/cv19_scc.tsv"
insert_query = "INSERT INTO sentences (paper_idx, location, para_num, sent_num, sent_start, sent_end, terms) VALUES %s"
cnt=-1
with open(fname) as f:
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
#for (paper_idx,loc,para_num,sent_num,start,end,t1,t2) in sents:
#    cur.execute("INSERT INTO sentences (paper_idx, location, para_num, sent_num, sent_start, sent_end, term1, term2) VALUES(%s, %s, %s, %s, %s, %s, %s, %s) ", (paper_idx,loc,para_num,sent_num,start,end,t1.strip(),t2.strip()))

#conn = psycopg2.connect("dbname='covid_text' user='dbuser' host='localhost' password='dbpass'")
#cur = conn.cursor()

#cur.execute("CREATE TABLE term ( term_name character(60) PRIMARY KEY, key character(10), tag character(50), link text)");

#    cur.execute("INSERT INTO terms (term_name, tag,key, link) VALUES(%s, %s, %s, %s) ", (term,tag,key,link))
    #cursor.execute("INSERT INTO terms (term_name, key, tag, link) VALUES(%s, %s, %s, %s) ON CONFLICT DO NOTHING", (prot,chem,overlap,score,papers))
conn.commit()

conn.close()
