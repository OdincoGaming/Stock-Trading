from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
import alpaca_trade_api as tradeapi
from alpha_vantage.timeseries import TimeSeries

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

av_key = 'RSNI4SWZTXYEPLWK'
ts = TimeSeries(av_key)
#TODO generate key and secret dynamically from web app using user login
API_KEY = "PKUXRZ6GHDZE9VXGYO2F"
API_SECRET = "cKRe5EdTOt7pGZMJaFAeuLdFeTBTESb3JYuzkCYL"
#paper-api is practice trading, live-api is real trading, also generate dynamically
APCA_API_BASE_URL = "https://paper-api.alpaca.markets"
api = tradeapi.REST(API_KEY, API_SECRET, APCA_API_BASE_URL, 'v2')

@app.route('/')
@cross_origin()
def index():
    return render_template('index.html')

@app.route("/test")
@cross_origin()
def test():
    test_string = 'this is not a test of the emergency broadcast system'
    return test_string

if __name__ == '__main__':
    app.debug = True
    app.run()
    aapl, meta = ts.get_daily(symbol='AAPL')
    print(aapl)
    print('\n\n')
    print(meta)