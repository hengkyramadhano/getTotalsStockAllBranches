import requests
import json
import sys
import pandas as pd
from types import SimpleNamespace
from variables import mylist

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

SKU_Store = []

try :
    print(f"Isi dari param ke-1: {sys.argv[1]}")
    for sku_item in range(1 , len(sys.argv)):
        sku_terminal = sys.argv[sku_item]

        data = hit_api(sku_terminal)
        SKU_Store.append(data)
        print(json.dumps(data, indent=4))

except IndexError as e:
    print(f"Data sku di ambil dari Variables.py {e}")

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
            
    # export to excel
    df = pd.DataFrame(SKU_Store)
    df.to_excel(f'stock.xlsx', index=False)
