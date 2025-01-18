import json
import os
import time

from DBRepo import StockDatabase
from FMPClient import FMPClient
from YFClient import YFClient
from decimal import Decimal, ROUND_HALF_UP


def enrichWithYahoo(symbol):
    DATABASE = {
        'dbname': 'postgres',
        'user': 'postgres',
        'password': 'postgres',
        'host': 'localhost',
        'port': 5432
    }
    stock_db = StockDatabase(DATABASE)
    yf_client = YFClient()
    yf_data = yf_client.fetch_data(symbol)
    print(str(yf_data))
    if str(yf_data) != "{'trailingPegRatio': None}":
        update_dict = dict()
        if "longBusinessSummary" in yf_data:
            update_dict['yh_longBusinessSummary'] = yf_data["longBusinessSummary"]
        if "trailingPE" in yf_data:
            update_dict['yh_trailingPE'] = round(float(yf_data["trailingPE"]),4)
        if "forwardPE" in yf_data:
            update_dict['yh_forwardPE'] = round(float(yf_data["forwardPE"]),4)
        if "dividendYield" in yf_data:
            update_dict['yh_dividendYield'] = round(float(yf_data["dividendYield"]),4)
        if "payoutRatio" in yf_data:
            update_dict['yh_payoutRatio'] = round(float(yf_data["payoutRatio"]),4)
        if "debtToEquity" in yf_data:
            update_dict['yh_debtToEquity'] = round(float(yf_data["debtToEquity"]),4)
        if "priceToBook" in yf_data:
            update_dict['yh_priceToBook'] = round(float(yf_data["priceToBook"]),4)
        if "freeCashflow" in yf_data:
            update_dict['yh_freeCashflow'] = round(float(yf_data["freeCashflow"]),4)
        if len(update_dict)>0:
            stock_db.update_stock(symbol, update_dict)
    else:
        time.sleep(2)


if '__main__' == __name__:
    DATABASE = {
        'dbname': 'postgres',
        'user': 'postgres',
        'password': 'postgres',
        'host': 'localhost',
        'port': 5432
    }
    stock_db = StockDatabase(DATABASE)
    stocks=stock_db.list_all_stocks()
    for stock in stocks[4001 + 1:]:
        symbol=stock["symbol"]
        print("Getting yahoo data for "+symbol)
        try:
            enrichWithYahoo(symbol)
        except Exception as e:
            print(e,"continuing...")
        print("Recorded yahoo data for "+symbol)