import alpaca_trade_api as tradeapi
from operator import itemgetter
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
    i = 0
    for a in active_stocks:
        i+=1
        if i < 25:
            symbol = a.symbol
            averages = []
            times = []
            o = []
            h = []
            l = []
            c = []
            v = []
            barset = api.get_barset(symbol, enoch, limit=limit)
            bars = barset[symbol]
            try:
                for i in range(limit):
                    a = str((bars[i].o + bars[i].c)/2)
                    averages.append(a)
                    t = bars[i].t
                    times.append(t)
                    o.append(bars[i].o)
                    h.append(bars[i].h)
                    l.append(bars[i].l)
                    c.append(bars[i].c)
                    v.append(bars[i].v)
                    data_dict = {"symbol": symbol, "time": times, "price": averages, "open": o, "high": h, "low": l, "close": c, "volume": v}
                dataset.append(data_dict)
            except:
                print(f'not enough data for {symbol}')
        else:
            print('done')
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


data = GetAllPrices('day', 1)
method1 = sorted(data, cmp=lambda x,y: - cmp(x['close'],y['volume']))
method2 = sorted(data, key=itemgetter('close', 'volume')) 
print(f'{method1}\n\n')
print(method2)
#price_symbol = ''
#volume_symbol = ''
#highest_price = 0
#highest_volume = 0
#for data_point in data:
#    for value in data_point['close']:
#        if value > highest_price:
#            highest_price = value
#            price_symbol = data_point['symbol']
#    for value in data_point['volume']:
#        if value > highest_volume:
#            highest_volume = value
#            volume_symbol = data_point['symbol']
#print(f'{price_symbol} at {highest_price}\n')
#print(f'{volume_symbol} at {highest_volume}\n')