import json
import boto3
from PIL import Image
from urllib.parse import unquote_plus
from urllib.parse import unquote
from decimal import Decimal
import urllib.request as urlreq

s3= boto3.client('s3')
Cliente = boto3.client('rekognition','us-east-1')
dynamo = boto3.resource('dynamodb','us-east-1')
def f1(event, context):
  key = unquote_plus(event['Records'][0]['s3']['object']['key'])
  nameBucket = unquote_plus(event['Records'][0]['s3']['bucket']['name'])
  new_ubi = '/tmp/{}'.format(key)
  new_name = '{}'.format(key)
  s3.download_file("julianbucketzap1",key,new_ubi)
  tabla = dynamo.Table('imagenesExam1')
  print(nameBucket,key)
  response =Cliente.detect_labels(
      Image={
          'S3Object':{
              'Bucket':nameBucket,
              'Name': key
          }
      })
  print('hola soy response',response)
  img = Image.open(new_ubi)
  cont = 0;
  pila=[]
  pila1=[]
  h = response
  for i in range(len(h['Labels'])):
    try:
      for j in range(len(h['Labels'])):
        b_left = h['Labels'][i]['Instances'][j]['BoundingBox']['Left']
        b_top = h['Labels'][i]['Instances'][j]['BoundingBox']['Top']
        b_dere = h['Labels'][i]['Instances'][j]['BoundingBox']['Width']
        b_abajo = h['Labels'][i]['Instances'][j]['BoundingBox']['Height']
        weight=img.size[0]
        higth = img.size[1]
        left = weight * b_left
        top = higth*b_top
        dere = (weight*b_dere)
        abajo = (higth*b_abajo)
        region = (left,top,(dere+left),(abajo+top))
        imagen_rec = img.crop(region)
        ruta = "/tmp/img{}.jpg".format(cont)
        new_name_up="img_{}_{}".format(cont,new_name)
        imagen_rec.save(ruta)
        pila.append(h['Labels'][i]['Name'])
        try:
          pila1.append(h['Labels'][i]['Parents'][0]['Name'])
        except:
          pila1.append('sinsubcategoria')
        cont = cont + 1
        ubi_cat = "{}".format(pila.pop())
        ubi_scat= "{}".format(pila1.pop())
        s3.upload_file(ruta,"julianbucketzap","categoria={}/subcategoria={}/{}".format(ubi_cat,ubi_scat,new_name_up))
        final = {'categoria': ubi_cat, 'subcategoria':ubi_scat,'nombre':new_name_up, 'Ruta':"{}/categoria={}/subcategoria={}".format(nameBucket,ubi_cat,ubi_scat)}
        tabla.put_item(Item=final)
    except:
      None


