import httpx
import json
import sys
import importlib
import pandas as pd
from types import SimpleNamespace
from variables import mylist
import asyncio
import time

async def hit_api(sku, client):
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
        "query": "mutation AllCheckoutOptions($input: CheckoutRequestInput!) { ... }"  # Truncated for brevity
    })

    payloadRemindMe = json.dumps([
        {
            "operationName": "AddProductSKUToRemindMe",
            "variables": {
                "requestBody": {
                    "branchIds": ["jz23mo"],
                    "email": "hengkyramadhano@gmail.com",
                    "id": sku
                }
            },
            "query": "mutation AddProductSKUToRemindMe($requestBody: ProductSkuAddProductSKUToRemindMeInput!) { ... }"
        }
    ])
    
    headers = {'content-type': 'application/json'}

    try:
        response = await client.post(url, headers=headers, content=payload)
        response.raise_for_status()

        json_response = json.loads(response.text, object_hook=lambda d: SimpleNamespace(**d))

        data_row = {}
        for item in range(6):
            nm_lokasi = json_response.data.getCheckoutOptions.online.stores[item].name
            stock = json_response.data.getCheckoutOptions.online.stores[item].options[0].skuList[0].stockValue

            sku_detail = {"SKU": sku}
            product_name_dict = {nm_lokasi: stock}

            if nm_lokasi == 'Toko Jakarta Pusat' and stock == 0:
                await client.post(url, headers=headers, content=payloadRemindMe)

            data_row.update(sku_detail)
            data_row.update(product_name_dict)

        return data_row
    except Exception as e:
        print(f"Error fetching SKU {sku}: {e}")
        return None

async def process_skus(skus):
    async with httpx.AsyncClient() as client:
        tasks = [hit_api(sku, client) for sku in skus]
        results = await asyncio.gather(*tasks)
        return [result for result in results if result]

def update_progress(progress):
    bar_length = 50
    filled_length = int(bar_length * progress)
    bar = '#' * filled_length + '-' * (bar_length - filled_length)
    sys.stdout.write(f'\rProgress: [{bar}] {int(progress * 100)}%')
    sys.stdout.flush()

def export_to_excel(data, file_name):
    df = pd.DataFrame(data)
    curr_time = time.strftime("%H_%M_%S", time.localtime())
    df.to_excel(f'{file_name}-{curr_time}.xlsx', index=False)

async def main():
    global file_name
    SKU_Store = []

    if len(sys.argv) > 1:
        if sys.argv[1] not in ("tiktok", "netlook", "shopee", "tourisme", "bestever", "sample"):
            print("Load Data SKU...")
            skus = sys.argv[1:]
            SKU_Store = await process_skus(skus)
            for data in SKU_Store:
                print(json.dumps(data, indent=4))
        else:
            print("Masuk ke import file")
            file_name = sys.argv[1]
            module = importlib.import_module(file_name)
            mylist = getattr(module, 'mylist')

            print(f"Total SKU: {len(mylist)}")
            SKU_Store = await process_skus(mylist)
            export_to_excel(SKU_Store, file_name)
    else:
        print("Tidak ada argumen yang diberikan")
        print(f"Total SKU: {len(mylist)}")
        SKU_Store = await process_skus(mylist)
        export_to_excel(SKU_Store, "default")

if __name__ == "__main__":
    asyncio.run(main())
