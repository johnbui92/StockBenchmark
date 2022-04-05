import csv
import time
import pickle
from collections import defaultdict
import requests
import pprint

# Dictionary mit allen Aktien erstellen (Key: ISIN) aber ohne Symbol
def get_all_stocks_temp():
    with open("./data/xetra_all_stocks.csv", "r", encoding="utf-8") as f:
        csvreader = csv.reader(f, delimiter=";", quotechar='"')
        counter = 0
        list = []
        all_stocks_dict_temp = defaultdict(int)
        for row in csvreader:
            if counter > 2 and row[11] not in ["ETN0", "FON0", "FON1", "FON2", "FONA", "ETC1", "FDL0", "FDLA", "ETC1", "FLS0"]:
                isin = row[3]
                all_stocks_dict_temp[isin] = {}
                all_stocks_dict_temp[isin]["instrument"] = row[2]
                all_stocks_dict_temp[isin]["isin"] = row[3]
                all_stocks_dict_temp[isin]["productId"] = row[4]
                all_stocks_dict_temp[isin]["instrumentId"] = row[5]
                all_stocks_dict_temp[isin]["wkn"] = row[6]
                all_stocks_dict_temp[isin]["mmnemonic"] = row[7]
                all_stocks_dict_temp[isin]["productAssignmentGroup"] = row[11]
                all_stocks_dict_temp[isin]["productAssignmentGroupDescription"] = row[12]
                list.append(isin)
            counter += 1
    return all_stocks_dict_temp

# Dictionary mit allen Aktien um die richtigen Symbole und weitere Infos ergänzen
def get_all_stocks():
    counter = 0
    all_stocks_dict = defaultdict(int)
    failed_searches = []
    for isin in all_stocks_dict_temp:
        keywords = all_stocks_dict_temp[isin]['mmnemonic'] + "."
        url = 'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={0}&apikey=MGRYIUKL7JKXZH2V'.format(keywords)
        r = requests.get(url)
        data = r.json()
        counter += 1
        print("--------------------")
        print(str(counter) + " " + isin)
        time.sleep(0.2)

        # Wenn nur ein Treffer, wird direkt zugewiesen
        if len(data["bestMatches"]) == 1:
            matches_dict = data["bestMatches"][0]
            symbol = matches_dict["1. symbol"]
            all_stocks_dict[symbol] = {}
            for key in all_stocks_dict_temp[isin]:
                all_stocks_dict[symbol][key] = all_stocks_dict_temp[isin][key]
            for key in matches_dict:
                key_cleaned = key.split(" ")[1]
                all_stocks_dict[symbol][key_cleaned] = matches_dict[key]
            #counter += 1
            print(str(counter) + " " + symbol + " | " + all_stocks_dict[symbol]["name"])

        # Wenn genau zwei oder mehr Treffer, wird das Symbol mit Xetra präferiert, danach Frankfurt
        elif len(data["bestMatches"]) >= 2:
            xetra = False
            for dict in data["bestMatches"]:
                if dict["4. region"] == "XETRA":
                    xetra = True
                    xetra_dict = dict
            frankfurt = False
            for dict in data["bestMatches"]:
                if dict["4. region"] == "Frankfurt":
                    frankfurt = True
                    frankfurt_dict = dict
            if xetra == True:
                symbol = xetra_dict["1. symbol"]
                all_stocks_dict[symbol] = {}
                for key in all_stocks_dict_temp[isin]:
                    all_stocks_dict[symbol][key] = all_stocks_dict_temp[isin][key]
                for key in xetra_dict:
                    key_cleaned = key.split(" ")[1]
                    all_stocks_dict[symbol][key_cleaned] = xetra_dict[key]
                print(str(counter) + " " + symbol + " | " + all_stocks_dict[symbol]["name"])
            elif frankfurt == True:
                symbol = frankfurt_dict["1. symbol"]
                all_stocks_dict[symbol] = {}
                for key in all_stocks_dict_temp[isin]:
                    all_stocks_dict[symbol][key] = all_stocks_dict_temp[isin][key]
                for key in frankfurt_dict:
                    key_cleaned = key.split(" ")[1]
                    all_stocks_dict[symbol][key_cleaned] = frankfurt_dict[key]
                print(str(counter) + " " + symbol + " | " + all_stocks_dict[symbol]["name"])
            else:
                matches_dict = data["bestMatches"][0]
                symbol = matches_dict["1. symbol"]
                all_stocks_dict[symbol] = {}
                for key in all_stocks_dict_temp[isin]:
                    all_stocks_dict[symbol][key] = all_stocks_dict_temp[isin][key]
                for key in matches_dict:
                    key_cleaned = key.split(" ")[1]
                    all_stocks_dict[symbol][key_cleaned] = matches_dict[key]
                print(str(counter) + " " + symbol + " | " + all_stocks_dict[symbol]["name"] + " (kein Xetra gefunden)")

        # Wenn keine Treffer, soll mit dem Namen gesucht werden
        else:
            keywords = all_stocks_dict_temp[isin]['instrument']
            url = 'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={0}&apikey=MGRYIUKL7JKXZH2V'.format(keywords)
            r = requests.get(url)
            data = r.json()
            time.sleep(0.2)
            # Wenn nur ein Treffer, wird direkt zugewiesen
            if len(data["bestMatches"]) == 1:
                matches_dict = data["bestMatches"][0]
                symbol = matches_dict["1. symbol"]
                all_stocks_dict[symbol] = {}
                for key in all_stocks_dict_temp[isin]:
                    all_stocks_dict[symbol][key] = all_stocks_dict_temp[isin][key]
                for key in matches_dict:
                    key_cleaned = key.split(" ")[1]
                    all_stocks_dict[symbol][key_cleaned] = matches_dict[key]
                print(str(counter) + " " + symbol + " | " + all_stocks_dict[symbol]["name"])
            # Wenn genau zwei oder mehr Treffer, wird das Symbol mit Xetra präferiert, danach Frankfurt
            elif len(data["bestMatches"]) >= 2:
                xetra = False
                for dict in data["bestMatches"]:
                    if dict["4. region"] == "XETRA":
                        xetra = True
                        xetra_dict = dict
                frankfurt = False
                for dict in data["bestMatches"]:
                    if dict["4. region"] == "Frankfurt":
                        frankfurt = True
                        frankfurt_dict = dict
                if xetra == True:
                    symbol = xetra_dict["1. symbol"]
                    all_stocks_dict[symbol] = {}
                    for key in all_stocks_dict_temp[isin]:
                        all_stocks_dict[symbol][key] = all_stocks_dict_temp[isin][key]
                    for key in xetra_dict:
                        key_cleaned = key.split(" ")[1]
                        all_stocks_dict[symbol][key_cleaned] = xetra_dict[key]
                    print(str(counter) + " " + symbol + " | " + all_stocks_dict[symbol]["name"])
                elif frankfurt == True:
                    symbol = frankfurt_dict["1. symbol"]
                    all_stocks_dict[symbol] = {}
                    for key in all_stocks_dict_temp[isin]:
                        all_stocks_dict[symbol][key] = all_stocks_dict_temp[isin][key]
                    for key in frankfurt_dict:
                        key_cleaned = key.split(" ")[1]
                        all_stocks_dict[symbol][key_cleaned] = frankfurt_dict[key]
                    print(str(counter) + " " + symbol + " | " + all_stocks_dict[symbol]["name"])
                else:
                    matches_dict = data["bestMatches"][0]
                    symbol = matches_dict["1. symbol"]
                    all_stocks_dict[symbol] = {}
                    for key in all_stocks_dict_temp[isin]:
                        all_stocks_dict[symbol][key] = all_stocks_dict_temp[isin][key]
                    for key in matches_dict:
                        key_cleaned = key.split(" ")[1]
                        all_stocks_dict[symbol][key_cleaned] = matches_dict[key]
                    print(str(counter) + " " + symbol + " | " + all_stocks_dict[symbol]["name"] + " (kein Xetra gefunden)")
            else:
            # Name wird gekürzt und Suche erneut gestartet
            # keywords_splitted = keywords.replace("-", " ").split(" ")
            # keywords_splitted.pop()
            # keywords = " ".join(keywords_splitted)
            # Suche wird abgebrochen, sobald Keywords weniger als zwei Wörter ist
            # if len(keywords) <= 2:
                print("- " + str(counter) + " Fehler: Für " + str(all_stocks_dict_temp[isin]["instrument"]) + " mit der ISIN " + isin + " wurde nichts gefunden!")
                failed_searches.append(isin)

    return all_stocks_dict, failed_searches

# Dictionary mit allen Aktien um einzelne Aktien ergänzen
def get_single_stock(isin, symbol):
    keywords = symbol
    url = 'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={0}&apikey=MGRYIUKL7JKXZH2V'.format(keywords)
    r = requests.get(url)
    data = r.json()
    print(isin)
    time.sleep(0.2)

    # Wenn nur ein Treffer, wird direkt zugewiesen
    if len(data["bestMatches"]) == 1:
        matches_dict = data["bestMatches"][0]
        symbol = matches_dict["1. symbol"]
        all_stocks_dict[symbol] = {}
        for key in all_stocks_dict_temp[isin]:
            all_stocks_dict[symbol][key] = all_stocks_dict_temp[isin][key]
        for key in matches_dict:
            key_cleaned = key.split(" ")[1]
            all_stocks_dict[symbol][key_cleaned] = matches_dict[key]
        print(symbol + " | " + all_stocks_dict[symbol]["name"])

    # Wenn genau zwei oder mehr Treffer, wird das Symbol mit Xetra präferiert, danach Frankfurt
    elif len(data["bestMatches"]) >= 2:
        xetra = False
        for dict in data["bestMatches"]:
            if dict["4. region"] == "XETRA":
                xetra = True
                xetra_dict = dict
        frankfurt = False
        for dict in data["bestMatches"]:
            if dict["4. region"] == "Frankfurt":
                frankfurt = True
                frankfurt_dict = dict
        if xetra == True:
            symbol = xetra_dict["1. symbol"]
            all_stocks_dict[symbol] = {}
            for key in all_stocks_dict_temp[isin]:
                all_stocks_dict[symbol][key] = all_stocks_dict_temp[isin][key]
            for key in xetra_dict:
                key_cleaned = key.split(" ")[1]
                all_stocks_dict[symbol][key_cleaned] = xetra_dict[key]
            print(symbol + " | " + all_stocks_dict[symbol]["name"])
        elif frankfurt == True:
            symbol = frankfurt_dict["1. symbol"]
            all_stocks_dict[symbol] = {}
            for key in all_stocks_dict_temp[isin]:
                all_stocks_dict[symbol][key] = all_stocks_dict_temp[isin][key]
            for key in frankfurt_dict:
                key_cleaned = key.split(" ")[1]
                all_stocks_dict[symbol][key_cleaned] = frankfurt_dict[key]
            print(symbol + " | " + all_stocks_dict[symbol]["name"])
        else:
            matches_dict = data["bestMatches"][0]
            symbol = matches_dict["1. symbol"]
            all_stocks_dict[symbol] = {}
            for key in all_stocks_dict_temp[isin]:
                all_stocks_dict[symbol][key] = all_stocks_dict_temp[isin][key]
            for key in matches_dict:
                key_cleaned = key.split(" ")[1]
                all_stocks_dict[symbol][key_cleaned] = matches_dict[key]
            print(symbol + " | " + all_stocks_dict[symbol]["name"] + " (kein Xetra gefunden)")

    return all_stocks_dict

# Fehlschläge erneut mit Namen (instrument) suchen und Aktien Dictionary ergänzen
def get_missing_stocks():
    failed_searches_2 = []
    for isin in failed_searches:
        counter = 0
        keywords = all_stocks_dict_temp[isin]['instrument']
        url = 'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={0}&apikey=MGRYIUKL7JKXZH2V'.format(keywords)
        r = requests.get(url)
        data = r.json()
        counter += 1
        print("--------------------")
        print(str(counter) + " " + keywords + " | " + isin)
        time.sleep(0.2)

        # Wenn keine Treffer, dann soll solange die Keywords gekürz werden bis Treffer gefunden werden
        while len(data["bestMatches"]) == 0:
            keywords_splitted = keywords.replace("-", " ").split(" ")
            keywords_splitted.pop()
            keywords = " ".join(keywords_splitted).strip()
            print(keywords)
            url = 'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={0}&apikey=MGRYIUKL7JKXZH2V'.format(keywords)
            r = requests.get(url)
            data = r.json()
            time.sleep(0.2)
            if len(keywords.split(" ")) == 1:
                print(str(counter) + " Kein Treffer für " + all_stocks_dict_temp[isin]['instrument'] + " | " + isin)
                failed_searches_2.append(isin)
                break

        # Wenn nur ein Treffer, wird direkt zugewiesen
        if len(data["bestMatches"]) == 1:
            matches_dict = data["bestMatches"][0]
            symbol = matches_dict["1. symbol"]
            all_stocks_dict[symbol] = {}
            for key in all_stocks_dict_temp[isin]:
                all_stocks_dict[symbol][key] = all_stocks_dict_temp[isin][key]
            for key in matches_dict:
                key_cleaned = key.split(" ")[1]
                all_stocks_dict[symbol][key_cleaned] = matches_dict[key]
            #counter += 1
            print(str(counter) + " " + symbol + " | " + all_stocks_dict[symbol]["name"])

        # Wenn genau zwei oder mehr Treffer, wird das Symbol mit Xetra präferiert, danach Frankfurt
        if len(data["bestMatches"]) >= 2:
            xetra = False
            for dict in data["bestMatches"]:
                if dict["4. region"] == "XETRA":
                    xetra = True
                    xetra_dict = dict
            frankfurt = False
            for dict in data["bestMatches"]:
                if dict["4. region"] == "Frankfurt":
                    frankfurt = True
                    frankfurt_dict = dict
            if xetra == True:
                symbol = xetra_dict["1. symbol"]
                all_stocks_dict[symbol] = {}
                for key in all_stocks_dict_temp[isin]:
                    all_stocks_dict[symbol][key] = all_stocks_dict_temp[isin][key]
                for key in xetra_dict:
                    key_cleaned = key.split(" ")[1]
                    all_stocks_dict[symbol][key_cleaned] = xetra_dict[key]
                print(str(counter) + " " + symbol + " | " + all_stocks_dict[symbol]["name"])
            elif frankfurt == True:
                symbol = frankfurt_dict["1. symbol"]
                all_stocks_dict[symbol] = {}
                for key in all_stocks_dict_temp[isin]:
                    all_stocks_dict[symbol][key] = all_stocks_dict_temp[isin][key]
                for key in frankfurt_dict:
                    key_cleaned = key.split(" ")[1]
                    all_stocks_dict[symbol][key_cleaned] = frankfurt_dict[key]
                print(str(counter) + " " + symbol + " | " + all_stocks_dict[symbol]["name"])
            else:
                matches_dict = data["bestMatches"][0]
                symbol = matches_dict["1. symbol"]
                all_stocks_dict[symbol] = {}
                for key in all_stocks_dict_temp[isin]:
                    all_stocks_dict[symbol][key] = all_stocks_dict_temp[isin][key]
                for key in matches_dict:
                    key_cleaned = key.split(" ")[1]
                    all_stocks_dict[symbol][key_cleaned] = matches_dict[key]
                print(str(counter) + " " + symbol + " | " + all_stocks_dict[symbol]["name"] + " (kein Xetra gefunden)")
    return all_stocks_dict, failed_searches_2

# Dictionary mit allen Aktien als Pickle speichern
def save_all_stocks():
    with open("./data/all_stocks_dict.pickle", "wb") as handle:
        pickle.dump(all_stocks_dict, handle)
    with open("./data/failed_searches.pickle", "wb") as handle:
        pickle.dump(failed_searches, handle)

# Dictionary mit allen Aktien von Pickle laden
def load_all_stocks():
    with open("./data/all_stocks_dict.pickle", "rb") as handle:
        all_stocks_dict = pickle.load(handle)
    with open("./data/failed_searches.pickle", "rb") as handle:
        failed_searches = pickle.load(handle)
    return all_stocks_dict

# all_stocks_dict_temp = get_all_stocks_temp()
# all_stocks_dict, failed_searches = get_all_stocks()
# all_stocks_dict, failed_searches = load_all_stocks()
# all_stocks_dict, failed_searches_2 = get_missing_stocks()
# all_stocks_dict = get_single_stock("isin","symbol")
# save_all_stocks()





# Archiv ###########################################################################################
# # Liste mit allen ISIN-Nummern erstellen
# def get_all_isin():
#     with open("./data/xetra_all_stocks.csv", "r", encoding="utf-8") as f:
#         csvreader = csv.reader(f, delimiter=";", quotechar='"')
#         counter = 0
#         all_stocks_list = []
#         for row in csvreader:
#             if counter > 2:
#                 all_stocks_list.append(row[3])
#             counter += 1
#
# # Extrahierte ISIN-Nummern als Pickle speichern
# def save_all_isin():
#     with open("./data/all_stocks_list.pickle", "wb") as handle:
#         pickle.dump(all_stocks_list, handle)
#
# # Lade gespeicherte ISIN-Nummern
# def load_all_isin():
#     with open("./data/all_stocks_list.pickle", "rb") as handle:
#         all_stocks_list = pickle.load(handle)
#     return all_stocks_list