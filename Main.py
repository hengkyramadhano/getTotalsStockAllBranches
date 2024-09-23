import requests
import json
import sys
import importlib
import pandas as pd
from types import SimpleNamespace
from variables import mylist
import time

def hit_api(sku) :

    url = "https://graphql.jakartanotebook.com/graphql/v3"

    payload = json.dumps({
      "operationName": "AllCheckoutOptions",
      "variables": {
        "input": {
          "items": [
            {
              "id": sku,
              "quantity": 1
            }
          ]
        }
      },
      "query": "mutation AllCheckoutOptions($input: CheckoutRequestInput!) {\n  getCheckoutOptions(requestBody: $input) {\n    online {\n      text\n      stores {\n        ...storesInfo\n        __typename\n      }\n      type\n      __typename\n    }\n    pickup {\n      text\n      stores {\n        ...storesInfo\n        __typename\n      }\n      type\n      __typename\n    }\n    cod {\n      text\n      isEnabled\n      disabledText\n      fees {\n        weight {\n          min\n          max\n          __typename\n        }\n        isSelected\n        fee\n        __typename\n      }\n      stores {\n        ...storesInfo\n        __typename\n      }\n      type\n      __typename\n    }\n    announcements\n    __typename\n  }\n}\n\nfragment storesInfo on CheckoutStore {\n  name\n  options {\n    skuList {\n      stockValue\n    }\n   }\n }"
    })
    headers = {
      'content-type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    json_response = json.loads(response.text, object_hook=lambda d: SimpleNamespace(**d))

    # pretty_json_response = json.dumps(json_response, indent=4)
    # print(pretty_json_response)

    data_row = {}
    for item in range(6):
        nm_lokasi = json_response.data.getCheckoutOptions.online.stores[item].name
        stock = json_response.data.getCheckoutOptions.online.stores[item].options[0].skuList[0].stockValue
        # print(f"{nm_lokasi} = {stock}")
        sku_detail = {"SKU" : sku}
        product_name_dict = {nm_lokasi : stock}

        data_row.update(sku_detail)
        data_row.update(product_name_dict)

    return data_row

def update_progress(progress):
    bar_length = 50
    filled_length = int(bar_length * progress)
    bar = '#' * filled_length + '-' * (bar_length - filled_length)
    sys.stdout.write(f'\rProgress: [{bar}] {int(progress * 100)}%')
    sys.stdout.flush()

# export to excel
def export_to_excel():
  df = pd.DataFrame(SKU_Store)
  curr_time = time.strftime("%H_%M_%S", time.localtime())
  df.to_excel(f'{file_name}-{curr_time}.xlsx', index=False)

SKU_Store = []

file_name = ""

if len(sys.argv) > 1:  # Memastikan ada argumen yang diberikan
  if sys.argv[1] not in ("tiktok", "netlook", "shopee", "tourisme"): # Nama file sku
      print("Argumen tidak valid")
      for sku_item in range(1 , len(sys.argv)):
        sku_terminal = sys.argv[sku_item]
        
        data = hit_api(sku_terminal)
        # SKU_Store.append(data)
        print(json.dumps(data, indent=4))
  else:
    print("Masuk ke import file")
    
    file_name = sys.argv[1]
    module = importlib.import_module(file_name)
    mylist = getattr(module, 'mylist')
    
    jumlahSKU = len(mylist)
    print(f"Total SKU: {jumlahSKU}")
    i = 1
    for sku in mylist:
      try:
        data = hit_api(sku)
        SKU_Store.append(data)
        if (i <= jumlahSKU):
          update_progress((i / jumlahSKU))
          i+=1
      except Exception as e:
        print(f"Error for sku {sku}: {e}")
    export_to_excel()
else:
  print("Tidak ada argumen yang diberikan")
  jumlahSKU = len(mylist)
  print(f"Total SKU: {jumlahSKU}")
  i = 1
  for sku in mylist:
    try:
      data = hit_api(sku)
      SKU_Store.append(data)
      if (i <= jumlahSKU):
        update_progress((i / jumlahSKU))
        i+=1
    except Exception as e:
      print(f"Error for sku {sku}: {e}")
  export_to_excel()
            