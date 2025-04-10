import requests
import json
import math
import sys
import argparse

# Import SKU mapping berdasarkan kelompok
from sku_product_mapping import sku_product_mapping as jaknet_mapping
from sku_product_mapping_eldas import sku_product_mapping as eldas_mapping
from sku_product_mapping_bestever import sku_product_mapping as bestever_mapping
from sku_product_mapping_katniss import sku_product_mapping as katniss_mapping
from sku_product_mapping_tourisme import sku_product_mapping as tourisme_mapping
from sku_product_mapping_babe import sku_product_mapping as babe_mapping

# Mapping nama kelompok ke datanya
SKU_GROUPS = {
    "jaknet": {
        "mapping": jaknet_mapping, 
        "warehouse_id": "3983159", 
        "shop_id": "1217314",
        "cookie": "_gcl_au=1.1.539197710.1737153251; _SID_Tokopedia_=DgZznGiWRuyvbARUAE0J__WlgbyKj9ME5B_k8nzf0aRyM7DuU1MNOuqyHLiqb1f__XxmATxSM70ppfYmEyoyEC0gR6z1sSPtnQUUr4dEXOZsJSvk_qvCzUEXDKyamOuc; DID=f35e6a74d34432de76e946a1b8d622f2d013de95f140fd2b546ef5123c5b112751e43c015599c3e31369252cb015530a; DID_JS=ZjM1ZTZhNzRkMzQ0MzJkZTc2ZTk0NmExYjhkNjIyZjJkMDEzZGU5NWYxNDBmZDJiNTQ2ZWY1MTIzYzViMTEyNzUxZTQzYzAxNTU5OWMzZTMxMzY5MjUyY2IwMTU1MzBh47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU=; _gid=GA1.2.770516540.1737153252; _m4b_theme_=new; passport_csrf_token=3189238bce85cf75d2790b298a5588f2; passport_csrf_token_default=3189238bce85cf75d2790b298a5588f2; _tt_enable_cookie=1; _ttp=4ZBz64Q1TLvgg1vg88zeqvF_5af.tt.1; l=1; tkpd-x-device=undefined; TOPATK=aYIJ4AVuRnGHuKVUx6B9aw; tuid=9750787; gec_id=41879311275278016; uidh=RhWo18PlN3JqrRc7TpBCkyhHmwkIqcCVC7A06t0P0Rk=; FPF=1; uide=NgJsvqoXt9raEZRTboHWLu5sczzZk6n6Rh0jYTe0oIETUaU=; aus=1; _CASE_=7f26654d60263e263534333d373d373133262826674d60263e3533322826604d60263e36363c34282668517460263e263634363129343529353c5034313e37323e36372f34333e3434262826686570263e2629322a353d3d343430323031373237373237262826686668263e26567169656c244c616a636f7d2456656965606c656a6b262826686b6a63263e263534322a3c353737303c313235323c313d3c26282674476b263e263534363734262826774d60263e3535313734313337282677507d7461263e266b6b67262826734d60263e342826736c77263e265f59262826736c7777263e265f592679; _UUID_CAS_=f962959f-e3cd-42bd-9ba6-bf31aad3cc55; sid_guard=02db8819c7876e956915fff56645b9e0%7C1737153953%7C5184000%7CTue%2C+18-Mar-2025+22%3A45%3A53+GMT; uid_tt=22173ea23a778455613bf79c1ace976d62a1109df751f8efc3e502d1ce00922e; uid_tt_ss=22173ea23a778455613bf79c1ace976d62a1109df751f8efc3e502d1ce00922e; sid_tt=02db8819c7876e956915fff56645b9e0; sessionid=02db8819c7876e956915fff56645b9e0; sessionid_ss=02db8819c7876e956915fff56645b9e0; sid_ucp_v1=1.0.0-KDMwYjU0ZmZkYjA2NDg1MDg5ZThmNzFkM2Y1MDI1MmMxNmNhMmExYjAKFQiBiMicismvl2IQoburvAYY5B8gDBADGgNzZzEiIDAyZGI4ODE5Yzc4NzZlOTU2OTE1ZmZmNTY2NDViOWUw; ssid_ucp_v1=1.0.0-KDMwYjU0ZmZkYjA2NDg1MDg5ZThmNzFkM2Y1MDI1MmMxNmNhMmExYjAKFQiBiMicismvl2IQoburvAYY5B8gDBADGgNzZzEiIDAyZGI4ODE5Yzc4NzZlOTU2OTE1ZmZmNTY2NDViOWUw; SHOP_ID=7159823510867624197; _UUID_NONLOGIN_=c1ae988af60ede2456c46903a000f545; _UUID_NONLOGIN_.sig=JtamP3amAeuhbTKnKGcVM-2X6V4; tt_ticket_guard_client_web_domain=2; msToken=Amo7zxo7e0M2Smli7L-jw32EruNU7LXD_Z7Mrw4VK9lFwdJ_TSolf55M5PY9fzMs9GFqabXPd5f52irqrTDdzUlVppBmEVzP8RHatXTQfrThVKNRkewmylZq1HASbw==; NR_SID=NRm7vgikrle2y3ob; odin_tt=4199bfce3cdc371ed7e018a311bd256844d6131c75e5204fa591472dbcc5349cf967d276571195079d606aac04757183a4fd753e6f4bde2d51639f3379398dd3; webauthn-session=18956f14-b898-4b1d-a605-fd336f603855; ttwid=1%7CJ3jKqxWY6mjoyPgXgY9IcVt3a2fAo7kb7xDBiaybxKg%7C1741728988%7Ce3b91a770a987c454a43511f4b4a211d8fb4e02de632f15842dcf9023a3fbb1b; tt_ticket_guard_client_data=eyJ0dC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwidHQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJ0dC10aWNrZXQtZ3VhcmQtcHVibGljLWtleSI6IkJLdHdBOE80N3lIeGdhVzdudFpRZWtuTnExMWRDVURBR1g1Q0RjWlVzUzlqNEpZSkxqOGRENzM3a2VLbG1LTlFjSXFremJKekd6eFppWWZSSWY4T04vRT0iLCJ0dC10aWNrZXQtZ3VhcmQtd2ViLXZlcnNpb24iOjF9; _ga_BZBQ2QHQSP=GS1.1.1741728987.408.1.1741729153.0.0.902213938; bm_sz=A7865ADCBF802104DD4C90CA535E449F~YAAQfIM0Fy8otYGVAQAA0dwmhxsj6m43Ja7LRrlyNLH7nT//SdevpFaK8LWJvc9DOCYzXvcxvEJjZfpb5vdLXxIjzRrtETLCnXQ/NWjibEt3Wof34YpZt9dXfig4KXrrjygplyLeKbNVlezoOhFvxLO9b7mzwd2+Y3XAmwFnw5JO3hG/d8inIswtatO9xa+jK3f7yGUoctt14wt2/PqfqQsdtPxoqMutaBukkvuPpstLHqngU4IAGgO7t1b2czNB/yJYZTDA4P/tkJfdnuqsyuLetgqR5N1OqoZpYuHg0xTVBC/uxD+Y0bq3cfbQvJ/8nzNQwaasYVZF3mDZZi6O+V85ZVf7WP71l6kkZ4uj3ypZXg/BE2d7ENA=~3355955~4342066; _abck=0EA40FD265B0F7C1F12392FA329A5E6B~0~YAAQvgMKctdHJH+VAQAAcvFbhw0ZWYptpPkCT5E1vHp/KV+IhxeVNGA7EnomWC7QK1hXkLJ4EJsJi5GiuDDaT1RSUmKr5T5U5CC4KSe710JZO/nn89dgtxqZnkrhRFvqUrTtOZrG+is8+hB3EpQravM0eH0VsXNLEg6ZHg0YG1kmWGAk30r8ZUPT+vMVakmDCqWlfTYpDV0NRge626GodwjJgxFimfonp2NRCnJYQUW21XUtKSx6yFC9tdXCh1MrX5UCGzXKMSxf6BI2Tlk17sn0Oob8D1XmTwIvqYgKVqRwcLDjV+lsTDB03KcNv/DLNUdn6PS4i+hl+Sd4SluzI69tIXmxYo+gaB7qQp60fMMXjvlGSZIg9RPq6fP01gBCDiPWWuxapR3YAR+bhseXupyUPLwSi69wdKdHQrab3lKjeFNPRgkEJJVQleLbc7CtOojEyvYbDyPssWGBNLjGvfmSHR761kV7jm2AyB54cFn1BsxUWH3KHtr6xFOVn0LNh/ULiR8sw0DIdaNm506xixfEuMLiNlHzX7UU2KTULXi+aH+S0gSY6hn/rBPOAT6xB4hlJ9W7usBVf3rEZ7O4MiL2VknRasIsCz9p4SHs2t27lK7srIKodlyqxTW47AW3DlknfmZBA7ya6ihp3usb6gD8XL9xBIqbfSnp932K40g0EbGUMt4rtwuivS5fzZ24Zp8SZGUt/zLEYSPxEZcpx7d5tXsP~-1~-1~-1; ISID=%7B%22seller.tokopedia.com%22%3A%22c2VsbGVyLnRva29wZWRpYS5jb20%3D.8549e6c8dfb844e9d8f3295bf949b026.1741732575052.1741732575052.1741732705046.2%22%2C%22www.tokopedia.com%22%3A%22d3d3LnRva29wZWRpYS5jb20%3D.890d82aaebb164424abfe5b7703bd3fd.1736894883041.1736894883041.1741364892515.57%22%2C%22ta.tokopedia.com%22%3A%22dGEudG9rb3BlZGlhLmNvbQ%3D%3D.85360aba72966460c8fe09a0c732e71b.1722846026421.1722846026421.1725266756057.4%22%2C%22accounts.tokopedia.com%22%3A%22YWNjb3VudHMudG9rb3BlZGlhLmNvbQ%3D%3D.8d929a09be2e34e9a88386a4da843228.1724329072491.1724329072491.1735526121849.3%22%2C%22developer.tokopedia.com%22%3A%22ZGV2ZWxvcGVyLnRva29wZWRpYS5jb20%3D.8283dc0b5157842ea98b25873ac43dfc.1740826555742.1740826555742.1740826555742.1%22%7D; _ga_70947XW48P=GS1.1.1741732484.475.1.1741732705.59.0.0; _ga=GA1.1.18400375.1737153251"
    },
    "eldas": {
        "mapping": eldas_mapping, 
        "warehouse_id": "4906536", 
        "shop_id": "710735",
        "cookie": "_SID_Tokopedia_=IZ900S0Yri6iVjRH9GRGiThzorgBEMzcVVgGMfjgnUkU7zx6qyg1Z59e3XQ7ASOqMDU3YIRu8rDruK3tCrZjtwExZVTEn6DLLQxLhWl5wT1Vo5yiKKiVVh1Z7-9blU_E; l=1; aus=1; uidh=M9ra5ixn8/xJmAPf1magFRfC9Xz4wrDHLMBYhS6x3X0=; uide=LldwM7b3/drgtfK7seBc+Va8Npf19Rh49UiZ8VMOBhb0h98=; DID_JS=OTRhNWI3ZDUyZjVhOTM1NTBiODQ5ZWExYmRjNDgyYWZlNTIxYjA1YjVmMGMyYjFkMWE3NzJlNGE3Zjg3ZTQ4NzE0NDAxNTk4MTFmZTViMjA3Mzk0M2ZhNzlhZTVhZjcz47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU=; tuid=5460248; gec_id=23451586588065472; _tt_enable_cookie=1; _uetvid=9fd0a9e0678c11ef9d8497334e2bf313; ttwid=1%7CYTYaKWP-iCLxZTD7356d38zgEpGcD70DQXM_hIILcGg%7C1725103915%7Ccd93d16f13ec0add58f99324ad7d47a75782beccfec83b7ac5a688baa77dbd2c; _ga_BZBQ2QHQSP=GS1.1.1725161116.2.0.1725161116.0.0.1386855536; DID=74e15896c44e05f5725344ac668f1b77fc98dcce3ecc3b6e931675f4c9ff9d0e83c7544fabc29d464dc37ad709cc9e4a; _CASE_=7e27644c61273f273433373337363237272927664c61273f3432332927614c61273f37373d35292769507561273f273735373128343528353751353c3f31363f313c2e35323f3535272927696471273f2728332b343c3c373330373135373035353532272927696769273f274469646864712571706f70646b254d606b626e7c2557646864616d646b6a272927696a6b62273f273435332b3d3436343530363131323237363127292775466a273f273435373635272927764c61273f3434303635303236292776517c7560273f276a6a66272927724c61273f352927726d76273f275e58272927726d7676273f275e582778; _UUID_CAS_=4ecb053c-a412-4be4-819a-2e293d1094cd; _ttp=2c1fzOhFmpb6Q9Wzy9kTxZLA7BT.tt.1; _UUID_NONLOGIN_=b89b89e4e9d82459d1dbd6c808361acd; _UUID_NONLOGIN_.sig=2heaD3etGoxA410s-ijZ84-b738; _gcl_au=1.1.613106944.1735616525; _gid=GA1.2.663872659.1740394283; webauthn-session=d128d61d-d7ae-4a4e-a63e-586aa780af56; _abck=FF184BB5682C139E1C9CE018910DA4DE~0~YAAQB/grF+k5S4yVAQAAtd+fkQ16yOMs0U0CFywvjDPyOxttkPBuX6IKeO0sUgU6NTUMsRg1OMsHnFTaovELHNYnNjYNAlOAZMHg2iQnlQOr5VeebDCl7Yn5YPXSSq3z6B+cYAmSrBHI/dyHSloqTFvWx4k9Y3fyuTVDt0d6XgQEJysL/V0bbBxhCD2+DRCecPt7S8tCg80jskhKEw2IhoKL/VPeEmXlQm537pR7VN+4XVzi6DSWekqiRwWrCNyuNKv3tXCzZ6HOY7ehTJjGXTcELnftLV6S6wbLIcczGn5TzvgnIdGlPrrLqmowSZ/CBz198pWuwyeirghiGThNR4/MW650Kk13Ty1Jjr3sCnaSbGXlfKpXyKeb6SjWq8yeaB62JabJ87JR8mBgXbrDnOEcJCZ0ZhdXCtekF5Ki4pYN4ZmU01XWXPmpo4JFEpKa4xSICJa9RCccexkhp8Y/mnypQFQwjkzdnwk700b1JVOmLEcOjWlly6FhQg6yQPqqdGymgRm5VvruFI3xCdR5l77B0Z9R+WYyD96Bxw/MlSHJsRWhBkQd57ZsQ7AkAw+cxlCEF8s/+ji3YRcbTQKkZoV6KiWusM4UK016w745P56px3ZKktDSfys/EmGXrlLPuQkXshBRYtnHWa/+e8FYBH70mQ0tZXAs7o8Fh4iaweFPHR3crIKaOMEGXdGwnDQo9k8E4h5GuC6fMuOn6Qo=~-1~-1~-1; bm_sz=83C18C395478AC4E5BC50F61B3630C96~YAAQZoM0F1r5RIqVAQAAEchokhvy3jms9VQ0iFXZQv95A75G6LL/r2Kr//yhcMpg0uIlEziGk45BT3rVq0zUnCb8Va5fx7BFjK3UoSxeRDJjRLO9txAeTAE04DVJAbGXHlXf2ItS1+c82bnPE46zPiMLyyuAlS/Ysns+DN3xx9FlVgYp0hDlfZ5XN4cA5IzvBVRSW8VCcwp4zZlCJbfsrVTSV4nDbUEZ0RstwLsEihRPvBP8ieLM5og8/kMrvI+HiQmzRYIr7xLXudkdafDZ0XWqyrxYWLbPNB3F2TI8Z5Am0WMW6SQQF3kdv5XgzfHf5kqTkp1xFzG+zVMvoAsEAllDNwtf4O4SenotfozT+4vkpTNJzmzGkQMSefGnQPLL8b1I4U+hWyWEYXrP86iTjQ==~4272454~3290936; _dc_gtm_UA-126956641-6=1; ISID=%7B%22ta.tokopedia.com%22%3A%22dGEudG9rb3BlZGlhLmNvbQ%3D%3D.841c6ec1d279f4e9ca2c881d031b107d.1704459856539.1704459856539.1704459857932.1%22%2C%22seller.tokopedia.com%22%3A%22c2VsbGVyLnRva29wZWRpYS5jb20%3D.8ae20f8544e3d4890a9d44258a8e93c9.1741904901231.1741904901231.1741918797494.4%22%2C%22www.tokopedia.com%22%3A%22d3d3LnRva29wZWRpYS5jb20%3D.86cc32e560a244fdb912ed90d26c850c.1728392352553.1728392352553.1740987760779.19%22%7D; _dc_gtm_UA-9801603-1=1; _ga=GA1.2.950060650.1649847333; _ga_70947XW48P=GS1.1.1741918094.6088.1.1741918810.47.0.0"
    },
    "bestever": {
        "mapping": bestever_mapping, 
        "warehouse_id": "9617877", 
        "shop_id": "9295598",
        "cookie": "_SID_Tokopedia_=d7RSTUKgwBTtscbhEKW9FbEHTH_WK-Bw2Z8MLzttd8f1DzwrxI8a1M4OS5dw4VyvlSnXNLFICTcZGsl1wrIGCcwr5PzQdsxByp7NQVyQuxbk9SBvE9SLltd_xqFcvhh4; l=1; aus=1; DID_JS=ZjFiZjIzZDJhYTYwYjFkYTM1NzVhMzY2YzIwZTQ2ZDVhOTExMWIzOTUzNjVmMzRjZDQ2NmRmNGZjMWNjOTQyZjRlMDQ0OGI4NTQ1YTNkNDI5OTVkYzY1MmMwYjQwMDFk47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU=; tuid=109815581; _m4b_theme_=new; SHOP_ID=7088186205686350085; _tt_enable_cookie=1; gec_id=471654328986255040; uidh=W0172ZMdG8Du0kFVpdovj0WGdpwyAQqNd1C86RM+tsM=; uide=5FloBKbLg7YdvHvR0CBemUalc6cci31vImowN2+o5WRuLxUbIg==; _clck=17txwrh%7C2%7Cfni%7C0%7C1658; DID=1606339fac816951c0bba055b3a81cf49402eb9a751e51863ea3fc695634abee9c10571d1ed59b47fd770e421a17158c; _CASE_=70296a426f2931293a3a333d3c3b3d333d29272968426f29313a3c3d27296f426f29313939333b2729675e7b6f293129393b393f263a3a263a385f3a3f313b3d313b3d203b3c313b3b292729676a7f293129263d253a323332393c393e333a3c3e3b3b38292729676967293129597e666a632b436a7962782927296764656c2931293a3b3d25333a38383c3c32393f393d383f332927297b48642931293a3b39383b29272978426f29313a3a3e383b3e3c382729785f727b6e2931296464682927297c426f29313b27297c637829312950562927297c63787829312950562976; _UUID_CAS_=5c7a176c-102a-4573-b0b5-dfce43170791; _ttp=5zLB6OnLreCOLmV_v7lEkjDbCA7.tt.1; _UUID_NONLOGIN_=a865c7d55fb607c78033845a67cedcc7; _UUID_NONLOGIN_.sig=L7yRs4-baZ6wODqv7GMKsriBmN4; _uetvid=df5eea302ac911efa59cc5729647e1fe; passport_csrf_token=75b5d7ea7243f2a0a42389c4afea33d3; passport_csrf_token_default=75b5d7ea7243f2a0a42389c4afea33d3; sid_guard=0f9b5fbed9b6497b36951bdb4499c1c9%7C1739100227%7C5184000%7CThu%2C+10-Apr-2025+11%3A23%3A47+GMT; uid_tt=5a327875932fd0112aad9a16a175f8391cd375dc67965054059114539f1775cc; uid_tt_ss=5a327875932fd0112aad9a16a175f8391cd375dc67965054059114539f1775cc; sid_tt=0f9b5fbed9b6497b36951bdb4499c1c9; sessionid=0f9b5fbed9b6497b36951bdb4499c1c9; sessionid_ss=0f9b5fbed9b6497b36951bdb4499c1c9; sid_ucp_v1=1.0.0-KDc3NzRkMTM4N2M0YTk5NjgyMTg1ODNjNWQxNjFmZTVhYWM2NGVlMjUKFQiCiMC4i8P5rmIQw6CivQYY5B8gDBADGgNzZzEiIDBmOWI1ZmJlZDliNjQ5N2IzNjk1MWJkYjQ0OTljMWM5; ssid_ucp_v1=1.0.0-KDc3NzRkMTM4N2M0YTk5NjgyMTg1ODNjNWQxNjFmZTVhYWM2NGVlMjUKFQiCiMC4i8P5rmIQw6CivQYY5B8gDBADGgNzZzEiIDBmOWI1ZmJlZDliNjQ5N2IzNjk1MWJkYjQ0OTljMWM5; tt_ticket_guard_client_web_domain=2; _gcl_au=1.1.45853389.1740054310; webauthn-session=99e304e4-bc30-41ad-9daf-b9bb903e299b; odin_tt=b556ee2b025e78bec8800befe0ea2076eedb6c1fbe323b5d5f119d505b52c9c4b67950735fe41f6e0a66013a3f4346f3dff44b298fa4e4bfdc6feb49bd307b4b; ttwid=1%7CcCZLLSpK1WkfG_jPPQiuhLCny0I5vfguNjCa30C2v9g%7C1742005659%7Ce73e726c24418137349079205e7b352edbd9a41bc1060244ed25937dcc00946f; _gid=GA1.2.2092255244.1742005659; SELLER_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJVc2VySWQiOjcwODgwNzQzODIzNzU5MTI0NTAsIk9lY1VpZCI6NzQ5NDYwNTIzMDY0NTQxNDQyNCwiT2VjU2hvcElkIjo3NDk0NjA1MjMwNjQ1NDE0NDI0LCJTaG9wUmVnaW9uIjoiIiwiR2xvYmFsU2VsbGVySWQiOjc0OTQ2MDUyMzA2NDU0MTQ0MjQsIlNlbGxlcklkIjo3NDk0NjA1MjMwNjQ1NDE0NDI0LCJleHAiOjE3NDIwOTIwNjAsIm5iZiI6MTc0MjAwNDY2MH0.h2r5HZQIXvtiHCZb8LaWbz6j2TU2s2yAPw4f65hJox8; tt_ticket_guard_client_data=eyJ0dC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwidHQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJ0dC10aWNrZXQtZ3VhcmQtcHVibGljLWtleSI6IkJORm9BSXkzdzdLYTJZaDBLdVRwK2pNVFBoVlkvTnlsMjh5UWlKYy9XRjVxMjBJWVAvQnJqZU5ySk9FbEJDZjhmeXI0eGUvOGhHU0RNK2p3bGgxakxBYz0iLCJ0dC10aWNrZXQtZ3VhcmQtd2ViLXZlcnNpb24iOjF9; bm_sz=FD067C1C43526E693E3B29798963379F~YAAQa4M0F5kVOY6VAQAA6+yglxu/hqChsZw/Ow8gAzwPkJkBf7kBG9rxeoWinzzXjCwm+GW46FqzhEUWEBBMj2SiwFnS9plQyj1dq069Qncw8jA7XLscShuJBFcF9BTzhsE/6YLPxpuFHPtcgboRCdIOFWVAFAaohLrgbv8V1Pn5OWtg/wmLwUB/Knes0N4IozxOu7W3Q+8kVly6NeVqnasKDawst+F+J54bkSRledbpI8ypNhdgv6sDFlS6yPddt4VhN8Wc/b3XWDaJhDx9XdfhVKgaliitKkinfAdBRmraDx3sQAnAd97YvuRmZ0K4XOZFNRGP2ipMuTWGnXxwl/nkOBLEV/VWjfLetAeLfvUB0na3/ENQKvQ=~4469559~3421491; _ga_BZBQ2QHQSP=GS1.1.1742005661.535.0.1742005661.0.0.1212300895; _abck=7AEF582E5E64A2B0028CE06961EB5E61~0~YAAQXgIKciuYd5SVAQAAPT+nlw1vUJkcgS90VoGszsy43yT/UyXcbhWNqBJsv5YcxlkPh9syDoj4pdcHpjGacv4DVwhqIy0VV5lmx07u1LKqSAtpCRb2OWQ1V0bl0E1FrO1FcqzHGu4NUfTRGcB03K8BLjdVUsPF+7xz1FWmMiytLO0E+f51RPxKfVkEhVeUEkUjf9+tgf9WC9cp4q8LBWZ3E+NE2DyRYEOqHFz3NbfC+DviuP/awVzn6hsvLcwUTWcEmtQi5ZOvob7z651fr5X4Whr52URHkXY9/32EaMTa0W3QAYxpEDn26h3simwiHMWk15GLZCuVG8fV0Hy/I/vQrIrxRHe42LR7HDav0Btb9vi4sK9FqH7BgIiK6h72WUUXRDLgSJW1VMhiOz5oN59ZtAGUIkDgPg7R2LtjOpMLCkZKA/mawemY3a4PNtgT+PIx0uCCMUwucN/wP+nQkDxqnW5xcYDjJAJPclbAFuWCXKbgCmUmlhgDS+OZif0SEzC78NGV9yV3v0n2t6nGmPytXQtFrraERP2+KZz5GO5MrnAUYzrv/71e6WrXGgPZZaE9tsJMcxt2OX7agGDzJQC0KDrW3EQlI2ei877VWDL4U7p7bKa4o9WyRr5nxONu9zcc4eS3yh8N+vb3ujySEWvUVgfWDC7GMytH3xfrCmbDfY7ga/IbRhq/jtR570T4PZOSPKgvxwKBEXoty2Fbd9PenDtMSAt0oEIxa8RKA1ga6HUD~-1~-1~-1; _ga=GA1.2.4230394.1649834302; ISID=%7B%22seller.tokopedia.com%22%3A%22c2VsbGVyLnRva29wZWRpYS5jb20%3D.85c4247e3e7a44917b74c56470ccaeb5.1742009656263.1742009656263.1742009656263.1%22%2C%22www.tokopedia.com%22%3A%22d3d3LnRva29wZWRpYS5jb20%3D.8f670d018b2e9472998b05c3d1974059.1715927789215.1715927789215.1740408829395.12%22%7D; _dc_gtm_UA-126956641-6=1; _dc_gtm_UA-9801603-1=1; _ga_70947XW48P=GS1.1.1742009656.4989.1.1742009660.56.0.0"
    },
    "katniss": {
        "mapping": katniss_mapping, 
        "warehouse_id": "7800575", 
        "shop_id": "7593019",
        "cookie": "_SID_Tokopedia_=dFEy6oYPsJoJDe-kpih7MhQRlv_6FByI_J0PfD2OZlvLHUwT7X20xJlYYDCfbwwgMNo29M1DouMnmQabLhPHYtOmp_OGxrsZ17ObEGkCNwjEiuMIELE9MA0htK-t1mes; _UUID_CAS_=e41678f3-6f34-4fc3-bd16-29354a3fbdc5; l=1; aus=1; d_ticket=ca950e6255c6e2e2139f942b4cf323597e0e5; _UUID_NONLOGIN_=8bd0bc0983fa7e3950970405c7eb3d9e; _UUID_NONLOGIN_.sig=_YhaFjBS2lRlOQIOFdVQlPJ5u_g; tuid=86247457; DID_JS=ZWU4MzM1N2UzNmY1ZWU2MDNhYjgwMzlmYTFiOTdlNjgyYzg0ODY4NWE1OTg0ZmEzNWQwODk2YjVjMmJiZGM5NjQyM2I0ZjNjNDc0MjliNWVhOGFlNDQ4YTFiYmM4MjM547DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU=; _CASE_=7e27614c61273f37373d352927644c61273f3435353d3d353d353c2927696769273f27577068646d25446b60696425566075716c606b6c255f70696e6c63696c272927664c61273f3432332927696a6b62273f273435332b3d3436373d3337272927696471273f2728332b343c3c37323c32353535353535353427292775466a273f273435373635272927724c61273f343631353636323d2927764c61273f3434303635303236292776517c7560273f27376d272927726d76273f275e7e5927726477606d6a7076605a6c6159273f343631353636323d295927766077736c66605a717c756059273f5927376d59272959275a5a717c75606b64686059273f5927526477606d6a707660765927785827292769507561273f27373537312835372834325134333f30323f37372e35323f35352778; _m4b_theme_=new; _fbp=fb.1.1714199581860.14608332; SHOP_ID=7151798086795329798; _ga_W44EJN0C49=GS1.1.1717927239.1.1.1717927476.0.0.0; _tt_enable_cookie=1; gec_id=370430007178182336; _ttp=6E0XmEcTLaFng_JKQ6y6wL4PKyi.tt.1; _uetvid=bbef5cf02d6211ef95e6dd5334b449f5; DID=fdb9277ac126ffc1cde7cba2fbb2d5120f9143a69d5c7c82b9ff3d415c731cca822e6f36f88cf71c4f4025ef25720937; passport_csrf_token=ef37172a623cae3cc2dfc49c45e27d78; passport_csrf_token_default=ef37172a623cae3cc2dfc49c45e27d78; odin_tt=11760018fa25787581f69ffd3c48a81fc3f92b84513d08e64190d897fa07569471e0f2d5a7cc755bb438b144098f0ea54c1204155e95279ef73ed49abbf7ca73; sid_guard=d3e1e6a59c5eabaa5387c0dd73d37945%7C1738740241%7C5184000%7CSun%2C+06-Apr-2025+07%3A24%3A01+GMT; uid_tt=6846865b8774d132a5344c87da2ecc4a679c8a40877e8d50b80b48d20331adfd; uid_tt_ss=6846865b8774d132a5344c87da2ecc4a679c8a40877e8d50b80b48d20331adfd; sid_tt=d3e1e6a59c5eabaa5387c0dd73d37945; sessionid=d3e1e6a59c5eabaa5387c0dd73d37945; sessionid_ss=d3e1e6a59c5eabaa5387c0dd73d37945; sid_ucp_v1=1.0.0-KGMwYTkxYWFjYTliYzRjZjNiN2Q5OGQzODk0MGI2ZWJmMzAwMGYxZWYKFQiBiJSchqaNkGMQkaSMvQYY5B8gDBADGgNzZzEiIGQzZTFlNmE1OWM1ZWFiYWE1Mzg3YzBkZDczZDM3OTQ1; ssid_ucp_v1=1.0.0-KGMwYTkxYWFjYTliYzRjZjNiN2Q5OGQzODk0MGI2ZWJmMzAwMGYxZWYKFQiBiJSchqaNkGMQkaSMvQYY5B8gDBADGgNzZzEiIGQzZTFlNmE1OWM1ZWFiYWE1Mzg3YzBkZDczZDM3OTQ1; tt_ticket_guard_client_web_domain=2; _gcl_au=1.1.590588929.1739698171; NR_SID=NRm85tatcyt4srs; webauthn-session=d61b811c-984e-46bb-b3d1-786ef661babd; ttwid=1%7Cn53irPMuvl1mmH24zpXm1f04JmJnpGkGqrtcQ4gKCys%7C1742038327%7C4765d2fde798061de12745dfda704202d062e7f1289036c8e4dc82915126ff06; tt_ticket_guard_client_data=eyJ0dC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwidHQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJ0dC10aWNrZXQtZ3VhcmQtcHVibGljLWtleSI6IkJET3I2ZWg1VmhNM2phaSt2YUR1M1BJRkkwL205dTNwV1BIdnlkb1lQK0Q3RnhkeWd0eWJCaU84K0pIQVkzMU85UEhpNjNJWjQyc3YyeFJMQ0FhbXozOD0iLCJ0dC10aWNrZXQtZ3VhcmQtd2ViLXZlcnNpb24iOjF9; _ga_BZBQ2QHQSP=GS1.1.1742038332.266.1.1742038398.0.0.544409451; _abck=F365B3D50C17D434D8FDF036D27D033B~0~YAAQvgMKcuJpb4mVAQAAvubHmQ0eDjK+jwzf8X/z1dFckiiRszyFSZzq1kRYBdBsAzAghPMjuhhnzkX12TxLWQd/Re5ka92wOAbhtD2GptZCTWLVuLA6QdftgB19CGwKifTt8FPEgHCW83l6kRmqXAq575e+HwviEGrbAWEKG6gFe8nZMo8hcx3ofJveQpZPFzkewKXYTzZb+sNagg0mkiXmQBbru4qKNwDknMwp8aNJMg/+A4QYQn5TPTAGvhensuuXuI5kNuTJn3bHdIc0l/KTlJCIDIiU2U43hQCy5H+pLLlmMAcOiV6tGCXC/twB5xjF5o8lX2IvJFoavCj1280dlBi2ZEscdCLe4xqK1bcL7FQ6TIiIKr7BGS3mehvPG9S+ktr0vDK7KltRbuN8JWV68HUFYqJLr2k6bCdC1Ae6T+yEIU4Y0Z2gp9C+FsnXAbAJhbrVRK5cz5NiYscQzAp4Dx3pQ5yaRqasdd0VBkjy6crDEaDCyU8qcT0pEMDYGG7ENF2WTmqT0t70rlRBj+EZvgmDYimAxlL4Ip/teydJ+M6OILSzY/gzEXWqwfDQbRw5aoGneqZ5xqL/xLTuq+8TID9/b5O51p47sSQehcY93zb2odNfvBvVObPyWrca6hcMuQ126Nu9S6CXc54TRRzyFA5i+DLOTVpPZfBXqsFzbm8MXEqUCc/JUaJLHdbAU8hWPzYD7/xJfnZFauEXSbMXYB3mOGQH7zIwcvZsb7UQDAKh4QEyfeti/apOHfo=~-1~-1~-1; _gid=GA1.2.180253002.1742041771; ISID=%7B%22seller.tokopedia.com%22%3A%22c2VsbGVyLnRva29wZWRpYS5jb20%3D.803f0747f9bf04aa1bf3f52415ac554c.1742050033045.1742050033045.1742055728029.3%22%2C%22ta.tokopedia.com%22%3A%22dGEudG9rb3BlZGlhLmNvbQ%3D%3D.88c4daa8ca38b40bb8f9defb833d1869.1708163833829.1708163833829.1708163835466.1%22%2C%22www.tokopedia.com%22%3A%22d3d3LnRva29wZWRpYS5jb20%3D.8e43332919e3f40fcade7d7fb248aa71.1708163838539.1708163838539.1741785166415.45%22%7D; uidh=KDQPGcdjIr3kXQ9RQBlCRQlKCzW4hDk2Fu75GoQusng=; uide=EC6+BOa2VFpEegjoQ4jyr9knG4Uno8AubvGl8rLH4u8PSskc; bm_sz=C992038EBB1C0EAE9FC568C20119222C~YAAQ1czbF4zhWY+VAQAA++ScmhtdD7ehFH3RfyyBApIjhok6soa6Tf+iSd5v5kpwmxuAdOeruk8DcTbgsMzJ7OeifZ9dxMmaur5TQE4HX0xfS4zV4YhZQuuGPz5cK1UJle0HDIvq45o+i4e5WcyJROB3fEzengdWIIiFYUKnxNXXPIgnHRPxfAQY+OfYcLnoKmdPseFl7gSh7QOpSqJcCtwyXaD8udNUDI+PVNKE7hM9Id4PaCpT+ZCPnEFhoz9kcWM9TjS8hQfhqNN2bbbDDZ1sjBGtXFqdZKlUC5+EFKnSo33cbG67hflRxea9928tLQ893jNZKhlJkmT38qtFD4xRZpcQ/OMuAs0VEWLJoGOxzjW3KGqIBexnGF5QgPva1URXQVYZLLlXVePaX6vlNlc=~3355191~3555891; _ga=GA1.2.1769629206.1651639407; _ga_70947XW48P=GS1.1.1742055728.844.1.1742055766.22.0.0"
    },
    "tourisme": {
        "mapping": tourisme_mapping, 
        "warehouse_id": "8900810", 
        "shop_id": "8743858",
        "cookie": "DID_JS=ZjQ3N2U5N2FkZWI2NTE5Zjg4MTRlMjVhNmYyZTRiYjhlNjFkZDFiODllOWY3ZjhjMzQ4MDMwNDU0NmZlZTdhZmFjMmIyNTAwMjE3YWJiYWRmZWQ0N2UyOTdkODQyODUw47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU=; tuid=104831330; _SID_Tokopedia_=e790xrzFzIqQh2mkXM-QqSJGIQVJprXuzR8s_D5c7M9iDaVSy8eslORhKXagYPJ0Gmtuv8zLp5wlEEY2p0Ljle0duDhmCrC9N9tYAEeIk9Zj-kljlz1euL_BJ5TF8IIe; _UUID_CAS_=31f6490d-e0e3-4821-a78c-796f4cc2f7c6; l=1; aus=1; _CASE_=2d74321f32746c646463607a74371f32746c67676264636f6463607a743a343a746c7404233b373e76021903041f051b191910101f151f171a0502190413747a74351f32746c6761627a743a393831746c746766607861606e616e636e6e6f63626f6462747a743a3722746c747b60786466626f676665606e62636f6f6161747a74261539746c746767636366747a74211f32746c67646467666561637a74251f32746c67676365666361657a7425022f2633746c74643e747a74213e25746c740d2d0a74213724333e39232533093f320a746c67646467666561637a0a74253324203f353309222f26330a746c0a74643e0a747a0a740909222f263338373b330a746c0a74013724333e39232533250a742b7a2d0a74213724333e39232533093f320a746c667a0a74253324203f353309222f26330a746c0a7467633b0a747a0a740909222f263338373b330a746c0a74013724333e39232533250a742b0b742b; gec_id=450247133946199744; _tt_enable_cookie=1; SHOP_ID=7189625483531649285; d_ticket=b1aa8fa7d164e36bf435709d7f3a1d8f7c042; _ttp=v-kY2iYpsp2IJ5Xma_tt2KTpCT-.tt.1; _uetvid=1311be503df511efaff1a7ba9b148daa; _gcl_au=1.1.991235373.1736057777; passport_csrf_token=04d238edc0669bac0520b232113f5f08; passport_csrf_token_default=04d238edc0669bac0520b232113f5f08; odin_tt=dfa05b86cd1fbc0ede0e1e9a5c7e9c15658e6ccd2bad70f3a5ccfa96f30a31dbba142989454d4bbaf4a5838fa2b3cf359579c27dd4c24e535083e5a5b78198ce; sid_guard=76fbb52d5529879ce2696e1d9a3d92d1%7C1737905106%7C5184000%7CThu%2C+27-Mar-2025+15%3A25%3A06+GMT; uid_tt=7ff5bdb40b453a0f1e799547dfde42488d1dd9df7fb9e1055d20e0eb9f10afc1; uid_tt_ss=7ff5bdb40b453a0f1e799547dfde42488d1dd9df7fb9e1055d20e0eb9f10afc1; sid_tt=76fbb52d5529879ce2696e1d9a3d92d1; sessionid=76fbb52d5529879ce2696e1d9a3d92d1; sessionid_ss=76fbb52d5529879ce2696e1d9a3d92d1; sid_ucp_v1=1.0.0-KDJkYjNiMzBiNjVkNWE3Yzg0MzU0MjZmMmVmNjFjOGU2ZWE5ZDUwZjAKFQiGiNncpa-r42MQ0qfZvAYY5B8gDBADGgNzZzEiIDc2ZmJiNTJkNTUyOTg3OWNlMjY5NmUxZDlhM2Q5MmQx; ssid_ucp_v1=1.0.0-KDJkYjNiMzBiNjVkNWE3Yzg0MzU0MjZmMmVmNjFjOGU2ZWE5ZDUwZjAKFQiGiNncpa-r42MQ0qfZvAYY5B8gDBADGgNzZzEiIDc2ZmJiNTJkNTUyOTg3OWNlMjY5NmUxZDlhM2Q5MmQx; _m4b_theme_=new; tt_ticket_guard_client_web_domain=2; ttwid=1%7CzLhnlJWELvhKcYA1cKA9O2mujJMaJU224J-5U9jhqmA%7C1741710504%7Cd1ba56aa7699a4fd0b00dc94c40f09664118b70b47eea4966348b6e7d57e7aa7; tt_ticket_guard_client_data=eyJ0dC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwidHQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJ0dC10aWNrZXQtZ3VhcmQtcHVibGljLWtleSI6IkJISk9JZDF6UFNsQW5YejY3M1dqM2hSOVNZdGZPTG1DTnAzK245U3VGaWt1TlFPV0I4TnloVnBRUVp4R214c3JsRVFLRlpDN3hOQ2QxRVROdzZRNjgvQT0iLCJ0dC10aWNrZXQtZ3VhcmQtd2ViLXZlcnNpb24iOjF9; _ga_BZBQ2QHQSP=GS1.1.1741710511.180.1.1741711266.0.0.2076149234; _gid=GA1.2.1031538694.1742212766; DID=ac2c85874e0660e1819e2bb6472d5f5cbd754672002c18ff09f67cea8a1f1a996f80e81bb1026b7b6252f09d6a19fb06; _dc_gtm_UA-126956641-6=1; _dc_gtm_UA-9801603-1=1; uidh=zQwPFOkuBDPpSANeR2uB11pt0agvJLmzJA3djIROHpc=; uide=2y2CV0JuG+Q0NML6NGy5awtxycGcAf6spv1Z4NwO8O/juJgvvA==; bm_sz=C3EE328E11C361D5C180F90800AC6B28~YAAQdgIKcqRBSqOVAQAAVPP3phvBZdkAXfTNRF5fxUm60KS1spD4pv6zhOIhxe6YsMS/rFoVYGn2fV0b6LBiovLu0qkxue4bkMznvhuSIBAVXeELAYMMFT4wCEOnVdE0bwEl7rgN522y0fyb2RFLhYALQFC0r2afrgv1PVbezh0t/MQ0Edw+9rqkazpi8yS/Fli8vForUOoJSHBMgf76jL0lzyWtde8hLdgxyUmKTHZGlMXMO5PSxbtaVIxdAL5MxP7k8l3cF0Si3TmA/2Bchlyc9O9nwU3uBHIHRE1vfaM2/6OY05nOAHYVO9kbzMi5RSakEvvakhO6IuwygVTl104lu4pm0v3LLEj/azdSeaYlUs0UbivBdQDSqMwLbwoXdoT6t/DQSFJgypwYImhq4mMdQ1r4~3748932~3622200; _abck=5FC89944352A06B40C2C42658CDD3FD0~0~YAAQdgIKcqVBSqOVAQAAyPP3pg3I0U/fBWvWo10s4KKc+P+KaoXIT22mhxPzmfOzsUtCh3bs52qZksS7QJkm5So44LcVswniw3IexXbcsPa/8pDp8zAM46xttAeWe91xIPAAQix9s6qcD2YBHESvZ4/wqxrsfpD9JHCrAKIdtHt1lxi9raRNh7OyE/b25slRyiHdmqE0oD6GVGruVqrydAQznKugMGEGQ+g9zn14enzAKkuDV77Zv815VpsTNjOsmovjWpoo728XB7f3/PjU1y/BplezAPjZQVBspgOYKgFFLACCMWVUTA6CL92wsso1lHkZqiGTJlGuAdc53eq0iN6sFmFnoXpM0eEMAP+7Egeov2yFzUVwjcBqInpGyjWiR1KR5zzFavfUw397HmJWic2IrM6+p7LxRhdgJGd9vlnrTcglBADrf2oNgH35dMoiEJ1N5sGIk3dklQHRMczee/d7MykcaSt1po2RprOOSFxNnbFZXWjZC5f3zzrNPURcmEsVCfLYoFnMW1dGxlWap2TBFuinbl6PupU0ntBhUvpphMHagJVrZRWlEgpMo17de3azcmZgNNZcf+Fnp+qEkqMUMyvxAO9dVnLe/LxRrBrGdE6IO3qmI7rhLKVmUK1aGvNqty/PC/VNpmD/J3htiCLds4o8UjTRqysY98izCTkWBfmyFe4hKQ0LBtVtp46qknCi0IXVbvZiO6r4NRDb3JpiGeR4Tbo=~-1~-1~-1; _gat_gtag_UA_9801603_1=1; ISID=%7B%22seller.tokopedia.com%22%3A%22c2VsbGVyLnRva29wZWRpYS5jb20%3D.823020bce45f1499cb11ccaeaa9fab5a.1740194548589.1740194548589.1742263025824.8%22%2C%22www.tokopedia.com%22%3A%22d3d3LnRva29wZWRpYS5jb20%3D.8ea8d78fe27c14c9ab0d9a81c4951f52.1732404906972.1732404906972.1739605394138.2%22%7D; _ga_70947XW48P=GS1.1.1742262727.723.1.1742263025.47.0.0; _ga=GA1.1.851956992.1651744251"
    },
    "babe": {
        "mapping": babe_mapping, 
        "warehouse_id": "10245084",
        "shop_id": "10178952",
        "cookie": "d_ticket=ac655481d0e24a1133473d8dfb6e7c2753777; _m4b_theme_=new; SHOP_ID=7189527783645675781; _tt_enable_cookie=1; _clck=fnufje%7C2%7Cfni%7C0%7C1658; _UUID_NONLOGIN_=e26d4bb64788a4afbac049b50d9b3717; DID=07dc5116ec6cb28d441b2281f35419d11fac34780014748b35d94170ef186a7f669d30a80069be684760c20e2175e59e; DID_JS=MDdkYzUxMTZlYzZjYjI4ZDQ0MWIyMjgxZjM1NDE5ZDExZmFjMzQ3ODAwMTQ3NDhiMzVkOTQxNzBlZjE4NmE3ZjY2OWQzMGE4MDA2OWJlNjg0NzYwYzIwZTIxNzVlNTll47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU=; uidh=d8s30GxMgCR/jWtvKVC/2wNTCd2/xhO1KFZC1jpG00I=; _SID_Tokopedia_=IT-7bwOWFLTlQikSBroi6kaZ9c_Wlr_lImGS9_78XGuwsykkh-3yIfJHOevls5uSm1OhWQbT8fkQMNXwTzyEFjYkXEWq3Xcp5XO0oR2NzCI3lZW5Kh6m7bgvHvibexaj; l=1; FPF=1; tuid=107500537; gec_id=461711290717454016; uide=Qi7WYYgQE6FiF3Y8+06hslqcdPLMFdA0DxyCbZvlhrOs2Kcvtg==; aus=1; _CASE_=71286b436e2830283b3b3c3e33393c3d3b28262869436e28303b3d3c26286e436e28303838323a2628665f7a6e283028383a383e273b3b273b3e5e3b3b303939303939213a3d303a3a282628666b7e283028273c243b3333383d333d3a3a3a3a3a3a3a3b282628666866283028587f676b622a6b7e63616b2826286665646d2830283b3a3c24323b3938323c382826287a49652830283b3a38393a28262879436e28303b3b3f393a3f3d392628795e737a6f2830286565692826287d436e28303a26287d627928302851572826287d62797928302851572877; _UUID_CAS_=420c11f2-c9a7-4644-893c-8939a4a49a43; _ttp=PqMy-zWzar4Q7tOGEX9i3z9JTTG.tt.1; _uetvid=69d65ee02d4a11efaef117759a8c125b; _gcl_au=1.1.1734389779.1737789864; passport_csrf_token=994a6e76ec9b034e60c8e0ed4f3e001c; passport_csrf_token_default=994a6e76ec9b034e60c8e0ed4f3e001c; sid_guard=00d587b4088ee2690eb0bdd2b2f4f55c%7C1738510135%7C5184000%7CThu%2C+03-Apr-2025+15%3A28%3A55+GMT; uid_tt=1b6001261cc947d18ea5278d38184320c70969c2ce1fc8f8619d8120efe7b456; uid_tt_ss=1b6001261cc947d18ea5278d38184320c70969c2ce1fc8f8619d8120efe7b456; sid_tt=00d587b4088ee2690eb0bdd2b2f4f55c; sessionid=00d587b4088ee2690eb0bdd2b2f4f55c; sessionid_ss=00d587b4088ee2690eb0bdd2b2f4f55c; sid_ucp_v1=1.0.0-KDA1ZDMyODUzNDdmNGZiN2JmZWRiN2RmNWY4ZWM5MmJiZWE5Nzk2ZjgKFQiFiIiYufmt0WMQt57-vAYY5B8gDBADGgNzZzEiIDAwZDU4N2I0MDg4ZWUyNjkwZWIwYmRkMmIyZjRmNTVj; ssid_ucp_v1=1.0.0-KDA1ZDMyODUzNDdmNGZiN2JmZWRiN2RmNWY4ZWM5MmJiZWE5Nzk2ZjgKFQiFiIiYufmt0WMQt57-vAYY5B8gDBADGgNzZzEiIDAwZDU4N2I0MDg4ZWUyNjkwZWIwYmRkMmIyZjRmNTVj; tt_ticket_guard_client_web_domain=2; odin_tt=b5374b3dab76fb8d66005d5bc50b18afce05bc7ab2831632786713c68c21bdf8f5734594a985d625ce356840102f4e496a7fee6852bbf821ddbb1c2e50dfaf55; SELLER_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJVc2VySWQiOjcxNzk1MDI4NDA5NTQ2MTg4ODUsIk9lY1VpZCI6NzQ5NDg3MTE2NTIyMzAxMzMyMywiT2VjU2hvcElkIjo3NDk0ODcxMTY1MjIzMDEzMzIzLCJTaG9wUmVnaW9uIjoiIiwiR2xvYmFsU2VsbGVySWQiOjc0OTQ4NzExNjUyMjMwMTMzMjMsIlNlbGxlcklkIjo3NDk0ODcxMTY1MjIzMDEzMzIzLCJleHAiOjE3NDI0NDE1NzksIm5iZiI6MTc0MjM1NDE3OX0.nuXcsOBzPxViQTxqghkZmi-QCN6Rkgdn-upVV_4V9p0; ttwid=1%7CXAGBZW3DDBf8N3uNBxnXfMa_vDi5e-xRO88PB96msgQ%7C1742355181%7Cd28a87daeca5f20f1e965a59bb3037ff7db8aa4dd439c4aa09df6a7ed3cf422a; tt_ticket_guard_client_data=eyJ0dC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwidHQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJ0dC10aWNrZXQtZ3VhcmQtcHVibGljLWtleSI6IkJJY0FPM2hxQXRRSnBPL1ovSWZwUHh6eFdRaGRjRkpNdXRvL3MvUzVhSXR1dnU0Y1NQMjBXV2pwSElUWmZSTzZ3NWtWcjNHNGdsc0s4bTF4NnBjV3RYcz0iLCJ0dC10aWNrZXQtZ3VhcmQtd2ViLXZlcnNpb24iOjF9; bm_sz=7946BEF11A6FDF5D5C3B06B92EAACAB3~YAAQdgIKciRPcqqVAQAA5D52rBuxBHey9cJlJ08OjyMcCQ+o6C/oXNd+t1mqyodk2XqTHxyyqfLVOzgbQd2nc5Qs1/n98vWgwz75s0s1xRIgn5IhfXlDs4HDg3MxsJRcG6Ne4yLHuZIi53/USCF97VbwlCYk+kqNJemxLlY3Rzh1aiCcPZEGWNheg7KTxxarwQ75QKZfrGBPYJgEsQTw8WRnHskuwnTAewNGimBCVuGDvcx4K5NCHruDGvVgmWURP6RTfJPqG7vV6E2myOMFcPndPtc75SsUqxjrcqm3TuYiX+XipQR28ynDlkiOGJA4oMySyrwLUyPq1CYFFNT4YylppJgBP1mJFpWo3aJY7Jpz+LymM2PH~4535365~3223864; _gid=GA1.2.999165452.1742355186; _abck=1CEBDAD3B7781E5A1662BD04E8577D54~0~YAAQdgIKcjVPcqqVAQAA+D92rA3jEzc17F1hIyyKQpW/Dj7y5pP8BmQcut8dCq1cRA60uaCuxmXFDDyNVmRCyNIWfKNCu4cQCgBVgOhEdDcDYMYeqX4RGm9UWljyJk3uKGr580wJj3di9XAbfItPHXdr/m8JPgmj4iCwxeE1CTH0/VLHcFtkjfW868kOvJnOpF9BAlvK62UWOIQwbiO5os66OF9NVzoKGLW1D9XBBDPPTXmc0ipF7JTdATkzb/3Xbb+N+KPUmM1mX6bynZ4uG76xcrU8FL0/e8uicy0M/H+NRTvE2qpy6GqddodZRiGDG7NQgbdZHG47MwpMD9FlTAh9yaucNDBAnie0F/o5YmPmsL5eeowyr8a+/l31x2D5ro5S1d79wWQpQ1Aaou/Vi5NKI9VQiJE8hO+WBejRhy4CwRL4Gvwb3RGM++3pVoUHHfeSWdWHHxEK0DtOl5Z7xuS/NuGyRBCFwHrZmAlNUd8AgZNkLgz5F+F7dHeKRdM3thBFlEvm0SDfyqSznJXgnfjlYYPimL4xQ49Ooeo1I+qUTLgR21Fykch/Fr3sMsxn0jnHrQ/A+Hrhi+qdjcDrs+Mmg/aMPq+99QaCc1YO4zng7LfSAwS9lKIe/a4sVf5v3alx8ifqDjdh/eKaYeY09GtfehOIVlAsfrd37l+fbH6X9nEPv3n+HfxQVJxpfrUv5KbeEBr8tEG1ET+cbKs8jBFZs/A5tAi5v+De4WU2U4BidkRJyXwpPpBPpUDWFt8=~-1~-1~-1; _ga_BZBQ2QHQSP=GS1.1.1742355179.557.1.1742355198.0.0.1244406690; ISID=%7B%22www.tokopedia.com%22%3A%22d3d3LnRva29wZWRpYS5jb20%3D.83fcf470bf9234ded890e26152c03f9e.1729913650352.1729913650352.1731821971499.5%22%2C%22seller.tokopedia.com%22%3A%22c2VsbGVyLnRva29wZWRpYS5jb20%3D.87db673af179644229c51d9a30271fe8.1741745772019.1741745772019.1742355220615.4%22%7D; _ga_70947XW48P=GS1.1.1742355186.98.1.1742355220.26.0.0; _ga=GA1.1.1469454711.1718177425"
    },
}

# Argument parser untuk command line
parser = argparse.ArgumentParser(description="Proses SKU berdasarkan kelompok")
parser.add_argument("--group", type=str, required=True, choices=SKU_GROUPS.keys(), help="Pilih kelompok SKU: jaknet, eldas, bestever, katniss")
parser.add_argument("--count", type=int, default=50, help="Jumlah SKU yang diproses (default: 50)")

args = parser.parse_args()
group_name = args.group
count_sku = args.count

# Ambil data berdasarkan kelompok yang dipilih
group_data = SKU_GROUPS[group_name]
sku_dict = group_data["mapping"][0]  # Ambil dictionary dari dalam list
warehouse_id = group_data["warehouse_id"]
shop_id = group_data["shop_id"]
cookie_value = group_data["cookie"]


def update_stock(sku):

    # Inisialisasi productWarehouse
    productWarehouse = []
    skuID = ""

    # Loop melalui 2 SKU pertama dari daftar SKU
    for product_desc in sku[:count_sku]:
        skuID = product_desc["SKU"]
        productID = sku_dict.get(skuID)
        stockID = int(product_desc["Gudang online"]) + int(product_desc["Toko Jakarta Pusat"])
        # price = hitung_harga(int(product_id["Price"]))

        if productID is None:  # Jika SKU tidak ditemukan, lewati iterasi ini
            # print("skip", end=" ")
            continue
          
        productWarehouse.append({
            "productID": str(productID),  # Pastikan productID dalam format string
            "warehouseID": warehouse_id,
            "stock": str(stockID),
            # "price": str(price)
        })
    return productWarehouse, product_desc

def hit_stock(data):
    
    url = "https://gql.tokopedia.com/graphql/IMSUpdateProductWarehouse"

    payload = json.dumps([
      {
        "operationName": "IMSUpdateProductWarehouse",
        "variables": {
          "input": {
            "shopID": shop_id,
            "productWarehouse": data
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
      'Cookie': cookie_value
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response

def validation(response, data, product_desc):
    json_response = json.loads(response.text)
    validation = json_response[0]["data"]["IMSUpdateProductWarehouse"]["header"]["error_code"]

    if validation:
        print(f"Error msg: {validation}\n")
        print(f"{response.text}\n")
        
        if validation == "ERROR_VALIDATION":

            for bit in data:
                response_x = hit_stock(bit)
                json_response_x = json.loads(response_x.text)
                validation_x = json_response_x[0]["data"]["IMSUpdateProductWarehouse"]["header"]["error_code"]

                if validation_x:
                    skuID = product_desc["SKU"]
                    productID = sku_dict.get(skuID)

                    if skuID in sku_dict:
                        del sku_dict[skuID]
                        print(f"SKU '{skuID}' berhasil dihapus.")
                    else:
                        print(f"SKU '{skuID}' tidak ditemukan dalam mapping.")

                    file_py_path = "sku_product_mapping.py"

                    with open(file_py_path, "w") as f:
                        f.write("sku_product_mapping = [\n")
                        f.write("    {\n")
                        for sku, product_id in sku_dict.items():
                            f.write(f"        '{sku}': {product_id},\n")
                        f.write("    }\n")
                        f.write("]\n")

                    print(f"File '{file_py_path}' telah diperbarui.")
                    print(f"Deleted ProductID: {productID}")
    

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
        D2 = B2 + (B2 * 0.40)
    elif B2 < 70000:
        D2 = B2 + (B2 * 0.30)
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
    E2 = D2 * 0.14 + D2

    # Menghitung F2 dengan ROUNDUP ke ratusan terdekat
    F2 = math.ceil(E2 / 100) * 100

    return F2

def split_dict(lst, chunk_size=count_sku):
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

batches = split_dict(dataSKU, count_sku)
jumlahSKU = len(batches)

print(f"Jumlah Perulangan: {jumlahSKU}")

i = 1
for j in range(jumlahSKU):
    try:
        data, data2 = update_stock(batches[j])
        
        if data:
          responds = hit_stock(data)
          validation(responds, data, data2)
        if (i <= jumlahSKU):
            update_progress((i / jumlahSKU))
            i+=1
    except Exception as e:
        print(f"Error for sku : {e}")
        