import requests
import json
import pandas as pd
from datetime import datetime, timezone, timedelta
import time

invoiceDict = []

def invoiceDetail(invID, totalSku):
    payloads = json.dumps([
      {
        "operationName": "OrderById",
        "variables": {
          "id": invID
        },
        "query": "query OrderById($id: String!) {\n  orderById(id: $id) {\n    id\n    code\n    comment\n    createdAt\n    deliveryTrackingHistory {\n      logs {\n        createdAt\n        description\n        __typename\n      }\n      __typename\n    }\n    isHandledByHargapabrik\n    detail {\n      additionalCosts {\n        amount\n        name\n        __typename\n      }\n      isPickupOnline\n      insuranceInformation\n      cod {\n        address {\n          receiver\n          telephone\n          address\n          provinceName\n          cityName\n          postalCode\n          __typename\n        }\n        __typename\n      }\n      online {\n        address {\n          receiver\n          telephone\n          address\n          provinceName\n          cityName\n          postalCode\n          __typename\n        }\n        airWaybillCode\n        deliveryService\n        deliveryType\n        formattedDeliveryFee\n        isAllowTrackDelivery\n        isInstantDelivery\n        weight\n        __typename\n      }\n      isPickupOnline\n      pickup {\n        code\n        __typename\n      }\n      pickupOnlineHistory {\n        list {\n          pickerNumber\n          pickerName\n          pickerTelephone\n          totalBox\n          createdAt\n          details {\n            boxCode\n            __typename\n          }\n          pickerImageUrl\n          __typename\n        }\n        pickedBoxCount\n        unpickedBoxCount\n        __typename\n      }\n      pickupOnlineStatus\n      pickupInformation {\n        name\n        mapUrl\n        address\n        operationHour {\n          close\n          holiday\n          normal\n          __typename\n        }\n        __typename\n      }\n      totalBox\n      totalInformation {\n        additional\n        dropship\n        insurance\n        items\n        shipping\n        voucherAbsolute\n        discount\n        __typename\n      }\n      __typename\n    }\n    items {\n      guarantee {\n        isDownloadable\n        __typename\n      }\n      id\n      name\n      imeis {\n        code\n        expiredAt\n        isVoid\n        __typename\n      }\n      weight\n      quantity\n      price {\n        bottom\n        __typename\n      }\n      url\n      __typename\n    }\n    logHistory {\n      createdAt\n      information\n      isDone\n      isRed\n      name\n      title\n      __typename\n    }\n    summaryPaymentInformation {\n      summaryPayments {\n        amount\n        name\n        __typename\n      }\n      __typename\n    }\n    state {\n      isCancelable\n      isNeedPaymentConfirmation\n      __typename\n    }\n    stockBranchName\n    paymentInformation {\n      deposit {\n        value\n        __typename\n      }\n      bankTransfer {\n        bankAccounts {\n          id\n          accountNumber\n          name\n          bank {\n            image\n            __typename\n          }\n          location\n          __typename\n        }\n        uniqueCode {\n          code\n          total\n          __typename\n        }\n        __typename\n      }\n      paidAt\n      __typename\n    }\n    status {\n      name\n      color {\n        background\n        text\n        __typename\n      }\n      __typename\n    }\n    type {\n      id\n      __typename\n    }\n    total\n    waitingPaymentExpiredAt\n    __typename\n  }\n}"
      }
    ])

    try:
        responses = requests.request("POST", url, headers=headers, data=payloads)
        json_responses = json.loads(responses.text)
    except Exception as e:
        print(f"An {invID} exception occurred: {e}")
        

    # uniqueID = json_responses[0]["data"]["orderById"]["id"]
    code = json_responses[0]["data"]["orderById"]["code"]
    createdAt = json_responses[0]["data"]["orderById"]["createdAt"]
    stockBranchName = json_responses[0]["data"]["orderById"]["stockBranchName"]

    # Konversi ke format UTC
    dt_utc = datetime.fromtimestamp(createdAt, tz=timezone.utc)
    # print("UTC Time:", dt_utc.strftime('%d %b %Y, %H:%M:%S'))

    # Konversi ke WIB (UTC+7)
    dt_wib = dt_utc + timedelta(hours=7)
    date = dt_wib.strftime('%d %b %Y, %H:%M:%S')

    print(code, end=" ")
    # print(createdAt)
    for j in range(totalSku):
        skuID = json_responses[0]["data"]["orderById"]["items"][j]["id"]
        productName = json_responses[0]["data"]["orderById"]["items"][j]["name"]
        quantity = json_responses[0]["data"]["orderById"]["items"][j]["quantity"]
        price = json_responses[0]["data"]["orderById"]["items"][j]["price"]["bottom"]

        data_row = {
            "Invoice Code": code,
            "Date": date,
            "Store": stockBranchName,
            "SKU": skuID,
            "Product Name": productName,
            "Quantity": quantity,
            "Price": price
        }

        invoiceDict.append(data_row)

        # print(skuID, end=" ")



url = "https://graphql.jakartanotebook.com/graphql/v3"
limit = "1000"

payload = json.dumps([
  {
    "operationName": "PurchaseHistoryPage",
    "variables": {},
    "query": "query PurchaseHistoryPage($code: String, $page: Int, $statusId: String, $typeId: TypeId) {\n  allOrders(\n    code: $code\n    limit: "+limit+"\n    page: $page\n    statusId: $statusId\n    typeId: $typeId\n  ) {\n    edges {\n      id\n      code\n      createdAt\n      isDropship\n      type {\n        id\n        __typename\n      }\n      salesBranchName\n      status {\n        id\n        color {\n          background\n          text\n          __typename\n        }\n        name\n        __typename\n      }\n      state {\n        isNeedPaymentConfirmation\n        __typename\n      }\n      totalSku\n      firstItem {\n        imageUrl\n        name\n        price\n        quantity\n        __typename\n      }\n      variants {\n        variant1\n        variant2\n        variantColor\n        __typename\n      }\n      waitingPaymentExpiredAt\n      total\n      __typename\n    }\n    pageInfo {\n      total\n      limit\n      currentPage\n      __typename\n    }\n    __typename\n  }\n}"
  }
])

headers = {
  'accept': '*/*',
  'accept-language': 'en-US,en;q=0.9',
  'authorization': 'Bearer eyJraWQiOiJmd0Rqb3BVUFJlbXRJb0diblhwYnRVR0ZvaVpGeEtrOFNoNVA2dXVrRTVFPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJmNzJjNDFlZi0wNDY5LTQyMzUtYWM2MS03N2RhMTBiZGYzZjkiLCJldmVudF9pZCI6IjY0MTY5YjgzLTI1MTItNDcwOC1hYzc0LTE3ZWFmNTEwYTA5OSIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4iLCJhdXRoX3RpbWUiOjE3MTQ2NjkzNDAsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC5hcC1zb3V0aGVhc3QtMS5hbWF6b25hd3MuY29tXC9hcC1zb3V0aGVhc3QtMV95VmFJOHRmeXkiLCJleHAiOjE3NDM4MTQyMjYsImlhdCI6MTc0MzgxMDYyNiwianRpIjoiYTIyYjczMmItZGRmNC00ODAyLThjMGEtOTZkOWQyMDk2ODYwIiwiY2xpZW50X2lkIjoiNDc5amphYmNmb2NmNnZlbzRhbTNkdDRwOG0iLCJ1c2VybmFtZSI6ImY3MmM0MWVmLTA0NjktNDIzNS1hYzYxLTc3ZGExMGJkZjNmOSJ9.ETNvydogI46B2MJiRdSYCeYJWXDbMclRFsFILBehpZGbOwlrILTMf41Psqlz6qVu-o7sWUM73vjkLPDcYvBP70A2RtafVi4H3SlzXAwwBGtU_1GF4WTWULtP7aaQ1QxM_WAezkMcVHsdFIKp7ap8V44YFWDcxUNq9Cq_r2Hq4VASDUrFn40_PVkbZ-NrGHfnhtXqUP0iy4j6A6T8pomAb3P6XW90Od-FEQwZU2Fsk-BIKszCN4HFwHoD4A9FZXfXPSkIX70sbiZ4YrQSwUn7Wsqh8iy0ofODi3p89mRVqMpeHlg-XwmBDloRdqL9KIPCHhi-eMeUjmCvHO8hOJmwzg',
  'content-type': 'application/json',
  'Cookie': '_hjSessionUser_228920=eyJpZCI6Ijk4NzgxMDYwLTNlYzUtNTFjMy1hMTZjLTQ3Yjg3ZTc0NTc4ZCIsImNyZWF0ZWQiOjE2NDk4MjA5OTg2OTYsImV4aXN0aW5nIjp0cnVlfQ==; _fbp=fb.1.1651195628645.437395018; __utmc=57912369; _tt_enable_cookie=1; _ttp=l72d7v2XQJ9Rx6zS_03q0lWbP-7.tt.1; _gcl_au=1.1.1914098985.1739720324; _gid=GA1.2.703875268.1740222869; _ga_KQLQDCFMZ4=GS1.1.1743476086.15.1.1743476093.0.0.0; _gat_UA-27401667-1=1; _ga_W01YK4R47J=GS1.2.1743810630.4818.0.1743810630.60.0.0; _ga_4LQQBHQXCC=GS1.1.1743810630.4428.1.1743810633.57.0.0; _ga=GA1.2.120352113.1649820998'
}

response = requests.request("POST", url, headers=headers, data=payload)
json_response = json.loads(response.text)

count = json_response[0]["data"]["allOrders"]["pageInfo"]["limit"]

for i in range(count):
    ids = json_response[0]["data"]["allOrders"]["edges"][i]["id"]
    status = json_response[0]["data"]["allOrders"]["edges"][i]["status"]["name"]
    totalSku = json_response[0]["data"]["allOrders"]["edges"][i]["totalSku"]
    if (status == "Completed"):
        invoiceDetail(ids, totalSku)
        # print(ids)

# export to excel
df = pd.DataFrame(invoiceDict)
curr_time = time.strftime("%H_%M_%S", time.localtime())
df.to_excel(f'invoices-{curr_time}.xlsx', index=False)