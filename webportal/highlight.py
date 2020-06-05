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
   if(pap_idx not in papers_dic): return False
   terms = set(terms)
   conn = psycopg2.connect("dbname='covid_text' user='dbuser' host='localhost' password='dbpass'")
   cur = conn.cursor()
   query = '''
      SELECT
      s.location,
      s.para_num,
      s.sent_start,
      s.sent_end,
      s.terms,
      p.journal,
      p.license

    FROM
      sentence as s,
      papers as p
    WHERE
      paper_idx= %(term)s 
      '''
      #count DESC''':wq

   cur.execute(query,{"term":pap_idx})
   rows = cur.fetchall()
   abst_terms = set()
   body_dic = {}
   for row in rows:
       if(row[0]=='abstract'):
           for term in row[4]:
               abst_terms.add(term)
       if(row[0]=='body'):
           l = body_dic.get(row[1],[])
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


       for x in data.get('abstract',[]):
          d = {}
          d['text']=x['text']
          d['highlight']=False
          if(highlight_abst):
              d['highlight_zone'] = [[0,len(x['text'])]] 
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

    #tree = pET.parse(path)
    #root = tree.getroot()
   #print(dic,'hi')
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
