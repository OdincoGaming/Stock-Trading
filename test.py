import alpaca_trade_api as tradeapi


#TODO generate key and secret dynamically from web app using user login
API_KEY = "PKUXRZ6GHDZE9VXGYO2F"
API_SECRET = "cKRe5EdTOt7pGZMJaFAeuLdFeTBTESb3JYuzkCYL"
#paper-api is practice trading, live-api is real trading, also generate dynamically
APCA_API_BASE_URL = "https://paper-api.alpaca.markets"
api = tradeapi.REST(API_KEY, API_SECRET, APCA_API_BASE_URL, 'v2')


def GetAveragePrice(symbol, enoch, limit):
    data = []
    barset = api.get_barset(symbol, enoch, limit=limit)
    bars = barset[symbol]
    for i in range(limit):
        a = str((bars[i].o + bars[i].c)/2)
        t = bars[i].t
        data.append(f"{a}, {t}")
    return data

symbol = 'AAPL'
enoch = 'minute'
limit = 10
data = GetAveragePrice(symbol, enoch, limit=limit)
print (data)