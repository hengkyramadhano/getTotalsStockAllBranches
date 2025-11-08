import requests
import json
import math
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
      for stockItem in range(6):  # Jumlah dari berapa banyak cabang yang di ambil
        nm_lokasi = json_response["data"]["getCheckoutOptions"]["online"]["stores"][stockItem]["name"]
        skuId = json_response["data"]["getCheckoutOptions"]["online"]["stores"][stockItem]["options"][0]["skuList"][item]["id"]
        stock = json_response["data"]["getCheckoutOptions"]["online"]["stores"][stockItem]["options"][0]["skuList"][item]["stockValue"]
        price = json_response["data"]["getCheckoutOptions"]["online"]["stores"][stockItem]["options"][0]["skuList"][item]["price"]
      
        if stock == 999999:
           stock = 100
        
        sku_detail = {"SKU" : skuId}
        price_final = {"Price" : hitung_harga(price)}
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

def hitung_harga(B2):
    # Menghitung D2 berdasarkan skema harga
    if B2 < 5000:
        D2 = B2 + 3800
    elif B2 < 10000:
        D2 = B2 + 6500
    elif B2 < 20000:
        D2 = B2 + 2000 + (B2 * 0.52)
    elif B2 < 35000:
        D2 = B2 + (B2 * 0.50)
    elif B2 < 50000:
        D2 = B2 + (B2 * 0.43)
    elif B2 < 70000:
        D2 = B2 + (B2 * 0.37)
    elif B2 < 100000:
        D2 = B2 + (B2 * 0.28)
    elif B2 < 150000:
        D2 = B2 + (B2 * 0.25)
    elif B2 < 200000:
        D2 = B2 + (B2 * 0.20)
    elif B2 < 250000:
        D2 = B2 + (B2 * 0.20)
    elif B2 < 300000:
        D2 = B2 + (B2 * 0.20)
    elif B2 < 500000:
        D2 = B2 + (B2 * 0.20)
    else:
        D2 = B2  # Jika lebih dari 500000, tidak ada tambahan dalam rumus

    # Menghitung E2
    E2 = D2 * 0.14 + D2 + 1400

    # Menghitung F2 dengan ROUNDUP ke ratusan terdekat
    F2 = math.ceil(E2 / 100) * 100

    return F2

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
            