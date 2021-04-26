import json
import boto3
import re
from io import StringIO
from datetime import datetime, timedelta
import requests
import pandas as pd
import urllib.request
import time
from bs4 import BeautifulSoup
import ast
meses=['enero','febrero','marzo','abril']
per=['eltiempo.txt','elespectador.txt']
s3 = boto3.client('s3')
for i in per:
  new_name1 = i.split('.')[0]
  new_ubi = '/tmp/{}.csv'.format(new_name1)
  ahora = datetime.now()
  s3.download_file("julianbucket333",i,new_ubi)
  df = pd.read_csv(new_ubi, sep='\001')
 
  for i in range(len(df['enlace'])):
    url = df['enlace'][i]
    namenot = df['titular'][i]
    try:
      r = requests.get(url)
      doc = open("/tmp/doc.txt","w")
      doc.write(r.text)
      doc.close()
      s3.upload_file("/tmp/doc.txt","julianbucket333","news/raw/periodico={}/year={}/month={}/day={}/{}.html".format(new_name1,ahora.year,meses[ahora.month-1],ahora.day,namenot))
      
    except:
      None
