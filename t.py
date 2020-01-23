import alpaca_trade_api as tradeapi
import requests


#TODO generate key and secret dynamically from web app using user login
API_KEY = "PKUXRZ6GHDZE9VXGYO2F"
API_SECRET = "cKRe5EdTOt7pGZMJaFAeuLdFeTBTESb3JYuzkCYL"
#paper-api is practice trading, live-api is real trading, also generate dynamically
APCA_API_BASE_URL = "https://paper-api.alpaca.markets"
api = tradeapi.REST(API_KEY, API_SECRET, APCA_API_BASE_URL, 'v2')

def GetAveragePrice(symbol, enoch, limit):
    data = []
    averages = []
    times = []
    barset = api.get_barset(symbol, enoch, limit=limit)
    bars = barset[symbol]
    for i in range(limit):
        a = str((bars[i].o + bars[i].c)/2)
        averages.append(a)
        t = bars[i].t
        times.append(t)
    data_dict = {"time": times, "price": averages}
    data.append(data_dict)
    return data

def GetAllPrices(enoch, limit):
    active_stocks = api.list_assets(status='active')
    dataset = []
    for a in active_stocks:
        symbol = a.symbol
        averages = []
        times = []
        barset = api.get_barset(symbol, enoch, limit=limit)
        bars = barset[symbol]
        try:
            for i in range(limit):
                a = str((bars[i].o + bars[i].c)/2)
                averages.append(a)
                t = bars[i].t
                times.append(t)
                data_dict = {"symbol": symbol, "time": times, "price": averages}
            dataset.append(data_dict)
        except:
            print(f'not enough data for {symbol}')
    return dataset

def GetListOfStocks():
    stock_list = api.list_assets(status='active')
    stocks = []
    for a in stock_list:
        stocks.append(a.symbol)
    return stocks

def get_symbol(symbol):
    url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en".format(symbol)

    result = requests.get(url).json()
    for x in result['ResultSet']['Result']:
        if x['symbol'] == symbol:
            symbol_name = {'name': x['name'], 'symbol': x['symbol']}
            return symbol_name

active_stocks = api.list_assets(status='active')
data = get_symbol('AAPL')
print(data)