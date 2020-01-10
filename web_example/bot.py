import alpaca_trade_api as tradeapi
import time

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
