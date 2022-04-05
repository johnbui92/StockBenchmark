import time
import requests
import pprint
from stocklist import save_data, load_data
import pickle
import statistics
from collections import defaultdict

# API nutzen, um Daten für die Benchmark zu sammeln
def get_stockdata():
    stocklist_dict = load_data("stocklist_dict_cleaned")
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
                    stockdata_dict[symbol]["FinancialData"]["BalanceSheet"]["totalEquity"] = equity
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

# Gesammelte Daten für Aktie "X" benchmarken
def benchmark_stock(current_symbol):
    stockdata_dict = load_data("stockdata_dict")
    benchmark_dict = defaultdict(int)
    for category in stockdata_dict[current_symbol]["FinancialData"]:
        for ratio in stockdata_dict[current_symbol]["FinancialData"][category]:
            benchmark_dict[ratio] = {}

    # Benchmark: Industry (Branche) ############################################################################
    current_industry = stockdata_dict[current_symbol]["Industry"]
    for category in stockdata_dict[current_symbol]["FinancialData"]:
        for ratio in stockdata_dict[current_symbol]["FinancialData"][category]:
            benchmark_dict[ratio]["Industry"] = {}
            benchmark_dict[ratio]["Industry"]["AllRatios"] = {}
            benchmark_dict[ratio]["Industry"]["AllRatiosList"] = []
    for symbol in stockdata_dict:
        if stockdata_dict[symbol]["Industry"] == current_industry:
            print("-" * 100)
            print(symbol)
            for category in stockdata_dict[symbol]["FinancialData"]:
                for ratio in stockdata_dict[symbol]["FinancialData"][category]:
                    ratio_value = stockdata_dict[symbol]["FinancialData"][category][ratio]
                    print(ratio + ": " + str(ratio_value))
                    if ratio_value == "None" or ratio_value == "-":
                        print("Nicht aufgenommen: " + ratio + ": " + ratio_value)
                    else:
                        benchmark_dict[ratio]["Industry"]["AllRatios"][symbol] = float(ratio_value)
                        all_ratios = benchmark_dict[ratio]["Industry"]["AllRatiosList"]
                        all_ratios.append(float(ratio_value))
    for category in stockdata_dict[symbol]["FinancialData"]:
        for ratio in stockdata_dict[symbol]["FinancialData"][category]:
            all_ratios = benchmark_dict[ratio]["Industry"]["AllRatiosList"]
            benchmark_dict[ratio]["Industry"]["Benchmark"] = statistics.mean(all_ratios)

    # Benchmark: Industry und Size (Branche und ähnliche Marktkapitalisierung) #################################
    current_industry = stockdata_dict[current_symbol]["Industry"]
    current_size = stockdata_dict[current_symbol]["Size"]
    for category in stockdata_dict[current_symbol]["FinancialData"]:
        for ratio in stockdata_dict[current_symbol]["FinancialData"][category]:
            benchmark_dict[ratio]["IndustryAndSize"] = {}
            benchmark_dict[ratio]["IndustryAndSize"]["AllRatios"] = {}
            benchmark_dict[ratio]["IndustryAndSize"]["AllRatiosList"] = []
    for symbol in stockdata_dict:
        if stockdata_dict[symbol]["Industry"] == current_industry and stockdata_dict[symbol]["Size"] == current_size:
            print("-" * 100)
            print(symbol)
            for category in stockdata_dict[symbol]["FinancialData"]:
                for ratio in stockdata_dict[symbol]["FinancialData"][category]:
                    ratio_value = stockdata_dict[symbol]["FinancialData"][category][ratio]
                    print(ratio + ": " + str(ratio_value))
                    if ratio_value == "None" or ratio_value == "-":
                        print("Nicht aufgenommen: " + ratio + ": " + ratio_value)
                    else:
                        benchmark_dict[ratio]["IndustryAndSize"]["AllRatios"][symbol] = float(ratio_value)
                        all_ratios = benchmark_dict[ratio]["IndustryAndSize"]["AllRatiosList"]
                        all_ratios.append(float(ratio_value))
    for category in stockdata_dict[symbol]["FinancialData"]:
        for ratio in stockdata_dict[symbol]["FinancialData"][category]:
            all_ratios = benchmark_dict[ratio]["IndustryAndSize"]["AllRatiosList"]
            if all_ratios != []:
                benchmark_dict[ratio]["IndustryAndSize"]["Benchmark"] = statistics.mean(all_ratios)
            else:
                benchmark_dict[ratio]["IndustryAndSize"]["Benchmark"] = "None"

    # # Benchmark: Sector (Wirtschaftszweige) ############################################################################
    # current_sector = stockdata_dict[current_symbol]["Sector"]
    # benchmark_dict = defaultdict(float)
    # benchmark_dict["Sector"] = {}
    # # Leere Dictionaries und Listen für jede Kennzahl anlegen
    # for category in stockdata_dict[current_symbol]["FinancialData"]:
    #     benchmark_dict["Sector"][category]= {}
    #     for ratio in stockdata_dict[current_symbol]["FinancialData"][category]:
    #         benchmark_dict["Sector"][category][ratio] = {}
    #         benchmark_dict["Sector"][category][ratio]["AllRatios"] = {}
    #         benchmark_dict["Sector"][category][ratio]["AllRatiosList"] = []
    # for symbol in stockdata_dict:
    #     # Nur Aktien im gleichen Sektor nehmen
    #     if stockdata_dict[symbol]["Sector"] == current_sector and symbol != current_symbol:
    #         print("-" * 100)
    #         print(symbol)
    #         for category in stockdata_dict[symbol]["FinancialData"]:
    #             category_value = stockdata_dict[symbol]["FinancialData"][category]
    #             # Schleife soll abgebrochen werden, wenn in der Kategorie keine Daten zu finden sind
    #             if category_value == "None":
    #                 continue
    #             else:
    #                 for ratio in stockdata_dict[symbol]["FinancialData"][category]:
    #                     ratio_value = stockdata_dict[symbol]["FinancialData"][category][ratio]
    #                     print(ratio + ": " + str(ratio_value))
    #                     # Wenn Kennzahl leer ist, soll diese nicht mit einbezogen werden
    #                     if ratio_value == "None" or ratio_value == "-":
    #                         print("Nicht aufgenommen: " + ratio + ": " + ratio_value)
    #                     # Kennzahl wird in das Dict eingetragen
    #                     else:
    #                         benchmark_dict["Sector"][category][ratio]["AllRatios"][symbol] = float(ratio_value)
    #                         benchmark = benchmark_dict["Sector"][category][ratio]["AllRatiosList"]
    #                         benchmark.append(float(ratio_value))
    # # Durchschnitt von allen gesammelten Kennzahlen berechnen und ins Dict eintragen
    # for category in stockdata_dict[symbol]["FinancialData"]:
    #     for ratio in stockdata_dict[symbol]["FinancialData"][category]:
    #         all_ratios = benchmark_dict["Sector"][category][ratio]["AllRatiosList"]
    #         benchmark_dict["Sector"][category][ratio]["Benchmark"] = statistics.mean(all_ratios)


    # # Benchmark: Industry (Branche) ############################################################################
    # current_industry = stockdata_dict[current_symbol]["Industry"]
    # # benchmark_dict = defaultdict(float)
    # benchmark_dict["Industry"] = {}
    # # Leere Dictionaries und Listen für jede Kennzahl anlegen
    # for category in stockdata_dict[current_symbol]["FinancialData"]:
    #     benchmark_dict["Industry"][category]= {}
    #     for ratio in stockdata_dict[current_symbol]["FinancialData"][category]:
    #         benchmark_dict["Industry"][category][ratio] = {}
    #         benchmark_dict["Industry"][category][ratio]["AllRatios"] = {}
    #         benchmark_dict["Industry"][category][ratio]["AllRatiosList"] = []
    # for symbol in stockdata_dict:
    #     # Nur Aktien in der gleichen Brache nehmen
    #     if stockdata_dict[symbol]["Industry"] == current_industry and symbol != current_symbol:
    #         print("-" * 100)
    #         print(symbol)
    #         for category in stockdata_dict[symbol]["FinancialData"]:
    #             category_value = stockdata_dict[symbol]["FinancialData"][category]
    #             # Schleife soll abgebrochen werden, wenn in der Kategorie keine Daten zu finden sind
    #             if category_value == "None":
    #                 continue
    #             else:
    #                 for ratio in stockdata_dict[symbol]["FinancialData"][category]:
    #                     ratio_value = stockdata_dict[symbol]["FinancialData"][category][ratio]
    #                     print(ratio + ": " + str(ratio_value))
    #                     # Wenn Kennzahl leer ist, soll diese nicht mit einbezogen werden
    #                     if ratio_value == "None" or ratio_value == "-":
    #                         print("Nicht aufgenommen: " + ratio + ": " + ratio_value)
    #                     # Kennzahl wird in das Dict eingetragen
    #                     else:
    #                         benchmark_dict["Industry"][category][ratio]["AllRatios"][symbol] = float(ratio_value)
    #                         benchmark = benchmark_dict["Industry"][category][ratio]["AllRatiosList"]
    #                         benchmark.append(float(ratio_value))
    # # Durchschnitt von allen gesammelten Kennzahlen berechnen und ins Dict eintragen
    # for category in stockdata_dict[symbol]["FinancialData"]:
    #     for ratio in stockdata_dict[symbol]["FinancialData"][category]:
    #         all_ratios = benchmark_dict["Industry"][category][ratio]["AllRatiosList"]
    #         benchmark_dict["Industry"][category][ratio]["Benchmark"] = statistics.mean(all_ratios)

    return benchmark_dict


# stockdata_dict = get_stockdata()
# save_data(stockdata_dict, "stockdata_dict")

# industry_benchmark_dict = benachmark_stock("A")

benchmark_dict = benchmark_stock("GOOG")