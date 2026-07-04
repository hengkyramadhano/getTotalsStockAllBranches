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

    headers = {
      'content-type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    json_response = json.loads(response.text)

    urutan_toko = [
      "Gudang Online",
      "Toko Jakarta Pusat",
      "Toko Jakarta Barat",
      "Toko Jakarta Utara",
      "Toko Tangerang",
      "Toko Cikupa"
    ]

    data = json_response["data"]["getCheckoutOptions"]["online"]
    jumlah_data = len(json_response["data"]["getCheckoutOptions"]["online"]["stores"][0]["options"][0]["skuList"])

    # Buat dictionary: nama_toko -> data store
    store_map = {store["name"]: store for store in data["stores"]}
   
    data_list = []
    for item in range(jumlah_data):
      data_row = {}

      for nm_toko in urutan_toko:
        # Skip jika toko tidak ada di response
        if nm_toko not in store_map:
            continue

        stores = store_map[nm_toko]

        skuId = stores["options"][0]["skuList"][item]["id"]
        stock = stores["options"][0]["skuList"][item]["stockValue"]
        price = stores["options"][0]["skuList"][item]["price"]
      
        if stock == 999999:
           stock = 100
        
        sku_detail = {"SKU" : skuId}
        price_mp, price_shopee = hitung_harga(price)
        mp_price_final = {"Price MP" : price_mp}
        shopee_price_final = {"Price Shopee" : price_shopee}
        product_name_dict = {nm_toko : stock}
        data_row.update(sku_detail)
        data_row.update(mp_price_final)
        data_row.update(shopee_price_final)
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

import math

def hitung_harga(B2):

  # Menentukan profit berdasarkan modal
  if B2 < 5000:
      profit = 3800
  elif B2 < 10000:
      profit = 6500
  elif B2 < 20000:
      profit = 2000 + (B2 * 0.52)
  elif B2 < 35000:
      profit = B2 * 0.50
  elif B2 < 50000:
      profit = B2 * 0.43
  elif B2 < 70000:
      profit = B2 * 0.37
  elif B2 < 100000:
      profit = B2 * 0.28
  elif B2 < 150000:
      profit = B2 * 0.25
  elif B2 < 200000:
      profit = B2 * 0.20
  elif B2 < 250000:
      profit = B2 * 0.20
  elif B2 < 300000:
      profit = B2 * 0.20
  elif B2 < 500000:
      profit = B2 * 0.20
  else:
      profit = 0

  # Uang bersih yang ingin diterima
  target_bersih = B2 + profit

  # Menghitung harga jual marketplace
  harga_mp = (target_bersih + 1250) / 0.80
  harga_shopee = (target_bersih + 1250) / 0.76

  # Pembulatan ke ratusan
  harga_final = math.ceil(harga_mp / 100) * 100
  harga_final_shopee = math.ceil(harga_shopee / 100) * 100
  
  return harga_final, harga_final_shopee

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
  if sys.argv[1] not in ("tiktok"): # Nama file sku
    print("Load Data SKU..")
    sku_list = sys.argv[1:]
    data = hit_api(sku_list)
    print(json.dumps(data, indent=4))

  else:
    print("Masuk ke import file")
    
    file_name = sys.argv[1]
    module = importlib.import_module(file_name)
    mylist = getattr(module, 'mylist')

    batches = split_list(mylist, 100) #Batches ini menampung slit data tiap 100 sku
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
            