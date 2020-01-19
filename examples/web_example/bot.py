import alpaca_trade_api as tradeapi
import time
import csv
import os

def GetMarketHours():
    is_market_open = api.get_clock()
    return is_market_open

def BrowseExchange(exchange):
    #if exchange = NASDAQ it will only return stocks available for trade through NASDAQ
    stocks_in_exchange = [a for a in active_assets if a.exchange == exchange]
    return stocks_in_exchange

def AccountInfo():
    portfolio = api.list_positions()
    net_worth = account.portfolio_value
    stock_worth = net_worth - account.cash
    return portfolio, net_worth, stock_worth

#algos only return 0 cuz python dont like empty methods lol
def Algo_1(symbol_list):
    #broad
    #buy many, sell all at once an hour or so later
    return 0

def Algo_2(symbol_list):
    #broad
    #watch many stocks for perfect moment to buy
    #sell when reached profit margin, percentage change from purchase price
    return 0

def Algo_3(symbol):
    #focused
    #select a stock to watch, purchase when under margin, sell when over
    return 0

def Algo_4(symbol, days_to_hold):
    #focused
    #hold strategy, buy when cheap. sell after set period of time
    return 0

#api call to submit a purchase order
def BuyAtMarket(symbol, qty, tif,):
    api.submit_order(
    symbol=symbol,
    qty=qty,
    side='buy',
    type='market',
    time_in_force=tif
)

def BuyAtLimit(symbol, qty, tif, limit_price):
    api.submit_order(
    symbol=symbol,
    qty=qty,
    side='buy',
    type='limit',
    limit_price=limit_price,
    time_in_force=tif
)

def BuyAtStopLimit(symbol, qty, tif, limit_price, stop_price):
    api.submit_order(
    symbol=symbol,
    qty=qty,
    side='buy',
    type='stop_limit',
    limit_price=limit_price,
    stop_price=stop_price,
    time_in_force=tif
)

#api call to submit a sell order
def SellAtMarket(symbol, qty, tif):
    api.submit_order(
    symbol=symbol,
    qty=qty,
    side='sell',
    type='market',
    time_in_force=tif,
)

def SellAtLimit(symbol, qty, tif, limit_price):
    api.submit_order(
    symbol=symbol,
    qty=qty,
    side='sell',
    type='limit',
    limit_price=limit_price,
    time_in_force=tif
)

def SellAtStopLimit(symbol, qty, tif, limit_price, stop_price):
    api.submit_order(
    symbol=symbol,
    qty=qty,
    side='sell',
    type='stop_limit',
    limit_price=limit_price,
    stop_price=stop_price,
    time_in_force=tif
)

#will be replacing this with a seperate API as alpacas data is kind of ehh
def GetData(symbol, enoch, limit):
    #a list with a list which is a lists of lists (I assume you can send in multiple symbols at once to get a list of lists that are lists of lists)
    #to get data on multiple symbols in one call send symbols as string seperated by , "AAPL, NFLX"
    #enoch is time period, day minute month year
    #limit is how many enochs, so enoch='minute', limit=1 would give the most recent data
    barset = api.get_barset(symbol, enoch, limit=limit)

    #top level list in barset
    bars = barset[symbol]

    filename = symbol + '.csv'
    path = os.getcwd() + "\\data\\csv\\" + filename

    try:
        with open(path, 'w+', newline='') as file:
            i = 0
            fieldnames = ['date', '1. open', '2. high', '3. low', '4. close', '5. volume']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            while i < limit:
                t = bars[i].t
                o = bars[i].o
                h = bars[i].h
                l = bars[i].l
                c = bars[i].c
                v = bars[i].v
                writer.writerow({'date':t,'1. open':o,'2. high':h,'3. low':l,'4. close':c,'5. volume':v})
                i += 1
    except:
        print("not enough data for " + symbol)

def Main(is_open):
    #continue to trade until market is closed
    while is_open:
        is_open = GetMarketHours()
        #depending on the algo will use sleep to prevent too many api calls, 75 calls every 30 seconds is what I used for the ML version
        time.sleep(10)
        print("working")
        #just cuz this script dont do shit yet and theres no point in continuing the loop lol
        break

#TODO generate dynamically from web app
API_KEY = "PKUXRZ6GHDZE9VXGYO2F"
API_SECRET = "cKRe5EdTOt7pGZMJaFAeuLdFeTBTESb3JYuzkCYL"
#paper-api is practice trading, live-api is real trading
APCA_API_BASE_URL = "https://paper-api.alpaca.markets"

api = tradeapi.REST(API_KEY, API_SECRET, APCA_API_BASE_URL, 'v2')
account = api.get_account()
active_stocks = api.list_assets(status='active')

is_open = GetMarketHours()
if is_open:
    Main(is_open)
