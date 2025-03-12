import requests
import json
import sys
import importlib
import pandas as pd
from types import SimpleNamespace
import time

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

if len(sys.argv) > 1:
    file_name = sys.argv[1]
    module = importlib.import_module(file_name)
    mylist = getattr(module, 'mylist')
    jumlahSKU = len(mylist)

    j=0
    for i in mylist:
        hit_restock(i)
        if (j <= jumlahSKU):
          update_progress((j / jumlahSKU))
          j+=1

else:
    print("Tidak ada argumen yang diberikan")