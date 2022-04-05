import time
import requests
import pprint
import pickle
from collections import defaultdict

with open("./data/stocklist_dict.pickle", "rb") as handle:
    stocklist_dict = pickle.load(handle)

sector_dict = defaultdict(int)
for symbol in stocklist_dict:
    sector = stocklist_dict[symbol]["Sector"]
    sector_dict[sector] += 1
    # if sector == "":
    #     print(symbol + " | " + stocklist_dict[symbol]["Name"])

pprint.pprint(sector_dict)


industry_dict = defaultdict(int)
for symbol in stocklist_dict:
    industry = stocklist_dict[symbol]["Industry"]
    industry_dict[industry] += 1
    # if industry == "":
    #     print(symbol + " | " + stocklist_dict[symbol]["Name"])
pprint.pprint(industry_dict)