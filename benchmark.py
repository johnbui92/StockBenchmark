import time
import requests
import pprint
from stocklist import save_data, load_data
import pickle
import statistics
from collections import defaultdict

# API nutzen, um Daten für die Benchmark zu sammeln
def get_stockdata():
    stocklist_dict = load_data("stocklist_dict")
    stockdata_dict = stocklist_dict.copy()
    counter = 0
    for symbol in stockdata_dict:
        counter += 1
        print(str(counter) + " | " + symbol + ": " + stockdata_dict[symbol]["Name"])
        stockdata_dict[symbol]["FinancialData"] = {}
        stockdata_dict[symbol]["FinancialData"]["CompanyOverview"] = {}
        stockdata_dict[symbol]["FinancialData"]["BalanceSheet"] = {}
        stockdata_dict[symbol]["FinancialData"]["Cashflow"] = {}

        # Daten von "Company Overview" holen
        url = 'https://www.alphavantage.co/query?function=OVERVIEW&symbol={0}&apikey=MGRYIUKL7JKXZH2V'.format(symbol)
        r = requests.get(url)
        data = r.json()
        time.sleep(0.2)
        for entry in data:
            stockdata_dict[symbol]["FinancialData"]["CompanyOverview"]["AnalystTargetPrice"] = data["AnalystTargetPrice"]
            stockdata_dict[symbol]["FinancialData"]["CompanyOverview"]["Beta"] = data["Beta"]
            stockdata_dict[symbol]["FinancialData"]["CompanyOverview"]["BookValue"] = data["BookValue"]
            stockdata_dict[symbol]["FinancialData"]["CompanyOverview"]["DividendPerShare"] = data["DividendPerShare"]
            stockdata_dict[symbol]["FinancialData"]["CompanyOverview"]["DividendYield"] = data["DividendYield"]
            stockdata_dict[symbol]["FinancialData"]["CompanyOverview"]["EBITDA"] = data["EBITDA"]
            stockdata_dict[symbol]["FinancialData"]["CompanyOverview"]["EPS"] = data["EPS"]
            stockdata_dict[symbol]["FinancialData"]["CompanyOverview"]["EVToEBITDA"] = data["EVToEBITDA"]
            stockdata_dict[symbol]["FinancialData"]["CompanyOverview"]["EVToRevenue"] = data["EVToRevenue"]
            stockdata_dict[symbol]["FinancialData"]["CompanyOverview"]["ForwardPE"] = data["ForwardPE"]
            stockdata_dict[symbol]["FinancialData"]["CompanyOverview"]["GrossProfitTTM"] = data["GrossProfitTTM"]
            stockdata_dict[symbol]["FinancialData"]["CompanyOverview"]["MarketCapitalization"] = data["MarketCapitalization"]
            stockdata_dict[symbol]["FinancialData"]["CompanyOverview"]["OperatingMarginTTM"] = data["OperatingMarginTTM"]
            stockdata_dict[symbol]["FinancialData"]["CompanyOverview"]["PEGRatio"] = data["PEGRatio"]
            stockdata_dict[symbol]["FinancialData"]["CompanyOverview"]["PERatio"] = data["PERatio"]
            stockdata_dict[symbol]["FinancialData"]["CompanyOverview"]["PriceToBookRatio"] = data["PriceToBookRatio"]
            stockdata_dict[symbol]["FinancialData"]["CompanyOverview"]["PriceToSalesRatioTTM"] = data["PriceToSalesRatioTTM"]
            stockdata_dict[symbol]["FinancialData"]["CompanyOverview"]["ProfitMargin"] = data["ProfitMargin"]
            stockdata_dict[symbol]["FinancialData"]["CompanyOverview"]["QuarterlyEarningsGrowthYOY"] = data["QuarterlyEarningsGrowthYOY"]
            stockdata_dict[symbol]["FinancialData"]["CompanyOverview"]["QuarterlyRevenueGrowthYOY"] = data["QuarterlyRevenueGrowthYOY"]
            stockdata_dict[symbol]["FinancialData"]["CompanyOverview"]["ReturnOnAssetsTTM"] = data["ReturnOnAssetsTTM"]
            stockdata_dict[symbol]["FinancialData"]["CompanyOverview"]["ReturnOnEquityTTM"] = data["ReturnOnEquityTTM"]
            stockdata_dict[symbol]["FinancialData"]["CompanyOverview"]["RevenuePerShareTTM"] = data["RevenuePerShareTTM"]
            stockdata_dict[symbol]["FinancialData"]["CompanyOverview"]["RevenueTTM"] = data["RevenueTTM"]
            stockdata_dict[symbol]["FinancialData"]["CompanyOverview"]["SharesOutstanding"] = data["SharesOutstanding"]
            stockdata_dict[symbol]["FinancialData"]["CompanyOverview"]["TrailingPE"] = data["TrailingPE"]

        # Daten von "Balance Sheet" holen
        url = 'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={0}&apikey=MGRYIUKL7JKXZH2V'.format(symbol)
        r = requests.get(url)
        data = r.json()
        time.sleep(0.2)
        for entry in data:
            if data["annualReports"] != []:
                stockdata_dict[symbol]["FinancialData"]["BalanceSheet"]["totalCurrentAssets"] = data["annualReports"][0]["totalCurrentAssets"]
                stockdata_dict[symbol]["FinancialData"]["BalanceSheet"]["totalNonCurrentAssets"] = data["annualReports"][0]["totalNonCurrentAssets"]
                stockdata_dict[symbol]["FinancialData"]["BalanceSheet"]["totalAssets"] = data["annualReports"][0]["totalAssets"]
                stockdata_dict[symbol]["FinancialData"]["BalanceSheet"]["totalCurrentLiabilities"] = data["annualReports"][0]["totalCurrentLiabilities"]
                stockdata_dict[symbol]["FinancialData"]["BalanceSheet"]["totalNonCurrentLiabilities"] = data["annualReports"][0]["totalNonCurrentLiabilities"]
                stockdata_dict[symbol]["FinancialData"]["BalanceSheet"]["totalLiabilities"] = data["annualReports"][0]["totalLiabilities"]
                stockdata_dict[symbol]["FinancialData"]["BalanceSheet"]["totalShareholderEquity"] = data["annualReports"][0]["totalShareholderEquity"]

                total_assets = data["annualReports"][0]["totalAssets"]
                total_liabilities = data["annualReports"][0]["totalLiabilities"]

                if total_assets != "None" and total_liabilities != "None":
                    equity = float(total_assets) - float(total_liabilities)
                    stockdata_dict[symbol]["FinancialData"]["BalanceSheet"]["totalEquity"] = str(equity)
                else:
                    stockdata_dict[symbol]["FinancialData"]["BalanceSheet"]["totalEquity"] = "None"
            else:
                stockdata_dict[symbol]["FinancialData"]["BalanceSheet"] = "None"

        # Daten von "Cash Flow" holen
        url = 'https://www.alphavantage.co/query?function=CASH_FLOW&symbol={0}&apikey=MGRYIUKL7JKXZH2V'.format(symbol)
        r = requests.get(url)
        data = r.json()
        time.sleep(0.2)
        for entry in data:
            if data["annualReports"] != []:
                stockdata_dict[symbol]["FinancialData"]["Cashflow"]["cashflowFromFinancing"] = data["annualReports"][0]["cashflowFromFinancing"]
                stockdata_dict[symbol]["FinancialData"]["Cashflow"]["cashflowFromInvestment"] = data["annualReports"][0]["cashflowFromInvestment"]
                stockdata_dict[symbol]["FinancialData"]["Cashflow"]["dividendPayout"] = data["annualReports"][0]["dividendPayout"]
                stockdata_dict[symbol]["FinancialData"]["Cashflow"]["netIncome"] = data["annualReports"][0]["netIncome"]
                stockdata_dict[symbol]["FinancialData"]["Cashflow"]["operatingCashflow"] = data["annualReports"][0]["operatingCashflow"]
                stockdata_dict[symbol]["FinancialData"]["Cashflow"]["profitLoss"] = data["annualReports"][0]["profitLoss"]
            else:
                stockdata_dict[symbol]["FinancialData"]["Cashflow"] = "None"

        # if counter == 1:
        #     break

    return stockdata_dict

# ESG Rating Converter
def esg_rating_converter(unconverted_rating):
    esg_rating_dict = load_data("esg_rating_dict")
    rating = esg_rating_dict[unconverted_rating]
    return rating

# Gesammelte Daten für Aktie "X" benchmarken
def benchmark_stock(current_symbol):
    stockdata_dict = load_data("stockdata_dict")
    benchmark_dict = defaultdict(int)
    for category in stockdata_dict[current_symbol]["FinancialData"]:
        for ratio in stockdata_dict[current_symbol]["FinancialData"][category]:
            benchmark_dict[ratio] = {}

    # Benchmark: Sektor (Sector) ####################################################################
    current_sector = stockdata_dict[current_symbol]["Sector"]
    # Leere Dictionaries und Listen anlegen
    for category in stockdata_dict[current_symbol]["FinancialData"]:
        for ratio in stockdata_dict[current_symbol]["FinancialData"][category]:
            benchmark_dict[ratio]["Sector"] = {}
            benchmark_dict[ratio]["Sector"]["AllRatios"] = {}
            benchmark_dict[ratio]["Sector"]["AllRatiosList"] = []
    # Kennzahlen von allen Aktien derselben Branche holen
    for symbol in stockdata_dict:
        if stockdata_dict[symbol]["Sector"] == current_sector:
            print("-" * 100)
            print(symbol)
            # Daten von FinancialData holen
            for category in stockdata_dict[symbol]["FinancialData"]:
                # Nur weiter machen, wenn Daten in der Kategorie vorhanden sind
                if stockdata_dict[symbol]["FinancialData"][category] != "None":
                    for ratio in stockdata_dict[symbol]["FinancialData"][category]:
                        ratio_value = stockdata_dict[symbol]["FinancialData"][category][ratio]
                        print(ratio + ": " + str(ratio_value))
                        # Wenn Kennzahl nicht vorhanden → wird nicht in die Benchmark aufgenommen
                        if ratio_value == "None" or ratio_value == "-":
                            print("Nicht aufgenommen: " + ratio + ": " + ratio_value)
                        else:
                            benchmark_dict[ratio]["Sector"]["AllRatios"][symbol] = float(ratio_value)
                            all_ratios = benchmark_dict[ratio]["Sector"]["AllRatiosList"]
                            all_ratios.append(float(ratio_value))
                else:
                    print("Leer: " + category)
            # Daten von ESG holen
            if "ESG" in stockdata_dict[symbol]:
                benchmark_dict[ratio]["Sector"]["AllRatings"][symbol]["environment_grade"] = stockdata_dict[symbol]["ESG"]["environment_grade"]
            else:
                print("ESG leer: " + symbol)

    # FinancialData: Gesammelten Kennzahlen werden im Durchschnitt genommen
    for category in stockdata_dict[symbol]["FinancialData"]:
        for ratio in stockdata_dict[symbol]["FinancialData"][category]:
            all_ratios = benchmark_dict[ratio]["Sector"]["AllRatiosList"]
            if all_ratios != []:
                benchmark_dict[ratio]["Sector"]["Benchmark"] = statistics.mean(all_ratios)
            else:
                print("Leere Kennzahl: " + ratio)

    # Benchmark: Sektor und ähnliche Martkkapitalisierung (Sector and Size) #########################################
    current_sector = stockdata_dict[current_symbol]["Sector"]
    current_size = stockdata_dict[current_symbol]["Size"]
    # Leere Dictionaries und Listen anlegen
    for category in stockdata_dict[current_symbol]["FinancialData"]:
        for ratio in stockdata_dict[current_symbol]["FinancialData"][category]:
            benchmark_dict[ratio]["SectorAndSize"] = {}
            benchmark_dict[ratio]["SectorAndSize"]["AllRatios"] = {}
            benchmark_dict[ratio]["SectorAndSize"]["AllRatiosList"] = []
    # Kennzahlen von allen Aktien derselben Branche holen
    for symbol in stockdata_dict:
        if stockdata_dict[symbol]["Sector"] == current_sector and stockdata_dict[symbol]["Size"] == current_size:
            print("-" * 100)
            print(symbol)
            for category in stockdata_dict[symbol]["FinancialData"]:
                # Nur weiter machen, wenn Daten in der Kategorie vorhanden sind
                if stockdata_dict[symbol]["FinancialData"][category] != "None":
                    for ratio in stockdata_dict[symbol]["FinancialData"][category]:
                        ratio_value = stockdata_dict[symbol]["FinancialData"][category][ratio]
                        print(ratio + ": " + str(ratio_value))
                        # Wenn Kennzahl nicht vorhanden → wird nicht in die Benchmark aufgenommen
                        if ratio_value == "None" or ratio_value == "-":
                            print("Nicht aufgenommen: " + ratio + ": " + ratio_value)
                        else:
                            benchmark_dict[ratio]["SectorAndSize"]["AllRatios"][symbol] = float(ratio_value)
                            all_ratios = benchmark_dict[ratio]["SectorAndSize"]["AllRatiosList"]
                            all_ratios.append(float(ratio_value))
                else:
                    print("Leer: " + category)
    # Gesammelten Kennzahlen werden im Durchschnitt genommen
    for category in stockdata_dict[symbol]["FinancialData"]:
        for ratio in stockdata_dict[symbol]["FinancialData"][category]:
            all_ratios = benchmark_dict[ratio]["SectorAndSize"]["AllRatiosList"]
            if all_ratios != []:
                benchmark_dict[ratio]["SectorAndSize"]["Benchmark"] = statistics.mean(all_ratios)
            else:
                print("Leere Kennzahl: " + ratio)

    # Benchmark: Branche (Industry) ##################################################################
    current_industry = stockdata_dict[current_symbol]["Industry"]
    # Leere Dictionaries und Listen anlegen
    for category in stockdata_dict[current_symbol]["FinancialData"]:
        for ratio in stockdata_dict[current_symbol]["FinancialData"][category]:
            benchmark_dict[ratio]["Industry"] = {}
            benchmark_dict[ratio]["Industry"]["AllRatios"] = {}
            benchmark_dict[ratio]["Industry"]["AllRatiosList"] = []
    # Kennzahlen von allen Aktien derselben Branche holen
    for symbol in stockdata_dict:
        if stockdata_dict[symbol]["Industry"] == current_industry:
            print("-" * 100)
            print(symbol)
            for category in stockdata_dict[symbol]["FinancialData"]:
                # Nur weiter machen, wenn Daten in der Kategorie vorhanden sind
                if stockdata_dict[symbol]["FinancialData"][category] != "None":
                    for ratio in stockdata_dict[symbol]["FinancialData"][category]:
                        ratio_value = stockdata_dict[symbol]["FinancialData"][category][ratio]
                        print(ratio + ": " + str(ratio_value))
                        # Wenn Kennzahl nicht vorhanden → wird nicht in die Benchmark aufgenommen
                        if ratio_value == "None" or ratio_value == "-":
                            print("Nicht aufgenommen: " + ratio + ": " + ratio_value)
                        else:
                            benchmark_dict[ratio]["Industry"]["AllRatios"][symbol] = float(ratio_value)
                            all_ratios = benchmark_dict[ratio]["Industry"]["AllRatiosList"]
                            all_ratios.append(float(ratio_value))
                else:
                    print("Leer: " + category)
    # Gesammelten Kennzahlen werden im Durchschnitt genommen
    for category in stockdata_dict[symbol]["FinancialData"]:
        for ratio in stockdata_dict[symbol]["FinancialData"][category]:
            all_ratios = benchmark_dict[ratio]["Industry"]["AllRatiosList"]
            if all_ratios != []:
                benchmark_dict[ratio]["Industry"]["Benchmark"] = statistics.mean(all_ratios)
            else:
                print("Leere Kennzahl: " + ratio)

    # Benchmark: Branche und ähnliche Martkkapitalisierung (Industry and Size) #########################################
    current_industry = stockdata_dict[current_symbol]["Industry"]
    current_size = stockdata_dict[current_symbol]["Size"]
    # Leere Dictionaries und Listen anlegen
    for category in stockdata_dict[current_symbol]["FinancialData"]:
        for ratio in stockdata_dict[current_symbol]["FinancialData"][category]:
            benchmark_dict[ratio]["IndustryAndSize"] = {}
            benchmark_dict[ratio]["IndustryAndSize"]["AllRatios"] = {}
            benchmark_dict[ratio]["IndustryAndSize"]["AllRatiosList"] = []
    # Kennzahlen von allen Aktien derselben Branche holen
    for symbol in stockdata_dict:
        if stockdata_dict[symbol]["Industry"] == current_industry and stockdata_dict[symbol]["Size"] == current_size:
            print("-" * 100)
            print(symbol)
            for category in stockdata_dict[symbol]["FinancialData"]:
                # Nur weiter machen, wenn Daten in der Kategorie vorhanden sind
                if stockdata_dict[symbol]["FinancialData"][category] != "None":
                    for ratio in stockdata_dict[symbol]["FinancialData"][category]:
                        ratio_value = stockdata_dict[symbol]["FinancialData"][category][ratio]
                        print(ratio + ": " + str(ratio_value))
                        # Wenn Kennzahl nicht vorhanden → wird nicht in die Benchmark aufgenommen
                        if ratio_value == "None" or ratio_value == "-":
                            print("Nicht aufgenommen: " + ratio + ": " + ratio_value)
                        else:
                            benchmark_dict[ratio]["Industry"]["AllRatios"][symbol] = float(ratio_value)
                            all_ratios = benchmark_dict[ratio]["Industry"]["AllRatiosList"]
                            all_ratios.append(float(ratio_value))
                else:
                    print("Leer: " + category)
    # Gesammelten Kennzahlen werden im Durchschnitt genommen
    for category in stockdata_dict[symbol]["FinancialData"]:
        for ratio in stockdata_dict[symbol]["FinancialData"][category]:
            all_ratios = benchmark_dict[ratio]["IndustryAndSize"]["AllRatiosList"]
            if all_ratios != []:
                benchmark_dict[ratio]["IndustryAndSize"]["Benchmark"] = statistics.mean(all_ratios)
            else:
                print("Leere Kennzahl: " + ratio)

    return benchmark_dict

# Aktueller Preis für jeweilige Aktie holen
def stock_price(symbol):
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey=MGRYIUKL7JKXZH2V'
    r = requests.get(url)
    data = r.json()
    stock_price = data["Global Quote"]["05. price"]
    return stock_price

# stockdata_dict = get_stockdata()
# save_data(stockdata_dict, "stockdata_dict")

# benchmark_dict = benchmark_stock("GOOG")

# stock_price("GOOG")