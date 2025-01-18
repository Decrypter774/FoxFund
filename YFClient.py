import yfinance as yf
import time
from decimal import Decimal

from DBRepo import StockDatabase


class YFClient:
    def __init__(self):
        pass

    def fetch_data(self, symbol):
        try:
            info = yf.Ticker(symbol)
            if info is None:
                time.sleep(5)
                info = yf.Ticker(symbol)
                if info is None:
                    return None

            return info.info

        except Exception as e:
            print("exception in yf client:", e)
            if 'Expecting value: line 1 column 1 (char 0)' in str(e):
                print("Waiting 5 seconds...")
                time.sleep(25)
                self.fetch_data()
            elif '404' in str(e):
                print("YahooClient: 404 error for " + symbol)
                pass

# 1. Write a MODULE (CLASS) for Yahoo finance
# get data from yahoo by symbol
# 'yh_trailingPE' DECIMAL(10, 2)
# 'yh_longBusinessSummary' VARCHAR(1024)
# 'yh_forwardPE' DECIMAL(10, 2)
# 'yh_dividendYield' DECIMAL(10, 4)
# 'yh_payoutRatio' DECIMAL(10, 4)
# 'yh_debtToEquity' DECIMAL(10, 4)
# 'yh_priceToBook' DECIMAL(10, 4)
# 'yh_freeCashflow' DECIMAL(10, 4)
# check http error. if 429 (too many requests), wait 5 sec

# 2. Add columns to the database for the fields above
# consider adding prefix to the columns so we know where did daqta come from, e.g. yh_longBusinessSummary

# 3. Write function named "enrichWithYahoo" that downloads symbol data from Yahoo for every symbol in our database and fills new fields
# do not delete from the database, use update
