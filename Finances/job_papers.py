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
s3 = boto3.client('s3')
ahora = datetime.now()
papers = ['eltiempo','elespectador']

for i in papers:
    name = '{}_{}_{}_{}'.format(i,ahora.year,ahora.month,ahora.day)
    r = requests.get('https://www.{}.com/'.format(i))
    doc = open("/tmp/doc.txt","w")
    doc.write(r.text)
    doc.close()
    meses = ['enero','febrero','marzo','abril','mayo','junio']
    ruta = 'news/raw/periodico={}/year={}/month={}/day={}/{}.txt'.format(i,ahora.year,meses[ahora.month-1],ahora.day,name)
    s3.upload_file("/tmp/doc.txt","julianbuckethead",ruta)
    s3.upload_file("/tmp/doc.txt","julianbuckethead","news/raw/{}.txt".format(i))
