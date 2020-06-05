import psycopg2
from psycopg2.extras import execute_values
import csv
import os

data_dir = os.path.join(os.path.dirname(os.getcwd()),"data")

db_pass = os.environ["DB_PASS"]

conn = psycopg2.connect("dbname='highlight' user='dbuser' host='localhost' password='%s'"%db_pass)
cur = conn.cursor()

metadata_fname = os.path.join(data_dir,"metadata.csv")
#cord_uid,sha,source_x,title,doi,pmcid,pubmed_id,license,abstract,publish_time,authors,journal,mag_id,who_covidence_id,arxiv_id,pdf_json_files,pmc_json_files,url,s2_id
#cur.execute("CREATE TABLE papers ( paper_idx varchar(50) PRIMARY KEY , source_x text, title text, doi text, license text, publish_time text, authors text, journal text)")
insert_query = "INSERT INTO papers (paper_idx, source_x, title, doi, license, publish_time, authors, journal) VALUES %s"
paps = []
seen_paps = set()
with open(metadata_fname,'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
#        paper_idx = row["cord_uid"] 
#        paper_idxs = [paper_idx]
        paper_idxs = []
        pmcid = row["pmcid"] 
        source_x  = row["source_x"] 
        title  = row["title"] 
        doi = row["doi"] 
        license = row["license"] 
        pub_time = row["publish_time"] 
        authors = row["authors"] 
        journal = row["journal"] 
        pdf_jsons = row["pdf_json_files"].split(";")
        for pdf_json in pdf_jsons:
            pdf_json = pdf_json.split('/')[-1]
            pdf_json = pdf_json.split('.')[0]
            paper_idxs.append(pdf_json)
               
        if(len(pmcid)>2):
            paper_idxs.append(pmcid + ".xml")
        for paper_idx in paper_idxs:
            if(paper_idx in seen_paps):continue
            seen_paps.add(paper_idx)
            paps.append((paper_idx ,source_x  ,  title  ,  doi ,  license ,  pub_time ,  authors ,  journal))

psycopg2.extras.execute_values( cur, insert_query, paps, template=None, page_size=1000)
conn.commit()

conn.close()
