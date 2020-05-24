
#PMC3320336.xml	body_2_2	US|https://id.nlm.nih.gov/mesh/D006678|https://id.nlm.nih.gov/mesh/D015658	COUNTRY#US|SPECIES#D006678|INDICATION#D015658	308-489
import psycopg2
'''
try:
   conn = psycopg2.connect("dbname='covid-text' user='postgres' host='localhost'")
except:
   print "I am unable to connect to the database"
   '''


conn = psycopg2.connect("dbname='covid_text' user='dbuser' host='localhost' password='dbpass'")
cur = conn.cursor()

term_and_link = set()
fname = "/home/dkorn_unc_edu/CORD19/sentence-co-occurrence-CORD-19/1.2/cv19_scc.tsv"
with open(fname) as f:
    next(f)
    for line in f:
        l = line.split('\t')
        #l[0] paperid
        #l[1] body/abstract_PARA_SENT
        #l[2] LINKS.split("|")
        #l[3] Terms.split("|")
        terms = l[3].strip().split("|")
        urls = l[2].split("|")
        if(len(terms)!=len(urls)):
            print(line)
            print("BAD")
            exit()
        for i in range(len(terms)):
            term_and_link.add((terms[i],urls[i]))

#PMC3320336.xml	body_2_2	US|https://id.nlm.nih.gov/mesh/D006678|https://id.nlm.nih.gov/mesh/D015658	COUNTRY#US|SPECIES#D006678|INDICATION#D015658	308-489
import psycopg2
'''
try:
   conn = psycopg2.connect("dbname='covid-text' user='postgres' host='localhost'")
except:
   print "I am unable to connect to the database"
   '''


conn = psycopg2.connect("dbname='covid_text' user='dbuser' host='localhost' password='dbpass'")
cur = conn.cursor()

#cur.execute("CREATE TABLE term ( term_name character(60) PRIMARY KEY, key character(10), tag character(50), link text)");
for (term,link) in term_and_link:
    (tag,key) = term.split("#")

    cur.execute("INSERT INTO terms (term_name, tag,key, link) VALUES(%s, %s, %s, %s) ", (term,tag,key,link))
    #cursor.execute("INSERT INTO terms (term_name, key, tag, link) VALUES(%s, %s, %s, %s) ON CONFLICT DO NOTHING", (prot,chem,overlap,score,papers))

conn.commit()
conn.close()
