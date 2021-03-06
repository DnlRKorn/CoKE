import os
import json
import psycopg2

papers_dic = {}  
cord_dir = "/home/dkorn_unc_edu/CORD19/annotated-CORD-19/1.4/CORD19"
for root, dirs, files in os.walk(cord_dir, topdown=False):
    for name in files:
        if(name.endswith(".json")):
            paper_idx = name.split(".json")[0]
            papers_dic[paper_idx] = os.path.join(root, name)


def highlight_v2(pap_idx,terms):
   if(pap_idx not in papers_dic): return 'No find' 
   terms = set(terms)
   db_pass = os.environ["DB_PASS"]

   conn = psycopg2.connect("dbname='highlight' user='dbuser' host='localhost' password='%s'"%db_pass)
   cur = conn.cursor()
   query = '''
      SELECT
      sentences.location,
      sentences.para_num,
      sentences.sent_start,
      sentences.sent_end,
      sentences.terms,
      papers.journal,
      papers.license,
      papers.doi,
      papers.source_x
    FROM
      sentences
    LEFT JOIN papers 
    ON papers.paper_idx=sentences.paper_idx
    WHERE
      sentences.paper_idx= %(pap_idx)s 
      '''
   cur.execute(query,{"pap_idx":pap_idx})
   rows = cur.fetchall()
   abst_terms = set()
   abst_dic = {}
   body_dic = {}
   
   for row in rows:
       journal = row[5]
       source_x = row[8]
       doi = row[7]
       license = row[6]
       if(row[0]=='abstract'):
           l = abst_dic.get(row[1],[])

           #Sentence_start, Sentence_end, Terms
           l.append((row[2],row[3],row[4]))
           abst_dic[row[1]] = l
           for term in row[4]:
               abst_terms.add(term)
       if(row[0]=='body'):

           #Get the list of terms found in this sentence.
           l = body_dic.get(row[1],[])

           #Sentence_start, Sentence_end, Terms
           l.append((row[2],row[3],row[4]))
           body_dic[row[1]] = l
   highlight_abst = False
   if( len(terms)== len(terms.intersection(abst_terms)) ):
        highlight_abst=True


#   path = '/home/dkorn_unc_edu/CORD19/data/%s.json'%pap_idx
   path = papers_dic[pap_idx]
   print(terms)
   with open(path) as f:
       data = json.load(f)
       dic = {}
       title = data['metadata']['title']
       dic["title"] = title
       abst = []


       para_cnt = 0
       for x in data.get('abstract',[]):
          l = abst_dic.get(para_cnt,[])
          para_cnt+=1
          highlight_zone = []
          for (sent_start,sent_end,sent_terms) in l:
             if( len(terms.intersection(set(sent_terms))) > 0 ):
                 highlight_zone.append((sent_start,sent_end))

          d = {}
          d['text']=x['text']
          d['highlight']=False
          if(len(highlight_zone)!=0):
              d['highlight_zone'] = highlight_zone
              d['highlight']=True
          abst.append(d)
              
       dic['abstract'] = abst
       body = []
       para_cnt = 0
       for x in data['body_text']:
          l = body_dic.get(para_cnt,[])
          para_cnt+=1
          highlight_zone = []
          for (sent_start,sent_end,sent_terms) in l:

             if( len(terms)== len(terms.intersection(set(sent_terms))) ):
                 highlight_zone.append((sent_start,sent_end))

          d = {}
          d['text']=x['text']
          d['highlight']=False
          if(len(highlight_zone)!=0):
              d['highlight_zone'] = highlight_zone
              d['highlight']=True
          body.append(d)
       dic['body'] = body

   dic['journal'] = journal
   dic['doi'] = doi
   if((license=='unk') & ("PMC" not in source_x)):
       dic['body'] = 'unk' 
   return dic 


   #print(type(rows))
if(__name__=="__main__"):
    print("HI")
#    x = highlight("0acc1f9a1c333a9a6b2dbba4a252d7576f024783","CVPROT#P0DTD1","DRUG#CHEMBL296588")
    x = highlight_v2("453985e02d2419abce4d5626b093a888187cfc7a",["CVPROT#P0DTD1","DRUG#CHEMBL296588"])
    for a in x['body']:
        print(a['highlight'])
        if(a['highlight']):
            b = a['highlight_zone'][0]
            print(type(b))
            print(b[0])
            print(a['text'][b[0]:b[1]])
            print(b)
