import requests
import json
import pprint

url = "https://yfapi.net/v11/finance/quoteSummary/AAPL?modules=defaultKeyStatistics%2CassetProfile"

querystring = {"symbols":"AAPL", "modules":"defaultKeyStatistics"}

headers = {
    'x-api-key': "ZFlFVu4kow49xkiNSz5mdaSu6DpkJSeg2fMTSmuk"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)

d_test = json.loads(response.text)
print(d_test["quoteSummary"])
pprint.pprint(d_test)