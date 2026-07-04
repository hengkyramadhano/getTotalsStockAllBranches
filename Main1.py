import requests
import json
import math
import time
import argparse
import logging
from typing import List, Dict, Any
import pandas as pd
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# ==============================
# CONFIGURATION
# ==============================

API_URL = "https://graphql.jakartanotebook.com/graphql/v3"
TIMEOUT = 20
MAX_RETRIES = 3
UNLIMITED_STOCK = 999999


# ==============================
# LOGGING SETUP
# ==============================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# ==============================
# HTTP SESSION WITH RETRY
# ==============================

def create_session() -> requests.Session:
    session = requests.Session()
    retries = Retry(
        total=MAX_RETRIES,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("https://", adapter)
    return session


# ==============================
# PRICE CALCULATION
# ==============================

def calculate_price(base_price: float) -> int:
    if base_price < 5000:
        adjusted = base_price + 3800
    elif base_price < 10000:
        adjusted = base_price + 6500
    elif base_price < 20000:
        adjusted = base_price + 2000 + (base_price * 0.52)
    elif base_price < 35000:
        adjusted = base_price + (base_price * 0.50)
    elif base_price < 50000:
        adjusted = base_price + (base_price * 0.43)
    elif base_price < 70000:
        adjusted = base_price + (base_price * 0.37)
    elif base_price < 100000:
        adjusted = base_price + (base_price * 0.28)
    elif base_price < 150000:
        adjusted = base_price + (base_price * 0.25)
    else:
        adjusted = base_price + (base_price * 0.20)

    marketplace_fee = adjusted * 0.14 + adjusted + 1400
    final_price = math.ceil(marketplace_fee / 100) * 100

    return int(final_price)


# ==============================
# API CLIENT
# ==============================

def build_payload(skus: List[str]) -> Dict[str, Any]:
    return {
        "operationName": "AllCheckoutOptions",
        "variables": {
            "input": {
                "items": [{"id": sku, "quantity": 1} for sku in skus]
            }
        },
        "query": """mutation AllCheckoutOptions($input: CheckoutRequestInput!) {
          getCheckoutOptions(requestBody: $input) {
            online {
              text
              stores {
                ...storesInfo
              }
            }
          }
        }

        fragment storesInfo on CheckoutStore {
          name
          options {
            skuList {
              id
              stockValue
              price
              subtotal
            }
          }
        }"""
    }


def fetch_sku_data(session: requests.Session, skus: List[str]) -> List[Dict[str, Any]]:
    payload = build_payload(skus)

    response = session.post(
        API_URL,
        json=payload,
        timeout=TIMEOUT,
        headers={"content-type": "application/json"}
    )

    response.raise_for_status()
    json_response = response.json()

    if "data" not in json_response:
        raise ValueError("Invalid API response structure")

    online_data = json_response["data"]["getCheckoutOptions"]["online"]
    stores = online_data.get("stores", [])

    if not stores:
        logging.warning("No stores returned from API.")
        return []

    sku_list = stores[0]["options"][0]["skuList"]

    results = []

    for index in range(len(sku_list)):
        row = {}
        sku_id = sku_list[index]["id"]
        base_price = sku_list[index]["price"]

        row["SKU"] = sku_id
        row["Price"] = calculate_price(base_price)

        for store in stores:
            store_name = store["name"]
            stock = store["options"][0]["skuList"][index]["stockValue"]

            if stock == UNLIMITED_STOCK:
                stock = 100

            row[store_name] = stock

        results.append(row)

    return results


# ==============================
# UTILITIES
# ==============================

def split_batches(data: List[str], batch_size: int = 100) -> List[List[str]]:
    return [data[i:i + batch_size] for i in range(0, len(data), batch_size)]


def export_to_excel(data: List[Dict[str, Any]], filename: str) -> None:
    timestamp = time.strftime("%H_%M_%S", time.localtime())
    df = pd.DataFrame(data)
    output_file = f"{filename}-{timestamp}.xlsx"
    df.to_excel(output_file, index=False)
    logging.info(f"Exported to {output_file}")


# ==============================
# MAIN EXECUTION
# ==============================

def main():
    parser = argparse.ArgumentParser(description="SKU Stock & Price Fetcher")
    parser.add_argument(
        "--file",
        help="Python module containing 'mylist' SKU list",
        required=True
    )

    args = parser.parse_args()

    module = __import__(args.file)
    sku_list = getattr(module, "mylist")

    logging.info(f"Total SKU: {len(sku_list)}")

    session = create_session()
    batches = split_batches(sku_list, 100)

    all_results = []

    for idx, batch in enumerate(batches, start=1):
        try:
            data = fetch_sku_data(session, batch)
            all_results.extend(data)
            logging.info(f"Processed batch {idx}/{len(batches)}")
        except Exception as e:
            logging.error(f"Batch {idx} failed: {e}")

    export_to_excel(all_results, args.file)


if __name__ == "__main__":
    main()