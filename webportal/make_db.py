import psycopg2
import os

db_pass = os.environ["DB_PASS"]

conn = psycopg2.connect("dbname='highlight' user='dbuser' host='localhost' password='%s'"%db_pass)

cur = conn.cursor()

#cur.execute("DROP TABLE papers")
#cur.execute("DROP TABLE sentences") 
#cur.execute("DROP TYPE paper_loc")
#cur.execute("DROP TABLE terms") 

cur.execute("CREATE TABLE terms ( term_name varchar (61) PRIMARY KEY, tag varchar(10), key varchar(50), link text)")
cur.execute("CREATE TYPE paper_loc AS ENUM ('abstract', 'body','title')")

cur.execute("CREATE TABLE papers ( paper_idx varchar(50) PRIMARY KEY , source_x text, title text, doi text, license text, publish_time text, authors text, journal text)")

cur.execute("CREATE TABLE sentences (  paper_idx varchar(50), location paper_loc, para_num integer, sent_num integer, sent_start integer, sent_end integer, terms varchar(61)[], FOREIGN KEY (paper_idx) REFERENCES papers (paper_idx))")
cur.execute("ALTER TABLE sentences ADD CONSTRAINT no_dups UNIQUE ( paper_idx, location, para_num,  sent_num)")


conn.commit()
conn.close()
