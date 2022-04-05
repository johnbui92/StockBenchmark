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

# Aktie in Kategorie "Marktkapitalisierung" einordnen
def marketcap_categorizer(symbol):
    marketcap = stockdata_dict[symbol]["FinancialData"]["CompanyOverview"]["MarketCapitalization"]
    if marketcap <= 50000000:
        marketcap_range = [0,50000000]
        marketcap_name = "Nano-Cap"
    if marketcap > 50000000 and marketcap <= 300000000:
        marketcap_range = [50000001,300000000]
        marketcap_name = "Micro-Cap"
    if marketcap > 300000000 and marketcap <= 2000000000:
        marketcap_range = [300000001,2000000000]
        marketcap_name = "Small-Cap"
    if marketcap > 2000000000 and marketcap <= 10000000000:
        marketcap_range = [2000000001, 10000000000]
        marketcap_name = "Mid-Cap"
    if marketcap > 10000000000 and marketcap <= 200000000000:
        marketcap_range = [10000000001, 200000000000]
        marketcap_name = "Large-Cap"
    if marketcap > 200000000000:
        marketcap_range = [200000000001, float("inf")]
        marketcap_name = "Mega-Cap"

    return marketcap_range, marketcap_name

# Gesammelte Daten für Aktie "X" benchmarken
def benchmark_stock(current_symbol):
    stockdata_dict = load_data("stockdata_dict")

    # Benchmark: Nur Branche
    current_industry = stockdata_dict[current_symbol]["Industry"]
    benchmark_dict = defaultdict(float)
    benchmark_dict["Industry"] = {}
    for category in stockdata_dict[current_symbol]["FinancialData"]:
        for ratio in stockdata_dict[current_symbol]["FinancialData"][category]:
            benchmark_dict["Industry"][ratio] = {}
            benchmark_dict["Industry"][ratio]["AllRatios"] = {}
            benchmark_dict["Industry"][ratio]["AllRatiosList"] = []
    for symbol in stockdata_dict:
        if stockdata_dict[symbol]["Industry"] == current_industry and symbol != current_symbol:
            print("-" * 100)
            print(symbol)
            for category in stockdata_dict[symbol]["FinancialData"]:
                for ratio in stockdata_dict[symbol]["FinancialData"][category]:
                    ratio_value = stockdata_dict[symbol]["FinancialData"][category][ratio]
                    print(ratio + ": " + str(ratio_value))
                    if ratio_value == "None" or ratio_value == "-":
                        print("Nicht aufgenommen: " + ratio + ": " + ratio_value)
                    else:
                        benchmark_dict["Industry"][ratio]["AllRatios"][symbol] = float(ratio_value)
                        benchmark = benchmark_dict["Industry"][ratio]["AllRatiosList"]
                        benchmark.append(float(ratio_value))
    for category in stockdata_dict[symbol]["FinancialData"]:
        for ratio in stockdata_dict[symbol]["FinancialData"][category]:
            # {0}_benchmark.format(ratio) = statistics.mean(ratio)
            all_ratios = benchmark_dict["Industry"][ratio]["AllRatiosList"]
            benchmark_dict["Industry"][ratio]["Benchmark"] = statistics.mean(all_ratios)

    return benchmark_dict


# stockdata_dict = get_stockdata()
# save_data(stockdata_dict, "stockdata_dict")

# industry_benchmark_dict = benachmark_stock("A")

# benchmark_dict = benchmark_stock("AAPL")

stockdata_dict = load_data("stockdata_dict")
sector_dict = defaultdict(int)
industry_dict = defaultdict(int)

for symbol in stockdata_dict:
    sector = stockdata_dict[symbol]["Sector"]
    sector_dict[sector] += 1
    industry = stockdata_dict[symbol]["Industry"]
    industry_dict[industry] += 1

pprint.pprint(sector_dict)
pprint.pprint(industry_dict)