import requests
import json
# from sku_product_mapping import sku_product_mapping
# from sku_product_mapping_eldas import sku_product_mapping
from sku_product_mapping_bestever import sku_product_mapping
from types import SimpleNamespace
import sys

COUNT_SKU = 1
WAREHOUSE_ID = "9617877" # 3983159-Jaknet 4906536-Eldas 9617877-Bestever
SHOP_ID = "9295598" # 1217314-Jaknet 710735-Eldas 9295598-Bestever
COOKIE = '_SID_Tokopedia_=d7RSTUKgwBTtscbhEKW9FbEHTH_WK-Bw2Z8MLzttd8f1DzwrxI8a1M4OS5dw4VyvlSnXNLFICTcZGsl1wrIGCcwr5PzQdsxByp7NQVyQuxbk9SBvE9SLltd_xqFcvhh4; l=1; aus=1; DID_JS=ZjFiZjIzZDJhYTYwYjFkYTM1NzVhMzY2YzIwZTQ2ZDVhOTExMWIzOTUzNjVmMzRjZDQ2NmRmNGZjMWNjOTQyZjRlMDQ0OGI4NTQ1YTNkNDI5OTVkYzY1MmMwYjQwMDFk47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU=; tuid=109815581; _m4b_theme_=new; SHOP_ID=7088186205686350085; _tt_enable_cookie=1; gec_id=471654328986255040; uidh=W0172ZMdG8Du0kFVpdovj0WGdpwyAQqNd1C86RM+tsM=; uide=5FloBKbLg7YdvHvR0CBemUalc6cci31vImowN2+o5WRuLxUbIg==; _clck=17txwrh%7C2%7Cfni%7C0%7C1658; DID=1606339fac816951c0bba055b3a81cf49402eb9a751e51863ea3fc695634abee9c10571d1ed59b47fd770e421a17158c; _CASE_=70296a426f2931293a3a333d3c3b3d333d29272968426f29313a3c3d27296f426f29313939333b2729675e7b6f293129393b393f263a3a263a385f3a3f313b3d313b3d203b3c313b3b292729676a7f293129263d253a323332393c393e333a3c3e3b3b38292729676967293129597e666a632b436a7962782927296764656c2931293a3b3d25333a38383c3c32393f393d383f332927297b48642931293a3b39383b29272978426f29313a3a3e383b3e3c382729785f727b6e2931296464682927297c426f29313b27297c637829312950562927297c63787829312950562976; _UUID_CAS_=5c7a176c-102a-4573-b0b5-dfce43170791; _ttp=5zLB6OnLreCOLmV_v7lEkjDbCA7.tt.1; _UUID_NONLOGIN_=a865c7d55fb607c78033845a67cedcc7; _UUID_NONLOGIN_.sig=L7yRs4-baZ6wODqv7GMKsriBmN4; _uetvid=df5eea302ac911efa59cc5729647e1fe; passport_csrf_token=75b5d7ea7243f2a0a42389c4afea33d3; passport_csrf_token_default=75b5d7ea7243f2a0a42389c4afea33d3; sid_guard=0f9b5fbed9b6497b36951bdb4499c1c9%7C1739100227%7C5184000%7CThu%2C+10-Apr-2025+11%3A23%3A47+GMT; uid_tt=5a327875932fd0112aad9a16a175f8391cd375dc67965054059114539f1775cc; uid_tt_ss=5a327875932fd0112aad9a16a175f8391cd375dc67965054059114539f1775cc; sid_tt=0f9b5fbed9b6497b36951bdb4499c1c9; sessionid=0f9b5fbed9b6497b36951bdb4499c1c9; sessionid_ss=0f9b5fbed9b6497b36951bdb4499c1c9; sid_ucp_v1=1.0.0-KDc3NzRkMTM4N2M0YTk5NjgyMTg1ODNjNWQxNjFmZTVhYWM2NGVlMjUKFQiCiMC4i8P5rmIQw6CivQYY5B8gDBADGgNzZzEiIDBmOWI1ZmJlZDliNjQ5N2IzNjk1MWJkYjQ0OTljMWM5; ssid_ucp_v1=1.0.0-KDc3NzRkMTM4N2M0YTk5NjgyMTg1ODNjNWQxNjFmZTVhYWM2NGVlMjUKFQiCiMC4i8P5rmIQw6CivQYY5B8gDBADGgNzZzEiIDBmOWI1ZmJlZDliNjQ5N2IzNjk1MWJkYjQ0OTljMWM5; tt_ticket_guard_client_web_domain=2; _gcl_au=1.1.45853389.1740054310; webauthn-session=99e304e4-bc30-41ad-9daf-b9bb903e299b; odin_tt=b556ee2b025e78bec8800befe0ea2076eedb6c1fbe323b5d5f119d505b52c9c4b67950735fe41f6e0a66013a3f4346f3dff44b298fa4e4bfdc6feb49bd307b4b; ttwid=1%7CcCZLLSpK1WkfG_jPPQiuhLCny0I5vfguNjCa30C2v9g%7C1742005659%7Ce73e726c24418137349079205e7b352edbd9a41bc1060244ed25937dcc00946f; _gid=GA1.2.2092255244.1742005659; SELLER_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJVc2VySWQiOjcwODgwNzQzODIzNzU5MTI0NTAsIk9lY1VpZCI6NzQ5NDYwNTIzMDY0NTQxNDQyNCwiT2VjU2hvcElkIjo3NDk0NjA1MjMwNjQ1NDE0NDI0LCJTaG9wUmVnaW9uIjoiIiwiR2xvYmFsU2VsbGVySWQiOjc0OTQ2MDUyMzA2NDU0MTQ0MjQsIlNlbGxlcklkIjo3NDk0NjA1MjMwNjQ1NDE0NDI0LCJleHAiOjE3NDIwOTIwNjAsIm5iZiI6MTc0MjAwNDY2MH0.h2r5HZQIXvtiHCZb8LaWbz6j2TU2s2yAPw4f65hJox8; tt_ticket_guard_client_data=eyJ0dC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwidHQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJ0dC10aWNrZXQtZ3VhcmQtcHVibGljLWtleSI6IkJORm9BSXkzdzdLYTJZaDBLdVRwK2pNVFBoVlkvTnlsMjh5UWlKYy9XRjVxMjBJWVAvQnJqZU5ySk9FbEJDZjhmeXI0eGUvOGhHU0RNK2p3bGgxakxBYz0iLCJ0dC10aWNrZXQtZ3VhcmQtd2ViLXZlcnNpb24iOjF9; bm_sz=FD067C1C43526E693E3B29798963379F~YAAQa4M0F5kVOY6VAQAA6+yglxu/hqChsZw/Ow8gAzwPkJkBf7kBG9rxeoWinzzXjCwm+GW46FqzhEUWEBBMj2SiwFnS9plQyj1dq069Qncw8jA7XLscShuJBFcF9BTzhsE/6YLPxpuFHPtcgboRCdIOFWVAFAaohLrgbv8V1Pn5OWtg/wmLwUB/Knes0N4IozxOu7W3Q+8kVly6NeVqnasKDawst+F+J54bkSRledbpI8ypNhdgv6sDFlS6yPddt4VhN8Wc/b3XWDaJhDx9XdfhVKgaliitKkinfAdBRmraDx3sQAnAd97YvuRmZ0K4XOZFNRGP2ipMuTWGnXxwl/nkOBLEV/VWjfLetAeLfvUB0na3/ENQKvQ=~4469559~3421491; _ga_BZBQ2QHQSP=GS1.1.1742005661.535.0.1742005661.0.0.1212300895; _abck=7AEF582E5E64A2B0028CE06961EB5E61~0~YAAQXgIKciuYd5SVAQAAPT+nlw1vUJkcgS90VoGszsy43yT/UyXcbhWNqBJsv5YcxlkPh9syDoj4pdcHpjGacv4DVwhqIy0VV5lmx07u1LKqSAtpCRb2OWQ1V0bl0E1FrO1FcqzHGu4NUfTRGcB03K8BLjdVUsPF+7xz1FWmMiytLO0E+f51RPxKfVkEhVeUEkUjf9+tgf9WC9cp4q8LBWZ3E+NE2DyRYEOqHFz3NbfC+DviuP/awVzn6hsvLcwUTWcEmtQi5ZOvob7z651fr5X4Whr52URHkXY9/32EaMTa0W3QAYxpEDn26h3simwiHMWk15GLZCuVG8fV0Hy/I/vQrIrxRHe42LR7HDav0Btb9vi4sK9FqH7BgIiK6h72WUUXRDLgSJW1VMhiOz5oN59ZtAGUIkDgPg7R2LtjOpMLCkZKA/mawemY3a4PNtgT+PIx0uCCMUwucN/wP+nQkDxqnW5xcYDjJAJPclbAFuWCXKbgCmUmlhgDS+OZif0SEzC78NGV9yV3v0n2t6nGmPytXQtFrraERP2+KZz5GO5MrnAUYzrv/71e6WrXGgPZZaE9tsJMcxt2OX7agGDzJQC0KDrW3EQlI2ei877VWDL4U7p7bKa4o9WyRr5nxONu9zcc4eS3yh8N+vb3ujySEWvUVgfWDC7GMytH3xfrCmbDfY7ga/IbRhq/jtR570T4PZOSPKgvxwKBEXoty2Fbd9PenDtMSAt0oEIxa8RKA1ga6HUD~-1~-1~-1; _ga=GA1.2.4230394.1649834302; ISID=%7B%22seller.tokopedia.com%22%3A%22c2VsbGVyLnRva29wZWRpYS5jb20%3D.85c4247e3e7a44917b74c56470ccaeb5.1742009656263.1742009656263.1742009656263.1%22%2C%22www.tokopedia.com%22%3A%22d3d3LnRva29wZWRpYS5jb20%3D.8f670d018b2e9472998b05c3d1974059.1715927789215.1715927789215.1740408829395.12%22%7D; _dc_gtm_UA-126956641-6=1; _dc_gtm_UA-9801603-1=1; _ga_70947XW48P=GS1.1.1742009656.4989.1.1742009660.56.0.0'

def update_stock(sku):

    # for product_id in sku[:2]:
    #     print(f"Hasil: \"{sku_product_mapping[0].get(product_id.get('SKU'))}\"")
    # print(json.dumps(sku_product_mapping[0].get(sku[0]["SKU"], "SKU Not Found")))

    url = "https://gql.tokopedia.com/graphql/IMSUpdateProductWarehouse"

    # Inisialisasi productWarehouse
    productWarehouse = []
    skuID = ""

    # Loop melalui 2 SKU pertama dari daftar SKU
    for product_id in sku[:COUNT_SKU]:
        skuID = product_id["SKU"]
        productID = sku_product_mapping[0].get(skuID)
        stockID = int(product_id["Gudang online"]) + int(product_id["Toko Jakarta Pusat"])
        # print(f"productID: {productID}\nstockID: {stockID}")

        if productID is None:  # Jika SKU tidak ditemukan, lewati iterasi ini
            print("skip", end=" ")
            continue
          
        productWarehouse.append({
            "productID": str(productID),  # Pastikan productID dalam format string
            "warehouseID": WAREHOUSE_ID,
            "stock": str(stockID)
        })
    # print(productWarehouse)

    payload = json.dumps([
      {
        "operationName": "IMSUpdateProductWarehouse",
        "variables": {
          "input": {
            "shopID": SHOP_ID,
            "productWarehouse": productWarehouse
          }
        },
        "query": "mutation IMSUpdateProductWarehouse($input: UpdatePWRequest!) {\n  IMSUpdateProductWarehouse(input: $input) {\n    header {\n      messages\n      reason\n      error_code\n      __typename\n    }\n    data {\n      product_id\n      warehouse_id\n      stock\n      price\n      shop_id\n      status\n      __typename\n    }\n    __typename\n  }\n}\n"
      }
    ], indent=2)
    headers = {
      'accept': '*/*',
      'accept-language': 'en-US,en;q=0.9',
      'content-type': 'application/json',
      'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
      'Cookie': COOKIE
    }

    # print(payload)

    response = requests.request("POST", url, headers=headers, data=payload)

    json_response = json.loads(response.text, object_hook=lambda d: SimpleNamespace(**d))

    validation = json_response[0].data.IMSUpdateProductWarehouse.header.error_code
    print(f"error_code: {validation}")
    
    # try: 
    #     productID = json_response[0].data.IMSUpdateProductWarehouse.data[0].product_id
    # except Exception as e:
    #     print(f"Error respond : {e} {sku_product_mapping[0].get(sku[0].get('SKU'))}")
    print(f"{response.text}\n")


def split_dict(lst, chunk_size=COUNT_SKU):
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

def update_progress(progress):
    bar_length = 50
    filled_length = int(bar_length * progress)
    bar = '#' * filled_length + '-' * (bar_length - filled_length)
    sys.stdout.write(f'\rProgress: [{bar}] {int(progress * 100)}%')
    sys.stdout.flush()


with open("dataSKU.json", "r") as file:
    dataSKU = json.load(file)

print(f"Total SKU: {len(dataSKU)}")

batches = split_dict(dataSKU, COUNT_SKU)
jumlahSKU = len(batches)

print(f"Jumlah Perulangan: {jumlahSKU}")

i = 1
for j in range(jumlahSKU):
    try:
        data = update_stock(batches[j])
        # if (i <= jumlahSKU):
        #     update_progress((i / jumlahSKU))
        #     i+=1
    except Exception as e:
        print(f"Error for sku : {e}")


# sku = dataSKU[1].get("SKU")
# print(sku)
# print(sku_product_mapping[0].get(sku))

# sku_dict = sku_product_mapping[0]