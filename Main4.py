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
      'content-type': 'application/json'
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