import csv
import yfinance as yf
import time
import pickle
from collections import defaultdict

# Liste mit allen ISIN-Nummern erstellen
def get_all_isin():
    with open("../data/xetra_all_stocks.csv", "r", encoding="utf-8") as f:
        csvreader = csv.reader(f, delimiter=";", quotechar='"')
        counter = 0
        all_stocks_list = []
        for row in csvreader:
            if counter > 2:
                all_stocks_list.append(row[3])
            counter += 1

# Extrahierte ISIN-Nummern als Pickle speichern
def save_all_isin():
    with open("../data/all_stocks_list.pickle", "wb") as handle:
        pickle.dump(all_stocks_list, handle)

# Lade gespeicherte ISIN-Nummern
def load_all_isin():
    with open("../data/all_stocks_list.pickle", "rb") as handle:
        all_stocks_list = pickle.load(handle)
    return all_stocks_list

# Erstelle Dictionary für eine Aktie und indexiere diese in einem zweiten Dictionary
def get_stock_info(isin):
    stock = yf.Ticker(isin)
    all_stocks_dict = {isin: stock.info}
    print(all_stocks_dict)
    index_dict = defaultdict(int)
    index_dict[isin] = isin
    for key in all_stocks_dict[isin]:
        if key == "shortName" or key == "longName":
            value = all_stocks_dict[isin][key]
            index_dict[value] = isin
            index_dict[value.split(" ")[0]] = isin
        if key == "underlyingSymbol" or key == "symbol":
            value = all_stocks_dict[isin][key]
            index_dict[value] = isin
    return all_stocks_dict, index_dict

# Speise das Stocks-Dictionary mit Infos von alle Aktien, ergänze dabei das Index-Dictionary und speichere es ab
def get_all_stocks_info(all_stocks_list):
    counter = 0
    for isin in all_stocks_list:
        all_stocks_dict, index_dict = get_stock_info(isin)
        print(counter)
        counter += 1
        time.sleep(30)
        if counter == 20:
            print(all_stocks_dict)
            print(index_dict)
            break

# Funktionsaufrufe
all_stocks_list = load_all_isin()
make_all_stocks_dict(all_stocks_list)


# Get stocks data from internet
apc_de = yf.Ticker("AT0000644505")
print(apc_de.info)
#
#
# stocks_dict = defaultdict(int)
# stocks_dict["apc_de"] = apc_de.info
#
# print(stocks_dict["apc_de"])
#
# for entry in stocks_dict["apc_de"]:
#     print(entry + ": " + str(stocks_dict["apc_de"][entry]))
