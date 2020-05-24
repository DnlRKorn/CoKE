from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request
import psycopg2
import highlight
import search
app = Flask(__name__)

@app.route('/')
def hello_world():
#        return app.send_static_file('index.html')
        return app.send_static_file('better_ui.html')
        #return 'Hello, World!'

@app.route("/search")
def search_route():
   term = request.args.get('term', default = None, type = str)
   dtd = request.args.get('dtd', default = False, type = bool)
   if("chembl" in term.lower() and "DRUG#" not in term):
       idx = [x for x in list(term) if x.isdigit()]
       term = "DRUG#CHEMBL" + "".join(idx)
       

   print(term)

   if(dtd):
       l = search.dtd_search(term)
   else:
       l = search.search(term)
   l2 = []
   for (a,b,c,d) in l:
       d2 = 3
       if(d > -1e-2):
           d2 = 0
       elif(d > -10):
           d2 = 1
       elif(d > -100):
           d2 = 2
       elif(d > -1000000):
           continue
       l2.append((a,b,c,d2))
   return jsonify(l2)

@app.route("/getPapers")
def get_papers_route():
   term1 = request.args.get('term1', default = None, type = str)
   term2 = request.args.get('term2', default = None, type = str)
   #print(term)
   l = search.getPapers(term1,term2)

   return jsonify(l)


@app.route("/highlight")
def highlight_route():
   paper_idx = request.args.get('paper',  type = str)
   term1 = request.args.get('term1', default = None, type = str)
   print(term1)
   term2 = request.args.get('term2', default = None, type = str)
   terms = request.args.get('term2', default = [], type = list)
   if(term1!=None and term2!=None):
       terms = [term1,term2]
   #l = [paper_idx,term1,term2] 
  # dic = highlight.highlight_v2(paper_idx,term1,term2)
   dic = highlight.highlight_v2(paper_idx,terms)
   title=dic['title'] 
   absts=dic['abstract']
   bodys=dic['body']
   for abst in absts:
       if(abst['highlight']):
           x = abst['highlight_zone']
           x.sort()
           l = []
           idx = 0
           for (start,end) in x:
               l.append((abst['text'][idx:start],False))
               l.append((abst['text'][start:end],True))
               idx = end

           l.append((abst['text'][idx:],False))
           abst['text']= l 
   #for abst in bodys:
   for i in range(len(bodys)):
       abst=bodys[i]
       if(abst['highlight']):
           x = abst['highlight_zone']
           x.sort()
           l = []
           idx = 0
           for (start,end) in x:
               l.append((abst['text'][idx:start],False))
               l.append((abst['text'][start:end],True))
               idx = end

           l.append((abst['text'][idx:],False))
           #abst['text']= l 
           abst['text'] = l
           bodys[i] = abst
           print(abst)
           #print(abst['text'])



   return render_template('highlight.html', title=dic['title'], absts=dic['abstract'],bodys=dic['body'])
   #return jsonify(dic)



