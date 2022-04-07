import csv
import time
import pickle
from collections import defaultdict
import requests
import pprint
import json

# Speicher: Datenbank
def save_data(data, data_str):
    with open("./data/{0}.pickle".format(data_str), "wb") as handle:
        pickle.dump(data, handle)

# Laden: Datenbank
def load_data(data_str):
    with open("./data/{0}.pickle".format(data_str), "rb") as handle:
        data = pickle.load(handle)
    return data

test = load_data("stockdata_dict")

# esg_rating_dict = {
#     "AAA": 0,
#     "AA": 1,
#     "A": 2,
#     "BBB": 3,
#     "BB": 4,
#     "B": 5,
#     "CCC": 6,
#     "CC": 7,
#     "C": 8,
#     "DDD": 9,
#     "DD": 10,
#     "D": 11,
#     "EEE": 12,
#     "EE": 13,
#     "E": 14,
#     "FFF": 15,
#     "FF": 16,
#     "F": 17
# }
#
# save_data(esg_rating_dict, "esg_rating_dict")