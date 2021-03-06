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

# CSV von NASDAQ in Dictionary umwandeln
def get_basic_nasdaq_info():
    stocklist_dict = defaultdict(int)

    with open('./data/nasdaq.csv', newline='', encoding="utf-8") as f:
        csvreader = csv.reader(f, delimiter=',', quotechar='"')

        for row in csvreader:
            if row[0] == "Symbol" or "^" in row[0]:
                continue
            stocklist_dict[row[0]] = {}

    return stocklist_dict

# Basic Infos von Alphantage zu stocklist_dict hinzufügen
def get_basic_alphavantage_info():
    stocklist_dict = load_data("stocklist_dict")
    failure_list = []
    counter = 0

    for symbol in stocklist_dict:
        counter += 1
        print("-" * 100)
        print(str(counter) + " " + symbol)

        url = 'https://www.alphavantage.co/query?function=OVERVIEW&symbol={0}&apikey=MGRYIUKL7JKXZH2V'.format(symbol)
        r = requests.get(url)
        data = r.json()
        time.sleep(0.2)
        print(data)

        if len(data) <= 1:
            print("Kein Treffer")
            failure_list.append(symbol)
            continue

        if len(data) > 3:
            sector = data["Sector"]
            industry = data["Industry"]
            asset_type = data["AssetType"]
            shares_outstanding = data["SharesOutstanding"]

            if len(sector) != 0 and len(industry) != 0 and asset_type == "Common Stock" and shares_outstanding != "0":
                stocklist_dict[symbol]["Name"] = data["Name"]
                stocklist_dict[symbol]["Address"] = data["Address"]
                stocklist_dict[symbol]["AssetType"] = data["AssetType"]
                stocklist_dict[symbol]["Currency"] = data["Currency"]
                stocklist_dict[symbol]["CountryShort"] = data["Country"]
                stocklist_dict[symbol]["Description"] = data["Description"]
                stocklist_dict[symbol]["Exchange"] = data["Exchange"]
                stocklist_dict[symbol]["Country"] = data["Country"]
                stocklist_dict[symbol]["Sector"] = data["Sector"]
                stocklist_dict[symbol]["Industry"] = data["Industry"]
                stocklist_dict[symbol]["SharesOutstanding"] = data["SharesOutstanding"]
            else:
                print("Kein Treffer")
                failure_list.append(symbol)
                continue

    return stocklist_dict

# Aktie in Kategorie "Marktkapitalisierung" einordnen
def marketcap_categorizer():
    stockdata_dict = load_data("stockdata_dict")
    stocklist_dict = load_data("stocklist_dict")
    stocklist_dict_temp = stocklist_dict.copy()

    for symbol in stockdata_dict:
        marketcap = float(stockdata_dict[symbol]["FinancialData"]["CompanyOverview"]["MarketCapitalization"])
        if marketcap <= 50000000:
            stocklist_dict_temp[symbol]["Size"] = "Nano-Cap"
        if marketcap > 50000000 and marketcap <= 300000000:
            stocklist_dict_temp[symbol]["Size"] = "Micro-Cap"
        if marketcap > 300000000 and marketcap <= 2000000000:
            stocklist_dict_temp[symbol]["Size"] = "Small-Cap"
        if marketcap > 2000000000 and marketcap <= 10000000000:
            stocklist_dict_temp[symbol]["Size"] = "Mid-Cap"
        if marketcap > 10000000000 and marketcap <= 200000000000:
            stocklist_dict_temp[symbol]["Size"] = "Large-Cap"
        if marketcap > 200000000000:
            stocklist_dict_temp[symbol]["Size"] = "Mega-Cap"

    stocklist_dict = stocklist_dict_temp
    return stocklist_dict

# Säubern: stocklist_dict von nicht benötigten und doppelten Eintragen bereinigen
def clean_stocklist_dict():
    stocklist_dict = load_data("stocklist_dict")
    stocklist_dict_temp = stocklist_dict.copy()
    deleted = []

    for symbol in stocklist_dict:
        # Ignoriere bereits gelöschte Einträge
        if symbol in deleted:
            continue
        print("-" * 100)
        print(symbol)
        # Einträge ohne Treffer löschen
        if stocklist_dict[symbol] == 0:
            del stocklist_dict_temp[symbol]
            print("delete: " + symbol)
            deleted.append(symbol)
            continue
        elif len(stocklist_dict[symbol]) <= 3:
            del stocklist_dict_temp[symbol]
            print("delete: " + symbol)
            deleted.append(symbol)
            continue

    for symbol in stocklist_dict:
        # Ignoriere bereits gelöschte Einträge
        if symbol in deleted:
            continue
        print("-" * 100)
        print(symbol)
        # Doppelte Einträge löschen
        current_symbol = symbol
        current_name = stocklist_dict[symbol]["Name"]
        for entry in stocklist_dict:
            # Ignoriere bereits gelöschte Einträge
            if entry in deleted:
                continue
            if entry != current_symbol:
                if entry == current_symbol or entry in current_symbol or current_symbol in entry:
                    if stocklist_dict[entry]["Name"] == stocklist_dict[current_symbol]["Name"]:
                        del stocklist_dict_temp[entry]
                        print("delete: " + entry)
                        print("Original: " + symbol)
                        deleted.append(entry)


        # if len(stocklist_dict[symbol]) > 3:
        #     name = stocklist_dict[symbol]["Name"]
        #     print(symbol + " | " + name)
        #
        #     sector = stocklist_dict[symbol]["Sector"]
        #     industry = stocklist_dict[symbol]["Industry"]
        #     asset_type = stocklist_dict[symbol]["AssetType"]
        #     shares_outstanding = stocklist_dict[symbol]["SharesOutstanding"]
        #     if len(sector) == 0:
        #         print("sector")
        #         print("delete: " + symbol + " | " + name)
        #         del stocklist_dict_temp[symbol]
        #     if len(industry) == 0:
        #         print("industry")
        #         print("delete: " + symbol + " | " + name)
        #         del stocklist_dict_temp[symbol]
        #     if asset_type != "Common Stock":
        #         # del stocklist_dict_temp[symbol]
        #         print("asset_type")
        #         print("delete: " + symbol + " | " + name)
        #         del stocklist_dict_temp[symbol]
        #     if shares_outstanding == "0":
        #         print("shares_outstanding")
        #         print("delete: " + symbol + " | " + name)
        #         del stocklist_dict_temp[symbol]

    stocklist_dict = stocklist_dict_temp
    return stocklist_dict

# ESG Rating für alle Aktien hinzufügen
def add_esg_rating():
    stocklist_dict = load_data("stocklist_dict")
    counter = 0

    for symbol in stocklist_dict:
        print("-" * 100)
        print(str(counter) + " " + symbol)
        counter += 1

        # Schleifer fortfahren
        if counter < 6151:
            continue

        # Daten von API holen
        url = "https://esg-environmental-social-governance-data.p.rapidapi.com/search"
        querystring = {"q": symbol}
        headers = {
            "X-RapidAPI-Host": "esg-environmental-social-governance-data.p.rapidapi.com",
            "X-RapidAPI-Key": "5e1447055fmshd217b6d846bbd7ap16f677jsn1e60f29bea63"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        time.sleep(1)
        data = response.text
        # Nächstes Symbol, falls data leer
        if data == "[]":
            print("Leer: " + symbol)
            stocklist_dict[symbol]["ESG"] = "None"
            continue
            print("wtf")
        else:
            data = json.loads(data)[0]
            if "company_name" in data:
                del data["company_name"]
            if "exchange_symbol" in data:
                del data["exchange_symbol"]
            if "stock_symbol" in data:
                del data["stock_symbol"]
            if "disclaimer" in data:
                del data["disclaimer"]
            print(data)
            # Daten dem Dict zuordnen
            stocklist_dict[symbol]["ESG"] = data

        save_data(stocklist_dict, "stocklist_dict")
        print("saved")

    return stocklist_dict

# ESG Rating Converter
def esg_rating_converter(unconverted_rating):
    esg_rating_dict = load_data("esg_rating_dict")
    rating = esg_rating_dict[unconverted_rating]
    return rating

# ESG Rating in Zahlen konvertieren und hinzufügen
def convert_esg_ratings():
    stocklist_dict = load_data("stocklist_dict")
    counter = 0

    for symbol in stocklist_dict:
        counter += 1
        print(str(counter) + " " + symbol)

        if stocklist_dict[symbol]["ESG"] != "None":
            environment_grade = stocklist_dict[symbol]["ESG"]["environment_grade"]
            social_grade = stocklist_dict[symbol]["ESG"]["social_grade"]
            governance_grade = stocklist_dict[symbol]["ESG"]["governance_grade"]
            total_grade = stocklist_dict[symbol]["ESG"]["total_grade"]

            environment_grade_converted = esg_rating_converter(environment_grade)
            social_grade_converted = esg_rating_converter(social_grade)
            governance_grade_converted = esg_rating_converter(governance_grade)
            total_grade_converted = esg_rating_converter(total_grade)

            stocklist_dict[symbol]["ESG"]["environment_grade_converted"] = environment_grade_converted
            stocklist_dict[symbol]["ESG"]["social_grade_converted"] = social_grade_converted
            stocklist_dict[symbol]["ESG"]["governance_grade_converted"] = governance_grade_converted
            stocklist_dict[symbol]["ESG"]["total_grade_converted"] = total_grade_converted

        # if counter == 1:
        #     break

    return stocklist_dict


# stocklist_dict = get_basic_nasdaq_info()
# save_data(stocklist_dict, "stocklist_dict")

# stocklist_dict = get_basic_alphavantage_info()
# save_data(stocklist_dict, "stocklist_dict")

# stocklist_dict = marketcap_categorizer()
# save_data(stocklist_dict, "stocklist_dict")

# stocklist_dict = clean_stocklist_dict()
# save_data(stocklist_dict, "stocklist_dict")

# stocklist_dict = add_esg_rating()

# stocklist_dict = convert_esg_ratings()
# save_data(stocklist_dict, "stocklist_dict")

