import requests
import json
from types import SimpleNamespace

url = "https://gql.tokopedia.com/graphql/jarvisRecommendation"

payload = json.dumps([
  {
    "operationName": "jarvisRecommendation",
    "variables": {
      "productName": "Sapu Garuk Taman Garden Leaf Rake Carbon Steel 15 Teeth"
    },
    "query": "query jarvisRecommendation($productName: String) {\n  getJarvisRecommendation(product_name: $productName) {\n    categories {\n      id\n      name\n      confidence_score\n      precision\n      __typename\n    }\n    __typename\n  }\n}\n"
  }
])
headers = {
  'Referer': 'https://seller.tokopedia.com/add-product',
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
  'accept': '*/*',
  'content-type': 'application/json',
  'Cookie': '_abck=0EA40FD265B0F7C1F12392FA329A5E6B~-1~YAAQVa0wF1kFUO6VAQAAd6TF9Q3ReYFtjHIRWWKyCRnZUYgsq+VC7b5Ig30G3F/kFHlzXkwWTkbIBb1+l0CYgNOdDU6/6R4n7qX16yigqGt0L8kB/SHrgmwOea3NM1N++Xh+ceydCWVBL+0Llz6/j7/Ud/zJ790nIXMD1/H7NXljiTsxj4kFYYmDW4jWhRUooKtqMmb95lpbxwpENnubHe9AgI/0Za6au1wcl+wGkDHoWYrE0pTWBSIjfpkyc4ZJNkakfzJL+2ZOQDpSNlGnm8RwiHcN++xGZApoZSl/qDHX68NxOPeMBq55SplaCq6CQu/bCTmVyL6U0b/YzufkN1ikf/IfiNOLGYZdM1wIMv3y6k6P1StpW7+ckIkFQjN2p+tWHvTzQoMFto71TtlHX0nZBQbq8Z4F/Y47keEn63Pgwf7xBeSG1p9q/0bsIeWZl2PZBI1MqT7RjmEugvEQ3nNhaVgZYrcPKO2Z+OCvn9m8UbQOAWjL2EkZq2ZmxNz0dpLfVGJdDClJzZjpXYWHAotZBvbtNGQtalvRnLWGQypPRx5rIpzLilbwgsTkV8GiNYX+nCSzTeAtTL3NV2SwBguUL+QaqhWYdbVxG53kcA+7po2bJm8uwXteHZKyB4iRtSc4F2euX5gtsis9XsS0WACzZRAvLgPbPqLPSZzoxVE/VtklNPmMpWDBvFmzsHmZ9U3bGPKeQERehMJXCOvxR8B4oS5UnQ==~-1~-1~-1; bm_sz=E02C24028AA9046D826EC0DE7AA19744~YAAQVa0wF1oFUO6VAQAAd6TF9RsZtAm3egM6ymJ+56XUEupQBXlLprsfpguwJi12LjasWJuZgc58EI0udF9fITtyXpQIJ8Loffuyldfx6APod9uTrSZojzzIeT21NslaFeuBGr735rjQshJ9Q6foBqV24r5BOnRe+r8Vp+BAudLDWXbMyj/1tbdnh+WsaOmdSRGmIvWi6zImmAFS9bQTFnHMb2UF2h0hEThUJAL3GPetMsDHBAC+ZtwGXgS2wOxKyGH3X2H8GxddAbKXE08iJCPia1oPkPR8pY+9DxZG2+xcWvVnIfP3J7rX3U/rf91PjSVf7uW/hUpkwn9cZCTSUHDczjcdgsJ4pZKSCsDXKA==~4473157~3747907'
}

response = requests.request("POST", url, headers=headers, data=payload)

# json_response = json.loads(response.text, object_hook=lambda d: SimpleNamespace(**d))
json_response = json.loads(response.text)
codeID = json_response[0]["data"]["getJarvisRecommendation"]["categories"][0]["id"]
print(codeID)  # Output: 1019

