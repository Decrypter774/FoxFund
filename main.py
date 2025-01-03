import json
import os
from AVClient import AVClient
from DBRepo import StockDatabase
import google.generativeai as genai
from FMPClient import FMPClient

#  Replace with your actual API key
genai.configure(api_key=os.environ.get("API_KEY_GEMINI"))
#
# # Setup Model (choose a model, e.g., gemini-pro)
model = genai.GenerativeModel('gemini-2.0-flash-exp')


# Function to Interact with Gemini
def process_with_gemini(system_prompt, user_prompt):
    """Sends a prompt to Gemini and returns the response."""

    chat = model.start_chat(
        history=[],
    )

    # send system prompt first
    chat.send_message(system_prompt)

    # then user prompt
    response = chat.send_message(user_prompt)

    return response.text

def download_data(industry):
    DATABASE = {
        'dbname': 'postgres',
        'user': 'postgres',
        'password': 'postgres',
        'host': 'localhost',
        'port': 5432
    }
    stock_db = StockDatabase(DATABASE)
    stock_list_client = FMPClient(os.environ.get("API_KEY_FMP"))
    stock_data = stock_list_client.get_stock_list(industry, 200000000, 3000000000)
    #
    print("Downloaded", len(stock_data), "records from FMP")
    for item in (stock_data):
        try:
            stock_db.delete_stock(item["symbol"])
            stock_db.create_stock({
                'symbol': item["symbol"],
                'company_name': item["companyName"],
                'market_cap': item["marketCap"],
                'sector': item["sector"],
                'industry': item["industry"],
                'beta': round(item["beta"], 4),
                'price': round(item["price"], 2),
                'last_annual_dividend': item["lastAnnualDividend"],
                'volume': item["volume"],
                'exchange': item["exchange"],
                'exchange_short_name': item["exchangeShortName"],
                'country': item["country"],
                'is_etf': item["isEtf"],
                'is_fund': item["isFund"],
                'is_actively_trading': item["isActivelyTrading"],
                'pe_ratio': 0,
                'industry_pe_ratio': 0
            })
        except Exception as e:
            print("exception:", e)
            print(item)
            continue

if __name__ == "__main__":
    with open("industries.json", 'r') as f:
        data_array = json.load(f)
    for industry in data_array:
        download_data(industry)


    # print(stock_db.list_all_stocks())