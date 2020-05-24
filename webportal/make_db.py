
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

cur.execute("DROP TABLE sentences") 
cur.execute("DROP TYPE paper_loc")
cur.execute("DROP TABLE terms") 
cur.execute("CREATE TABLE terms ( term_name varchar (61) PRIMARY KEY, tag varchar(10), key varchar(50), link text)")
#cur.execute("CREATE TABLE terms ( term_name varchar(61) PRIMARY KEY, tag varchar(10), key varchar(50), link text) ON CONFLICT DO NOTHING")
cur.execute("CREATE TYPE paper_loc AS ENUM ('abstract', 'body','title')")

#cur.execute("CREATE TABLE sentences ( paper_idx varchar(50) , location paper_loc, para_num integer,  sent_num integer, sent_start integer, sent_end integer, term1 varchar(61) REFERENCES terms(term_name), term2 varchar(61) REFERENCES terms(term_name))")
cur.execute("CREATE TABLE sentences ( paper_idx varchar(50) , location paper_loc, para_num integer,  sent_num integer, sent_start integer, sent_end integer, terms varchar(61)[])")
cur.execute("ALTER TABLE sentences ADD CONSTRAINT no_dups UNIQUE ( paper_idx, location, para_num,  sent_num)")
#ALTER TABLE example ADD CONSTRAINT constraintname UNIQUE (first, second, third, fourth, fifth);
conn.commit()
conn.close()
