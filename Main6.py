import requests
import json
import sys
from sku_product_mapping_shopee import sku_product_mapping as shopee_mapping


with open("dataSKU.json", "r") as file:
    dataSKU = json.load(file)


def getCodeVariant(productID):

  url = f"https://seller.shopee.co.id/api/v3/product/get_product_info_for_quick_edit?SPC_CDS=7ed10ba2-7a4f-487d-a2d8-06ad1f95c401&SPC_CDS_VER=2&product_id={productID}&is_draft=false"

  payload = {}
  headers = {
    'accept': 'application/json, text/plain, */*',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'Cookie': 'fulfillment-language=id; _QPWSDCXHZQA=7cd86e9c-b65b-4742-b81c-f404e6366d46; SPC_CDS=7ed10ba2-7a4f-487d-a2d8-06ad1f95c401; SPC_CDS_VER=2; SPC_SC_SA_TK=; SPC_SC_SA_UD=; SPC_SC_OFFLINE_TOKEN=; SC_SSO=-; SC_SSO_U=-; SPC_CDS_CHAT=d7da2afd-8bf0-431a-95e1-d3092a862d13; _sapid=78ab8b893f30f1ef2350d4fec7b3e0b30bd9ca49cf3f3036d4e12d52; REC7iLP4Q=4d91d270-320c-4756-a238-d54ddd785305; SPC_F=fxJLnEQzkCkWKrpfenKjCKspqYcRfrlK; SC_DFP=MILdziIelGBIQrJSkWGWXXmtwpvJoZke; REC_T_ID=434759fe-b525-11ef-b011-0e4ff3912761; SPC_CLIENTID=ZnhKTG5FUXprQ2tXpmarhaoxvrxhkahz; _gcl_au=1.1.1702852482.1735857676; _ga_TEVYGNDY1K=GS1.1.1736096872.2.0.1736096872.60.0.0; SPC_SI=nzFpZwAAAABua1JTc0RFMbjrOgAAAAAAWUxiZlBYaVo=; _ga_QMX630BLLS=GS1.1.1739847341.6.0.1739847341.60.0.0; web-seller-affiliate_language=id; MOCK_TYPE=; web-seller-affiliate-region=id; language=id; _ga_8TJ45E514C=GS1.1.1741709419.2.1.1741709783.60.0.0; SPC_T_IV=TWxTT0dVWWloN2p6REZHQw==; SPC_R_T_ID=ozP/f3YYXCq1oVW68Zbg7LEFBcYav5OaRh3h6WtjjGAEM6nfufZaa/2Nbdz6xysaOmdHviiiqeSNW5bH/ddYiYwkij7br5bDdmGLc+LAyhHJbFlwuCyUg452V37xghhW8p67XtT0oEoEuJ+GNQPj/s9A3gnk8XNOBvWriPgiOR4=; SPC_R_T_IV=TWxTT0dVWWloN2p6REZHQw==; SPC_T_ID=ozP/f3YYXCq1oVW68Zbg7LEFBcYav5OaRh3h6WtjjGAEM6nfufZaa/2Nbdz6xysaOmdHviiiqeSNW5bH/ddYiYwkij7br5bDdmGLc+LAyhHJbFlwuCyUg452V37xghhW8p67XtT0oEoEuJ+GNQPj/s9A3gnk8XNOBvWriPgiOR4=; SPC_SI=nzFpZwAAAABua1JTc0RFMbjrOgAAAAAAWUxiZlBYaVo=; SPC_U=-; _ga=GA1.1.1315976015.1650768788; SPC_EC=.TndPV1BNZFZXd2J6NmhSQ1E4lhyJmIZ7HjDYu7IuGVCYNBf24BeeAq0QyLmLmDt+8ZA9Oi9+B9NLuEYl5K/MOgOPayzxC38Z4v2B813h7l7kYAik3lkXPFY9ZOTpaBOXwzBJIXQqNwQ2G/BYxMFWu8Zw+Bd/oBUHF+rWHScYRaChyxGtBR/Lc9Y8yZ3gMORZil4ke+Spm4Fk2GYF0OiB6+5MzjJKCXkmaPEfN2fEcu4=; SPC_ST=.OWN3dlM4QXlMWmN5c0hBOGaCb+GHAR2H9gOD1x/Geze6oP9pBkkBicVXUFLGp3aY6q9R+hDiGY6ID0N0WmdVo2vNQ/wup9R6vMZN+D93+VYsbdnmQ3/najEZhaJfqjxDruMnK8uBIvFcRwQDGcDW0wq++qxh4elRLaAEOV8aI+hTrbxE3JDEC/9CoDI/sj+CFOC9y34+QwiN6whR6Yhr3wAi0sszM+IbeYK65Zt6uPQ=; _ga_SW6D8G0HXK=GS1.1.1743305193.244.1.1743305849.14.0.0; SPC_SC_SESSION=gYD6ZNsDWv6cKXTX3KVswsmB3HbWQ4LuUf+VGRyxT8Srmb+FPd8hpaetIFIUoliBsHLXOb5jzJ0XNibU9DrlB7+6++hGyRGw3EVWpKArgTt3RLIWa5piK3jmGZJXBAjEPtrOlJ/dF1VN2317scrcyuZwmAo6D39h5FbMGY9P7UxRUqlot98pDiKZZDKJ97ghxhHJwHU5yQ5BOtbhRnS0i+gfCyFH/Tk4eyJbpm8zaiLoOcNAUeAVAWHwsM9iCuF/A_1_51605901; SPC_STK=mfhEIfaN11Y1LQBllBrmtgw029BlsMmxcUoaopwWuUJzU/xylh2r4Yj2ffvGfjLdzCqY1xYYCwmvRCxrL21XPu2zfLTK/sNndKsBXobMMPruLb42GTWeC2AH55eoBzkAp527W5zpDIk75wd5VMCrx65Npc3iD8/1g+Rws1e50Xbb78dgh8WriJ2BBxPDT1cu5fYWky8hIFSvrmM4FsQOzmYszNPrXNz/q/zEzKbWZiotcwn2LnOBtVuB76WUA40FI8pyRkGiNmCW761nCCusxejZTTzg9fuhRu61VHR/hg6lIUbeTtoIpX8Tj9T6O6u+GxDon9BR0nj6okajeA5CTV0ucsP1CM6MjdhbnzmSae37KRpYN1vXINjZ1Df9YplKlXs3/kEjR/KkTG7TKpbMaHKJfxief77NWieXVhKX6qGpk7UlZfz/qVnX/MAYe4LOIVEVlfUNnGMwmdYscFZwyg==; SPC_SEC_SI=v1-VUFYYnRDY2RkdFhuTHk4RNRXbkyqmYaQRiYOXn75oddmzhN7251tSxeFl/n9f5nwJoSm31td/bk6TBJpJKj/EZQymU+n/yYW28ka0eLIvNE=; CTOKEN=wJsM4Q4jEfCJXiLuVlUgww%3D%3D; shopee_webUnique_ccd=6y9x5lLXGeYx%2BUnwgm7t8g%3D%3D%7C4vkUtnnBfUT%2BJv1aVs3v7WG6bsLnGjLpbz2R6%2FrHe0SRXA6b5O7k3t6d0fauWq%2FoH4EUchI88sA%3D%7Cy5v0YTgCsBReNpj2%7C08%7C3; ds=c57d5bf2c3a076de7c9266ea20eb6ac8'
  }

  response = requests.request("GET", url, headers=headers, data=payload)
  json_response = json.loads(response.text)

  # Mengakses model_stock_list secara dinamis
  stock_list = json_response.get("data", {}).get("product_info", {})
  model_stock_list = stock_list.get("model_list", [])

  for model in model_stock_list:
    variantID = model.get("id")
    skuID = model.get("sku")
    getInfo(productID, skuID, variantID)

def getInfo(product, sku, variant):
   
   sku_dict = {item["SKU"]: item for item in dataSKU}
   item = sku_dict.get(sku, {})
   total_stock = item.get("Gudang online", 0) + item.get("Toko Jakarta Pusat", 0)

   postUpdate(product, variant, total_stock)

def postUpdate(productID, variantID, stock):

  url = "https://seller.shopee.co.id/api/v3/product/update_product_info_for_quick_edit?SPC_CDS=7ed10ba2-7a4f-487d-a2d8-06ad1f95c401&SPC_CDS_VER=2"

  payload = f"""{{
    "product_id": {productID},
    "product_info": {{
        "model_list": [{{
            "id": {variantID},
            "stock_setting_list": [{{
                "location_id": "IDZ",
                "sellable_stock": {stock}
            }}]
        }}]
    }}
}}"""
  headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json;charset=UTF-8',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'Cookie': 'fulfillment-language=id; _QPWSDCXHZQA=7cd86e9c-b65b-4742-b81c-f404e6366d46; SPC_CDS=7ed10ba2-7a4f-487d-a2d8-06ad1f95c401; SPC_CDS_VER=2; SPC_SC_SA_TK=; SPC_SC_SA_UD=; SPC_SC_OFFLINE_TOKEN=; SC_SSO=-; SC_SSO_U=-; SPC_CDS_CHAT=d7da2afd-8bf0-431a-95e1-d3092a862d13; _sapid=78ab8b893f30f1ef2350d4fec7b3e0b30bd9ca49cf3f3036d4e12d52; REC7iLP4Q=4d91d270-320c-4756-a238-d54ddd785305; SPC_F=fxJLnEQzkCkWKrpfenKjCKspqYcRfrlK; SC_DFP=MILdziIelGBIQrJSkWGWXXmtwpvJoZke; REC_T_ID=434759fe-b525-11ef-b011-0e4ff3912761; SPC_CLIENTID=ZnhKTG5FUXprQ2tXpmarhaoxvrxhkahz; _gcl_au=1.1.1702852482.1735857676; _ga_TEVYGNDY1K=GS1.1.1736096872.2.0.1736096872.60.0.0; SPC_SI=nzFpZwAAAABua1JTc0RFMbjrOgAAAAAAWUxiZlBYaVo=; _ga_QMX630BLLS=GS1.1.1739847341.6.0.1739847341.60.0.0; web-seller-affiliate_language=id; MOCK_TYPE=; web-seller-affiliate-region=id; language=id; _med=affiliates; _ga_8TJ45E514C=GS1.1.1741709419.2.1.1741709783.60.0.0; SPC_T_IV=TWxTT0dVWWloN2p6REZHQw==; SPC_R_T_ID=ozP/f3YYXCq1oVW68Zbg7LEFBcYav5OaRh3h6WtjjGAEM6nfufZaa/2Nbdz6xysaOmdHviiiqeSNW5bH/ddYiYwkij7br5bDdmGLc+LAyhHJbFlwuCyUg452V37xghhW8p67XtT0oEoEuJ+GNQPj/s9A3gnk8XNOBvWriPgiOR4=; SPC_R_T_IV=TWxTT0dVWWloN2p6REZHQw==; SPC_T_ID=ozP/f3YYXCq1oVW68Zbg7LEFBcYav5OaRh3h6WtjjGAEM6nfufZaa/2Nbdz6xysaOmdHviiiqeSNW5bH/ddYiYwkij7br5bDdmGLc+LAyhHJbFlwuCyUg452V37xghhW8p67XtT0oEoEuJ+GNQPj/s9A3gnk8XNOBvWriPgiOR4=; SPC_SI=nzFpZwAAAABua1JTc0RFMbjrOgAAAAAAWUxiZlBYaVo=; SPC_SEC_SI=v1-N0NqM3VQMFJYbEZPbEJvcob7S3QeSRY3QL5e3KYIE1G7eidk374BgkL+g4uzwpKSOYUZEhdBMEP7hZ80ijKJyE+iBu+1CssefSTGvCPqD6k=; _gid=GA1.3.550010525.1743305194; SPC_U=-; _ga=GA1.1.1315976015.1650768788; SPC_EC=.TndPV1BNZFZXd2J6NmhSQ1E4lhyJmIZ7HjDYu7IuGVCYNBf24BeeAq0QyLmLmDt+8ZA9Oi9+B9NLuEYl5K/MOgOPayzxC38Z4v2B813h7l7kYAik3lkXPFY9ZOTpaBOXwzBJIXQqNwQ2G/BYxMFWu8Zw+Bd/oBUHF+rWHScYRaChyxGtBR/Lc9Y8yZ3gMORZil4ke+Spm4Fk2GYF0OiB6+5MzjJKCXkmaPEfN2fEcu4=; SPC_ST=.OWN3dlM4QXlMWmN5c0hBOGaCb+GHAR2H9gOD1x/Geze6oP9pBkkBicVXUFLGp3aY6q9R+hDiGY6ID0N0WmdVo2vNQ/wup9R6vMZN+D93+VYsbdnmQ3/najEZhaJfqjxDruMnK8uBIvFcRwQDGcDW0wq++qxh4elRLaAEOV8aI+hTrbxE3JDEC/9CoDI/sj+CFOC9y34+QwiN6whR6Yhr3wAi0sszM+IbeYK65Zt6uPQ=; _ga_SW6D8G0HXK=GS1.1.1743305193.244.1.1743305849.14.0.0; SPC_SC_SESSION=gYD6ZNsDWv6cKXTX3KVswsmB3HbWQ4LuUf+VGRyxT8Srmb+FPd8hpaetIFIUoliBsHLXOb5jzJ0XNibU9DrlB7+6++hGyRGw3EVWpKArgTt3RLIWa5piK3jmGZJXBAjEPtrOlJ/dF1VN2317scrcyuZwmAo6D39h5FbMGY9P7UxRUqlot98pDiKZZDKJ97ghxhHJwHU5yQ5BOtbhRnS0i+gfCyFH/Tk4eyJbpm8zaiLoOcNAUeAVAWHwsM9iCuF/A_1_51605901; SPC_STK=mfhEIfaN11Y1LQBllBrmtgw029BlsMmxcUoaopwWuUJzU/xylh2r4Yj2ffvGfjLdzCqY1xYYCwmvRCxrL21XPu2zfLTK/sNndKsBXobMMPruLb42GTWeC2AH55eoBzkAp527W5zpDIk75wd5VMCrx65Npc3iD8/1g+Rws1e50Xbb78dgh8WriJ2BBxPDT1cu5fYWky8hIFSvrmM4FsQOzmYszNPrXNz/q/zEzKbWZiotcwn2LnOBtVuB76WUA40FI8pyRkGiNmCW761nCCusxejZTTzg9fuhRu61VHR/hg6lIUbeTtoIpX8Tj9T6O6u+GxDon9BR0nj6okajeA5CTV0ucsP1CM6MjdhbnzmSae37KRpYN1vXINjZ1Df9YplKlXs3/kEjR/KkTG7TKpbMaHKJfxief77NWieXVhKX6qGpk7UlZfz/qVnX/MAYe4LOIVEVlfUNnGMwmdYscFZwyg==; CTOKEN=T6O9gA0YEfCjrGqvVJkgng%3D%3D; shopee_webUnique_ccd=Lvjrzw39qf%2FxeE3jMRx1AQ%3D%3D%7C2%2FkUtnnBfUT%2BJv1aVs3v7WG6bsLnGjLpbz2R66C2okqRXA6b5O7k3t6d0fauWq%2FoH4EUchI88sDgHJHsEpM%3D%7Cy5v0YTgCsBReNpj2%7C08%7C3; ds=edc3bdfa3e4581eba8e4c7aec5e8bc26; SPC_EC=.UHgxem9oVDF6MFV1S1UyTsDQZBnPbb7O/TNABFAwP8xUx75XZirRb+AgaZl3g6ISki/D7EeYW/ivWwvzeCmBH6k/M1dGM8zyFUXUAEyQy/GcqPbDcZIKQmk3mo8t4LcmkiU3MRjO9ICNVqQZZysWqSP8MLTAxGAal+8kYWLEPtO9Qdm4KVmcBlra2kTYNGJLFqjsl0ZKidf2PLhSZWWYjOcrfEbIkGK04RXw5neCFNA=; SPC_R_T_ID=ozP/f3YYXCq1oVW68Zbg7LEFBcYav5OaRh3h6WtjjGAEM6nfufZaa/2Nbdz6xysaOmdHviiiqeSNW5bH/ddYiYwkij7br5bDdmGLc+LAyhHJbFlwuCyUg452V37xghhW8p67XtT0oEoEuJ+GNQPj/s9A3gnk8XNOBvWriPgiOR4=; SPC_R_T_IV=TWxTT0dVWWloN2p6REZHQw==; SPC_SI=nzFpZwAAAABua1JTc0RFMbjrOgAAAAAAWUxiZlBYaVo=; SPC_ST=.Skt1RVVmRUFkN3pPaDhmNU68pVOEOL7uky8BEHqg69Zjz3rrJzgrG/+rMAY3tU/yNlUNM/5LuJbXZepypsDFYf7LllO/b5GWxI20Qg90wk2PKDz+IQLGC+NueFvZvtomcRWRLpHIX8Va/tmdXffcbwYJ9dVcUBdNnbgpIMipLgHvmkq8yfc3qQhLdf9SuYr45uSXuYjyCMgfV2JUchjd7UP7OLDzO0BAv5KnEApIr+Q=; SPC_T_ID=ozP/f3YYXCq1oVW68Zbg7LEFBcYav5OaRh3h6WtjjGAEM6nfufZaa/2Nbdz6xysaOmdHviiiqeSNW5bH/ddYiYwkij7br5bDdmGLc+LAyhHJbFlwuCyUg452V37xghhW8p67XtT0oEoEuJ+GNQPj/s9A3gnk8XNOBvWriPgiOR4=; SPC_T_IV=TWxTT0dVWWloN2p6REZHQw==; SPC_SEC_SI=v1-R2N0MndpT09oRUhkNll5cO41R+8wJ98sgbCVbvA4QwKKQFVkYvQsBX4ZSMiSWx9xIbjpR2GOVjNylH8t/5yggpj9YHgwoljOqmHWszz8qrI=; SPC_SI=nzFpZwAAAABua1JTc0RFMbjrOgAAAAAAWUxiZlBYaVo='
  }

  response = requests.request("POST", url, headers=headers, data=payload)


def update_progress(progress):
    bar_length = 50
    filled_length = int(bar_length * progress)
    bar = '#' * filled_length + '-' * (bar_length - filled_length)
    sys.stdout.write(f'\rProgress: [{bar}] {int(progress * 100)}%')
    sys.stdout.flush()

i = 1
jumlahKode = len(shopee_mapping)
for code in shopee_mapping:
   getCodeVariant(code)
   if (i <= jumlahKode):
      update_progress((i / jumlahKode))
      i+=1