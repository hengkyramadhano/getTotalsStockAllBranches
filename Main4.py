import requests
import json
import sys
import importlib
import pandas as pd
from types import SimpleNamespace
import time

with open("dataSKU.json", "r") as file:
    dataSKU = json.load(file)
        
def hit_restock(sku):
    url = "https://graphql.jakartanotebook.com/graphql/v3"

    payloadRemindMe = json.dumps([
      {
        "operationName": "AddProductSKUToRemindMe",
        "variables": {
          "requestBody": {
            "branchIds": [
              "jz23mo"
            ],
            "email": "thebestever8118@gmail.com",
            "id": sku
          }
        },
        "query": "mutation AddProductSKUToRemindMe($requestBody: ProductSkuAddProductSKUToRemindMeInput!) {\n  addProductSKUToRemindMe(requestBody: $requestBody) {\n    id\n    isWatched\n    isActive\n    stocks {\n      branchId\n      isReminded\n      __typename\n    }\n    __typename\n  }\n}"
      }
    ])

    headers = {
      'content-type': 'application/json',
      'authorization': 'Bearer eyJraWQiOiJmd0Rqb3BVUFJlbXRJb0diblhwYnRVR0ZvaVpGeEtrOFNoNVA2dXVrRTVFPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJmNzJjNDFlZi0wNDY5LTQyMzUtYWM2MS03N2RhMTBiZGYzZjkiLCJldmVudF9pZCI6IjczMjI1ZDRiLTk4ODYtNDE2Ni04MDNjLTUwNWIzOGE0MjM5MiIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4iLCJhdXRoX3RpbWUiOjE3NDYyNzM3ODYsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC5hcC1zb3V0aGVhc3QtMS5hbWF6b25hd3MuY29tXC9hcC1zb3V0aGVhc3QtMV95VmFJOHRmeXkiLCJleHAiOjE3NDk2NTg1NDcsImlhdCI6MTc0OTY1NDk0NywianRpIjoiMjFmNmM2ZWQtYTcxOC00ODQ1LThkMzMtNDViMDdjMzhmMTVjIiwiY2xpZW50X2lkIjoiNDc5amphYmNmb2NmNnZlbzRhbTNkdDRwOG0iLCJ1c2VybmFtZSI6ImY3MmM0MWVmLTA0NjktNDIzNS1hYzYxLTc3ZGExMGJkZjNmOSJ9.rTc7Nxr3LDN3nzcr3XB0dSb_5f8I_0oa6IE7uifTpiD3nM_z7k7IAJH4KbeiNGm7iepPuSHmjpOIs6sEeDDWqtSSb86uO4De2GJSbESmkLgreb_DOoDTGEvSdfpiGtGEAGAWF0bNWtBKSozOYAEUvaORRIrUQUD01HB_GzYkflNO4KezfkI0W6sBjZH9xNvbjMnYuwAVrAyxU3GuOv54s4NKklcdmNC3COVb24SY_IkNHKRaEqFcHOpezIr0TnNIms2oWAwUz4je3VZlvhNi6TqoVZ8QfRNOZX-ITKGUOOrQb1ZW6sfMTSYz90EVgunRwI8C8zWqlpDL639p8styjw'
    }

    requests.request("POST", url, headers=headers, data=payloadRemindMe)

def update_progress(progress):
    bar_length = 50
    filled_length = int(bar_length * progress)
    bar = '#' * filled_length + '-' * (bar_length - filled_length)
    sys.stdout.write(f'\rProgress: [{bar}] {int(progress * 100)}%')
    sys.stdout.flush()

jumlahSKU = len(dataSKU)

j=0
for item in dataSKU:
  skuID = item["SKU"]
  checkStock = int(item["Toko Jakarta Pusat"])

  if (checkStock == 0):
    hit_restock(skuID)

  if (j <= jumlahSKU):
     update_progress((j / jumlahSKU))
     j+=1