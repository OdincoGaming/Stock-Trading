import alpaca_trade_api as tradeapi
from alphavantage import TimeSeries

av_key = 'RSNI4SWZTXYEPLWK'
ts = TimeSeries(av_key)
#TODO generate key and secret dynamically from web app using user login
API_KEY = "PKUXRZ6GHDZE9VXGYO2F"
API_SECRET = "cKRe5EdTOt7pGZMJaFAeuLdFeTBTESb3JYuzkCYL"
#paper-api is practice trading, live-api is real trading, also generate dynamically
APCA_API_BASE_URL = "https://paper-api.alpaca.markets"
api = tradeapi.REST(API_KEY, API_SECRET, APCA_API_BASE_URL, 'v2')

aapl, meta = ts.get_daily(symbol='AAPL')
print(aapl['2019-09-12'])