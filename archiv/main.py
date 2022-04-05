import yfinance as yf
import time

msft = yf.Ticker("MSF.DE")

# get stock info
msft.info

while True:
    msft = yf.Ticker("MSF.DE")
    msft.info
    print(msft.info["ask"])
    print(msft.info["bid"])
    print("--------------------")
    time.sleep(5)

# get historical market data
hist = msft.history(period="1d")
print(hist)

# show actions (dividends, splits)
msft.actions

# show financials
msft.financials
print(msft.financials)

msft.quarterly_financials
