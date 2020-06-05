from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request
import psycopg2
import highlight
app = Flask(__name__)


@app.route("/highlight")
def highlight_route():
   paper_idx = request.args.get('paper',  type = str)
   term1 = request.args.get('term1', default = None, type = str)
   term2 = request.args.get('term2', default = None, type = str)
   terms = request.args.get('terms', default = [], type = list)
   if(term1!=None and term2!=None):
       terms = [term1,term2]

   dic = highlight.highlight_v2(paper_idx,terms)
   if(type(dic)==str):
       if(dic=='unk'):
           return "<p>This paper has an unknown license situation and therefore we cannot show full text of it.</p>"
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
               #Go through every 
               l.append((abst['text'][idx:start],False))
               l.append((abst['text'][start:end],True))
               idx = end

           l.append((abst['text'][idx:],False))
           abst['text']= l 
   #for abst in bodys:
   if(bodys=="unk"):
       bodys = {'text':'This paper has no documented license provided by CORD-19 metadata, and therefore we cannot show the body. Please seek it out from <a href="https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge">https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge</a> for more information.',"highlight":False}
    
   for i in range(len(bodys)):
       paragraph=bodys[i]
       if(paragraph['highlight']):
           x = paragraph['highlight_zone']
           x.sort()
           l = []
           idx = 0
           for (start,end) in x:
               l.append((paragraph['text'][idx:start],False))
               l.append((paragraph['text'][start:end],True))
               idx = end

           l.append((paragraph['text'][idx:],False))
           #abst['text']= l 
           paragraph['text'] = l
           bodys[i] = paragraph
           print(paragraph)



   return render_template('highlight.html', title=dic['title'], absts=dic['abstract'],bodys=dic['body'],journal=dic['journal'], doi=dic['doi'])

