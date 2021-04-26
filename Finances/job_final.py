import boto3
import requests
import urllib.request
from bs4 import BeautifulSoup
import re
import ast
from datetime import datetime
pila=[]
meses = ['enero','febrero','marzo','abril','mayo']
s3 = boto3.client('s3')
ahora = datetime.now()
key1 = 'eltiempo.txt'
key2 = 'elespectador.txt'
new_ubi = '/tmp/{}'.format(key1)
new_ubi2 = '/tmp/{}'.format(key2)
s3.download_file("julianbuckethead","news/raw/{}".format(key1),new_ubi)
if (key1=="eltiempo.txt"):
  y = []
  doc = open(new_ubi,'r')
  soup = BeautifulSoup(doc, 'lxml')
  line1 = open(new_ubi,"w")
  line1csv = open("/tmp/doc1sv.txt","w")
  div_main = soup.find_all("h3", {"class":"title-container"})
  cont = 0
  line1.write("categoria"+"\001"+"titular"+"\001"+"enlace"+"\n")
  for i in div_main:
    k = (i).a
    tag=k.next.next.next.next.next
    #k = str(i)
    cont +=1
    #tag = BeautifulSoup(k, 'html.parser').a
    try:
      h = tag['href']
      category = h.split('/')[1]
      content = tag.text   
      if(h and category and content !=None):
        url = ('https://www.eltiempo.com'+h)
        line1.write(category+"\001"+content+"\001"+url+"\n")
        line1csv.write(category+"\001"+content+"\001"+url+"\n")
    except:
      print("")
  doc.close()
  line1.close()
  line1csv.close()
  s3.upload_file("/tmp/doc1sv.txt","julianbuckethead","headlines/final/periodico=eltiempo/year={}/month={}/day={}/eltiempo.csv".format(ahora.year,meses[ahora.month-1],ahora.day))
  s3.upload_file(new_ubi,"julianbucket333","eltiempo.txt")
s3.download_file("julianbuckethead","news/raw/{}".format(key2),new_ubi2)
if (key2=="elespectador.txt"):
  pila1=[]
  y1 = []
  dicc={}
  doc1 = open(new_ubi2,'r')
  soup = BeautifulSoup(doc1, 'lxml')
  line = open("/tmp/doc.txt","w")
  linecsv = open("/tmp/docsv.txt","w")
  div_main1 = soup.find_all("script", {"type":"application/ld+json"})
  print(div_main1[2])
  line.write("categoria"+"\001"+"titular"+"\001"+"enlace"+"\n")
  for i in div_main1:
   
    try:
      print(i,'esto es i')
      k = i.next
      print(k)
      dicc.update(ast.literal_eval(k.replace('""',"'")))
      y1.append(dicc)
      for i in y1:
        enl = i['mainEntityOfPage']['@id']
        cat = i['articleSection']
        tit = i['headline']
        line.write(cat+"\001"+tit+"\001"+enl+"\n")
        linecsv.write(cat+"\001"+tit+"\001"+enl+"\n")
      y1.pop()
    except:
      None
  doc1.close()     
  line.close()
  linecsv.close()
  s3.upload_file("/tmp/docsv.txt","julianbuckethead","headlines/final/periodico=elespectador/year={}/month={}/day={}/elespectador.csv".format(ahora.year,meses[ahora.month-1],ahora.day))
  s3.upload_file("/tmp/doc.txt","julianbucket333","elespectador.txt")
  line.close()
