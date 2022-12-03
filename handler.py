# coding=utf-8

import boto3
import os
import uuid

dynamodb = boto3.resource("dynamodb")

def extractMetadata(event, context):
    from PIL import Image #Importação da biblioteca Pillow
    from PIL.ExifTags import TAGS #Importar a TAGS
 
    image = Image.open("img.jpg") #Abertura da imagem
   
    exifdata = image.getexif() #Extrair dos metadados exif da imagem 
       
    for tagid in exifdata: #Looping através de todas TAGS presentes no Exifdata da figura      
        tagname = TAGS.get(tagid, tagid) #Captura do nome da tag ao invés do ID do tag
        value = exifdata.get(tagid) #Passar o TAGID para pegar seu respectivo valor
       
        print(f"{tagname:25}: {value}") #Print o valor obtido

def get_dynamo_table(): #Funcao para recupera a tabela do DynamoDB através do boto3
    dynamodb = boto3.resource("dynamodb")
    table_name = os.environ['TABLE']
    return dynamodb.Table(table_name)

def create(event, context): #recebe o conteúdo que vem no body da requisição, verifica se possui dimensao e tamanho informados, então gera um id único para esse registro e o persiste na tabela.
    body = event["body"]

    if ("dimensao" in body and "tamanho" in body):
        table = get_dynamo_table()

        table.put_item(
            Item={
                "id":    str(uuid.uuid4()),
                "dimensao":  body["dimensao"],
                "tamanho": body["tamanho"],
            }
        )

        return {
            "status": 200,
            "body": "OK",
        }

    return {
        "status": 422,
        "body": "No dimensao or tamanho provided"
    }

def list(event, context): #Funcao para retornar os registros existentes
    table = get_dynamo_table()
    return table.scan()['Items']

def getMetadata(event, context):
    dynamodb = boto3.resource('dynamodb')
    tabela = dynamodb.Table('TABLE')
    resposta = tabela.get_item(
        Key={
            'dimensao': dimensao,
            'tamanho': tamanho
        }
    )
    return resposta   

def tamanho(image): #Funcao para chamada das imagens com maior e menor tamanho
    pessoas_ordenado = sorted(pessoas, key=lambda obj: obj['nome']) #Foi utilizada uma key para buscar pelo nome para permitir ser de ordem alfabetica
    print('As pessoas cadastradas em ordem alfabetica são:')
    for pessoa in pessoas_ordenado:
        print(f"- {pessoa['nome']} tem {pessoa['idade']} anos.")