import requests
import pprint

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key

url = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=IBM&apikey=demo'
r = requests.get(url)
data = r.json()

pprint.pprint(data)