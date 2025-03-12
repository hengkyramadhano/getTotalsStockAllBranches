import requests
import json
from sku_product_mapping import sku_product_mapping

def update_stock(sku):

    # for product_id in sku[:2]:
    #     print(f"Hasil: \"{sku_product_mapping[0].get(product_id.get('SKU'))}\"")

    url = "https://gql.tokopedia.com/graphql/IMSUpdateProductWarehouse"

    payload = json.dumps([
      {
        "operationName": "IMSUpdateProductWarehouse",
        "variables": {
          "input": {
            "shopID": "1217314",
            "productWarehouse": [
                {
                    "productID": json.dumps(sku_product_mapping[0].get(product_id["SKU"])),  # Pastikan SKU ada di mapping
                    "warehouseID": "3983159",
                    "stock": f"{int(json.dumps(product_id['Gudang online'])) + int(json.dumps(product_id['Toko Jakarta Pusat']))}"
                }
                for product_id in sku[:50]
            ]
            # "productWarehouse": [{"productID": f"\"{sku_product_mapping[0].get(product_id.get('SKU'))}\"", "warehouseID": "3983159", "stock": "100"} for product_id in sku[:2]]
          }
        },
        "query": "mutation IMSUpdateProductWarehouse($input: UpdatePWRequest!) {\n  IMSUpdateProductWarehouse(input: $input) {\n    header {\n      messages\n      reason\n      error_code\n      __typename\n    }\n    data {\n      product_id\n      warehouse_id\n      stock\n      price\n      shop_id\n      status\n      __typename\n    }\n    __typename\n  }\n}\n"
      }
    ])
    headers = {
      'accept': '*/*',
      'accept-language': 'en-US,en;q=0.9',
      'content-type': 'application/json',
      'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
      'Cookie': '_gcl_au=1.1.539197710.1737153251; _SID_Tokopedia_=DgZznGiWRuyvbARUAE0J__WlgbyKj9ME5B_k8nzf0aRyM7DuU1MNOuqyHLiqb1f__XxmATxSM70ppfYmEyoyEC0gR6z1sSPtnQUUr4dEXOZsJSvk_qvCzUEXDKyamOuc; DID=f35e6a74d34432de76e946a1b8d622f2d013de95f140fd2b546ef5123c5b112751e43c015599c3e31369252cb015530a; DID_JS=ZjM1ZTZhNzRkMzQ0MzJkZTc2ZTk0NmExYjhkNjIyZjJkMDEzZGU5NWYxNDBmZDJiNTQ2ZWY1MTIzYzViMTEyNzUxZTQzYzAxNTU5OWMzZTMxMzY5MjUyY2IwMTU1MzBh47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU=; _gid=GA1.2.770516540.1737153252; _m4b_theme_=new; passport_csrf_token=3189238bce85cf75d2790b298a5588f2; passport_csrf_token_default=3189238bce85cf75d2790b298a5588f2; _tt_enable_cookie=1; _ttp=4ZBz64Q1TLvgg1vg88zeqvF_5af.tt.1; l=1; tkpd-x-device=undefined; TOPATK=aYIJ4AVuRnGHuKVUx6B9aw; tuid=9750787; gec_id=41879311275278016; uidh=RhWo18PlN3JqrRc7TpBCkyhHmwkIqcCVC7A06t0P0Rk=; FPF=1; uide=NgJsvqoXt9raEZRTboHWLu5sczzZk6n6Rh0jYTe0oIETUaU=; aus=1; _CASE_=7f26654d60263e263534333d373d373133262826674d60263e3533322826604d60263e36363c34282668517460263e263634363129343529353c5034313e37323e36372f34333e3434262826686570263e2629322a353d3d343430323031373237373237262826686668263e26567169656c244c616a636f7d2456656965606c656a6b262826686b6a63263e263534322a3c353737303c313235323c313d3c26282674476b263e263534363734262826774d60263e3535313734313337282677507d7461263e266b6b67262826734d60263e342826736c77263e265f59262826736c7777263e265f592679; _UUID_CAS_=f962959f-e3cd-42bd-9ba6-bf31aad3cc55; sid_guard=02db8819c7876e956915fff56645b9e0%7C1737153953%7C5184000%7CTue%2C+18-Mar-2025+22%3A45%3A53+GMT; uid_tt=22173ea23a778455613bf79c1ace976d62a1109df751f8efc3e502d1ce00922e; uid_tt_ss=22173ea23a778455613bf79c1ace976d62a1109df751f8efc3e502d1ce00922e; sid_tt=02db8819c7876e956915fff56645b9e0; sessionid=02db8819c7876e956915fff56645b9e0; sessionid_ss=02db8819c7876e956915fff56645b9e0; sid_ucp_v1=1.0.0-KDMwYjU0ZmZkYjA2NDg1MDg5ZThmNzFkM2Y1MDI1MmMxNmNhMmExYjAKFQiBiMicismvl2IQoburvAYY5B8gDBADGgNzZzEiIDAyZGI4ODE5Yzc4NzZlOTU2OTE1ZmZmNTY2NDViOWUw; ssid_ucp_v1=1.0.0-KDMwYjU0ZmZkYjA2NDg1MDg5ZThmNzFkM2Y1MDI1MmMxNmNhMmExYjAKFQiBiMicismvl2IQoburvAYY5B8gDBADGgNzZzEiIDAyZGI4ODE5Yzc4NzZlOTU2OTE1ZmZmNTY2NDViOWUw; SHOP_ID=7159823510867624197; _UUID_NONLOGIN_=c1ae988af60ede2456c46903a000f545; _UUID_NONLOGIN_.sig=JtamP3amAeuhbTKnKGcVM-2X6V4; tt_ticket_guard_client_web_domain=2; msToken=Amo7zxo7e0M2Smli7L-jw32EruNU7LXD_Z7Mrw4VK9lFwdJ_TSolf55M5PY9fzMs9GFqabXPd5f52irqrTDdzUlVppBmEVzP8RHatXTQfrThVKNRkewmylZq1HASbw==; NR_SID=NRm7vgikrle2y3ob; odin_tt=4199bfce3cdc371ed7e018a311bd256844d6131c75e5204fa591472dbcc5349cf967d276571195079d606aac04757183a4fd753e6f4bde2d51639f3379398dd3; webauthn-session=18956f14-b898-4b1d-a605-fd336f603855; ttwid=1%7CJ3jKqxWY6mjoyPgXgY9IcVt3a2fAo7kb7xDBiaybxKg%7C1741728988%7Ce3b91a770a987c454a43511f4b4a211d8fb4e02de632f15842dcf9023a3fbb1b; tt_ticket_guard_client_data=eyJ0dC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwidHQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJ0dC10aWNrZXQtZ3VhcmQtcHVibGljLWtleSI6IkJLdHdBOE80N3lIeGdhVzdudFpRZWtuTnExMWRDVURBR1g1Q0RjWlVzUzlqNEpZSkxqOGRENzM3a2VLbG1LTlFjSXFremJKekd6eFppWWZSSWY4T04vRT0iLCJ0dC10aWNrZXQtZ3VhcmQtd2ViLXZlcnNpb24iOjF9; _ga_BZBQ2QHQSP=GS1.1.1741728987.408.1.1741729153.0.0.902213938; bm_sz=A7865ADCBF802104DD4C90CA535E449F~YAAQfIM0Fy8otYGVAQAA0dwmhxsj6m43Ja7LRrlyNLH7nT//SdevpFaK8LWJvc9DOCYzXvcxvEJjZfpb5vdLXxIjzRrtETLCnXQ/NWjibEt3Wof34YpZt9dXfig4KXrrjygplyLeKbNVlezoOhFvxLO9b7mzwd2+Y3XAmwFnw5JO3hG/d8inIswtatO9xa+jK3f7yGUoctt14wt2/PqfqQsdtPxoqMutaBukkvuPpstLHqngU4IAGgO7t1b2czNB/yJYZTDA4P/tkJfdnuqsyuLetgqR5N1OqoZpYuHg0xTVBC/uxD+Y0bq3cfbQvJ/8nzNQwaasYVZF3mDZZi6O+V85ZVf7WP71l6kkZ4uj3ypZXg/BE2d7ENA=~3355955~4342066; _abck=0EA40FD265B0F7C1F12392FA329A5E6B~0~YAAQvgMKctdHJH+VAQAAcvFbhw0ZWYptpPkCT5E1vHp/KV+IhxeVNGA7EnomWC7QK1hXkLJ4EJsJi5GiuDDaT1RSUmKr5T5U5CC4KSe710JZO/nn89dgtxqZnkrhRFvqUrTtOZrG+is8+hB3EpQravM0eH0VsXNLEg6ZHg0YG1kmWGAk30r8ZUPT+vMVakmDCqWlfTYpDV0NRge626GodwjJgxFimfonp2NRCnJYQUW21XUtKSx6yFC9tdXCh1MrX5UCGzXKMSxf6BI2Tlk17sn0Oob8D1XmTwIvqYgKVqRwcLDjV+lsTDB03KcNv/DLNUdn6PS4i+hl+Sd4SluzI69tIXmxYo+gaB7qQp60fMMXjvlGSZIg9RPq6fP01gBCDiPWWuxapR3YAR+bhseXupyUPLwSi69wdKdHQrab3lKjeFNPRgkEJJVQleLbc7CtOojEyvYbDyPssWGBNLjGvfmSHR761kV7jm2AyB54cFn1BsxUWH3KHtr6xFOVn0LNh/ULiR8sw0DIdaNm506xixfEuMLiNlHzX7UU2KTULXi+aH+S0gSY6hn/rBPOAT6xB4hlJ9W7usBVf3rEZ7O4MiL2VknRasIsCz9p4SHs2t27lK7srIKodlyqxTW47AW3DlknfmZBA7ya6ihp3usb6gD8XL9xBIqbfSnp932K40g0EbGUMt4rtwuivS5fzZ24Zp8SZGUt/zLEYSPxEZcpx7d5tXsP~-1~-1~-1; ISID=%7B%22seller.tokopedia.com%22%3A%22c2VsbGVyLnRva29wZWRpYS5jb20%3D.8549e6c8dfb844e9d8f3295bf949b026.1741732575052.1741732575052.1741732705046.2%22%2C%22www.tokopedia.com%22%3A%22d3d3LnRva29wZWRpYS5jb20%3D.890d82aaebb164424abfe5b7703bd3fd.1736894883041.1736894883041.1741364892515.57%22%2C%22ta.tokopedia.com%22%3A%22dGEudG9rb3BlZGlhLmNvbQ%3D%3D.85360aba72966460c8fe09a0c732e71b.1722846026421.1722846026421.1725266756057.4%22%2C%22accounts.tokopedia.com%22%3A%22YWNjb3VudHMudG9rb3BlZGlhLmNvbQ%3D%3D.8d929a09be2e34e9a88386a4da843228.1724329072491.1724329072491.1735526121849.3%22%2C%22developer.tokopedia.com%22%3A%22ZGV2ZWxvcGVyLnRva29wZWRpYS5jb20%3D.8283dc0b5157842ea98b25873ac43dfc.1740826555742.1740826555742.1740826555742.1%22%7D; _ga_70947XW48P=GS1.1.1741732484.475.1.1741732705.59.0.0; _ga=GA1.1.18400375.1737153251; _abck=0EA40FD265B0F7C1F12392FA329A5E6B~-1~YAAQN1A7Fzhaz4OVAQAAbEgRiw1MXv8vBMbQBUfcFXgZCRS/JhUH5PfYa77yV1VBo90rvtLaC1DkXxMKpnDoI1oFPrXa9tMgSZUnUNCEXM6l/W10kghN76B/7N6Gy7Y/QaMmxufznhKYL/tNet7Cne+TniImLi1FK/Cefq0e0ElNnYNjrivouSNM3PvV6NCGbq8CcfJy/9a2JULG6s0PzKyE5I6TxEaVPlmX12Y+WFDVUjZY8mV74nRLdDj3q7trt7XlpqYO57Dx9d2WE92ntI5UQky7JDu8LiMrvYgJUn8JDZL1b9+wiKZQRD5wN3tFseU9e/xcW7sDwJimG59uhDogOzX0jQf5awZdNXBLGvoAFM1TULTeYYtefVOMz9+c8TOCxU20KRwDSA41CnNHbCzoqFJn0hXvYLuYvX7V1Hjz75ap8qJ6tUJhaIvJ6aEeeIJj0w0BsDp2cnnTIU2s72291RnjvuGNnug2NaFMabg0TQItpS2L5EQxDlj05SkBN34cI++SOF8pt7yy6lF7vquatSgViEEypkS/Qk6X55dU88fy8qyhEjRb5PfXtui9ZV9FLP6eVrzVps8l6a+MpvuhRyx8EfvDa3gaWR3rurEJc3fp+PjRsXNjp1pemhPwLArvqFGEH0bhaWQ43khb/UDMaca1QEgJU2/fiSopAvkYHra6tylhhdJHPQ==~0~-1~-1'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # print(response.text)


def split_dict(lst, chunk_size=50):
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


with open("dataSKU.json", "r") as file:
    dataSKU = json.load(file)

print(f"Total SKU: {len(dataSKU)}")

batches = split_dict(dataSKU, 50)
jumlahSKU = len(batches)

print(f"Jumlah Perulangan: {jumlahSKU}")

for j in range(jumlahSKU):
    try:
        data = update_stock(batches[j])

    except Exception as e:
        print(f"Error for sku : {e}")


# sku = dataSKU[1].get("SKU")
# print(sku)
# print(sku_product_mapping[0].get(sku))

# sku_dict = sku_product_mapping[0]