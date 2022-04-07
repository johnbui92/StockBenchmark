import time
import requests
import pprint
import pickle
import statistics
from collections import defaultdict

# Laden: Datenbank
def load_data(data_str):
    with open("./data/{0}.pickle".format(data_str), "rb") as handle:
        data = pickle.load(handle)
    return data

test = load_data("stockdata_dict")

# url = "https://esg-environmental-social-governance-data.p.rapidapi.com/search"
# querystring = {"q": "ACGLO"}
# headers = {
#     "X-RapidAPI-Host": "esg-environmental-social-governance-data.p.rapidapi.com",
#     "X-RapidAPI-Key": "5e1447055fmshd217b6d846bbd7ap16f677jsn1e60f29bea63"
# }
# response = requests.request("GET", url, headers=headers, params=querystring)
# time.sleep(1)
# data = response.text
# print(data)

# url = "https://esg-environmental-social-governance-data.p.rapidapi.com/search"
# querystring = {"q":"AKYA"}
# headers = {
#     "X-RapidAPI-Host": "esg-environmental-social-governance-data.p.rapidapi.com",
#     "X-RapidAPI-Key": "5e1447055fmshd217b6d846bbd7ap16f677jsn1e60f29bea63"
# }
# response = requests.request("GET", url, headers=headers, params=querystring)
# data = response.text
# # data = data[1:-1]
# # data_list = data.split(",")
# # print(len(data_list))
# data = json.loads(data)
# print(data)

# def load_data(data_str):
#     with open("./data/{0}.pickle".format(data_str), "rb") as handle:
#         data = pickle.load(handle)
#     return data
# def save_data(data, data_str):
#     with open("./data/{0}.pickle".format(data_str), "wb") as handle:
#         pickle.dump(data, handle)
#
# a = load_data("stocklist_dict")
# asdsad





