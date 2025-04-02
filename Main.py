import requests
import json
import sys
import importlib
import pandas as pd
from variables import mylist
import time

def hit_api(sku) :

    url = "https://graphql.jakartanotebook.com/graphql/v3"

    payload = json.dumps({
      "operationName": "AllCheckoutOptions",
      "variables": {
        "input": {
          "items": [{"id": jejak, "quantity": 1} for jejak in sku[:100]]
        }
      },
      "query": "mutation AllCheckoutOptions($input: CheckoutRequestInput!) {\n  getCheckoutOptions(requestBody: $input) {\n    online {\n      text\n      stores {\n        ...storesInfo\n        __typename\n      }\n      type\n      __typename\n    }\n    }\n}\n\nfragment storesInfo on CheckoutStore {\n  name\n  options {\n    skuList {\n      id\n            stockValue\n      price\n      subtotal\n     }\n   }\n  }"
    })

    # payloadRemindMe = json.dumps([
    #   {
    #     "operationName": "AddProductSKUToRemindMe",
    #     "variables": {
    #       "requestBody": {
    #         "branchIds": [
    #           "jz23mo"
    #         ],
    #         "email": "hengkyramadhano@gmail.com",
    #         "id": sku
    #       }
    #     },
    #     "query": "mutation AddProductSKUToRemindMe($requestBody: ProductSkuAddProductSKUToRemindMeInput!) {\n  addProductSKUToRemindMe(requestBody: $requestBody) {\n    id\n    isWatched\n    isActive\n    stocks {\n      branchId\n      isReminded\n      __typename\n    }\n    __typename\n  }\n}"
    #   }
    # ])
    headers = {
      'content-type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    json_response = json.loads(response.text)

    jumlah_data = len(json_response["data"]["getCheckoutOptions"]["online"]["stores"][0]["options"][0]["skuList"])
   
    data_list = []
    for item in range(jumlah_data):
      data_row = {}
      for stockItem in range(6):
        nm_lokasi = json_response["data"]["getCheckoutOptions"]["online"]["stores"][stockItem]["name"]
        skuId = json_response["data"]["getCheckoutOptions"]["online"]["stores"][stockItem]["options"][0]["skuList"][item]["id"]
        stock = json_response["data"]["getCheckoutOptions"]["online"]["stores"][stockItem]["options"][0]["skuList"][item]["stockValue"]
        price = json_response["data"]["getCheckoutOptions"]["online"]["stores"][stockItem]["options"][0]["skuList"][item]["price"]
      
        sku_detail = {"SKU" : skuId}
        price_final = {"Price" : price}
        product_name_dict = {nm_lokasi : stock}
        data_row.update(sku_detail)
        data_row.update(price_final)
        data_row.update(product_name_dict)
        
      data_list.append(data_row)
      # if((nm_lokasi == 'Toko Jakarta Pusat') & (stock == 0)):
      #   requests.request("POST", url, headers=headers, data=payloadRemindMe)
        

    return data_list

def update_progress(progress):
    bar_length = 50
    filled_length = int(bar_length * progress)
    bar = '#' * filled_length + '-' * (bar_length - filled_length)
    sys.stdout.write(f'\rProgress: [{bar}] {int(progress * 100)}%')
    sys.stdout.flush()

# export to excel
def export_to_excel():
  with open("dataSKU.json", "w") as fp:
        json.dump(SKU_Store, fp)

  df = pd.DataFrame(SKU_Store)
  curr_time = time.strftime("%H_%M_%S", time.localtime())
  df.to_excel(f'{file_name}-{curr_time}.xlsx', index=False)

def split_list(lst, chunk_size=100):
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

SKU_Store = []

file_name = ""

if len(sys.argv) > 1:  # Memastikan ada argumen yang diberikan
  if sys.argv[1] not in ("tiktok", "netlook", "shopee", "tourisme", "bestever", "sample"): # Nama file sku
    print("Load Data SKU..")
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

    batches = split_list(mylist, 100)
    print(f"Total SKU: {len(mylist)}")
    jumlahSKU = len(batches)
    
    i = 1
    for j in range(jumlahSKU):
      try:
        data = hit_api(batches[j])
        SKU_Store.extend(data)
        if (i <= jumlahSKU):
          update_progress((i / jumlahSKU))
          i+=1
      except Exception as e:
        print(f"Error for sku : {e}")
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
            