import http.client
import json

conn = http.client.HTTPSConnection("graphql.jakartanotebook.com")
payload = json.dumps([
  {
    "operationName": "AllCheckoutOptions",
    "variables": {
      "input": {
        "items": [
          {
            "id": "7CHZGIWH",
            "quantity": 1
          }
        ]
      }
    },
    "query": "mutation AllCheckoutOptions($input: CheckoutRequestInput!) {\n  getCheckoutOptions(requestBody: $input) {\n    online {\n      text\n      stores {\n        ...storesInfo\n        __typename\n      }\n      type\n      __typename\n    }\n    pickup {\n      text\n      stores {\n        ...storesInfo\n        __typename\n      }\n      type\n      __typename\n    }\n    cod {\n      text\n      isEnabled\n      disabledText\n      fees {\n        weight {\n          min\n          max\n          __typename\n        }\n        isSelected\n        fee\n        __typename\n      }\n      stores {\n        ...storesInfo\n        __typename\n      }\n      type\n      __typename\n    }\n    announcements\n    __typename\n  }\n}\n\nfragment storesInfo on CheckoutStore {\n  name\n  options {\n    skuList {\n      stockValue\n    }\n   }\n }"
  }
])
headers = {
  'content-type': 'application/json'
}
conn.request("POST", "/graphql/v3", payload, headers)
res = conn.getresponse()
data = res.read()
response_data = data.decode("utf-8")
# print(data.decode("utf-8"))

# Close the connection
conn.close()

lokasi = response_data['stockValue']
print(lokasi)


# pretty_json_response = json.dumps(json_response, indent=4)
