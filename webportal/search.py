import psycopg2
'''
try:
   conn = psycopg2.connect("dbname='covid-text' user='postgres' host='localhost'")
except:
   print "I am unable to connect to the database"
   '''


def search(term):
   conn = psycopg2.connect("dbname='covid_text' user='dbuser' host='localhost' password='dbpass'")
   cur = conn.cursor()
   query = '''
      SELECT
      term1,
      term2,
      count,
      score
    FROM
      overlap
    WHERE
      term1= %(term)s OR
      term2= %(term)s
    ORDER BY
      score DESC'''
      #count DESC'''

   cur.execute(query,{"term":term})
   #conn.close()
   rows = cur.fetchall()
   #print(type(rows))
   return rows

def dtd_search(term):
   conn = psycopg2.connect("dbname='covid_text' user='dbuser' host='localhost' password='dbpass'")
   cur = conn.cursor()
   query = '''
      SELECT
      term1,
      term2,
      count,
      score
    FROM
      overlap_dtd
    WHERE
      term1= %(term)s OR
      term2= %(term)s
    ORDER BY
      score DESC'''
      #count DESC'''

   cur.execute(query,{"term":term})
   #conn.close()
   rows = cur.fetchall()
   #print(type(rows))
   return rows

def getPapers(term1,term2):
   conn = psycopg2.connect("dbname='covid_text' user='dbuser' host='localhost' password='dbpass'")
   cur = conn.cursor()
   query = '''
      SELECT
      papers 
    FROM
      overlap
    WHERE
      term1= %(term1)s AND
      term2= %(term2)s
      '''

   cur.execute(query,{"term1":term1,"term2":term2})
   #conn.close()
   rows = cur.fetchall()
   l = []
   for row in rows:
       for x in row:
           for y in x:
              l.append(y)


   rows = [x.strip() for x in l]

   print(term1,term2,len(rows))
   #print(type(rows))
   return rows

#search("DRUG#CHEMBL296588")
#search("CVPROT#P0DTD1")
