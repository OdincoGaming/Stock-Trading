from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import alpaca_trade_api as tradeapi
import json

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

#TODO generate key and secret dynamically from web app using user login
API_KEY = "PKUXRZ6GHDZE9VXGYO2F"
API_SECRET = "cKRe5EdTOt7pGZMJaFAeuLdFeTBTESb3JYuzkCYL"
#paper-api is practice trading, live-api is real trading, also generate dynamically
APCA_API_BASE_URL = "https://paper-api.alpaca.markets"
api = tradeapi.REST(API_KEY, API_SECRET, APCA_API_BASE_URL, 'v2')

def GetAveragePrice(symbol, enoch, limit):
    #data = []
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
    #data.append(data_dict)
    return data_dict

def GetListOfStocks():
    stocks = api.list_assets(status='active')
    stock_list = []
    for s in stocks:
        stock_list.append(s.symbol)
    return stock_list

####
#### PYTHON
###########
#### WEB
####

@app.route('/')
@cross_origin()
def index():
    return render_template('index.html')

@app.route("/test")
@cross_origin()
def test():
    test_string = 'this is not a test of the emergency broadcast system'
    return test_string

@app.route('/stock_data')
@cross_origin()
def stock_data():
    symbol = 'AAPL'
    enoch = 'minute'
    limit = 10
    data = GetAveragePrice(symbol, enoch, limit=limit)
    return jsonify(data)

@app.route('/stock_list')
@cross_origin()
def stock_list():
    stock_list = GetListOfStocks()
    return jsonify(stock_list)

@app.route('/stock/<string:company>/<string:time_scale>/<int:limit>', methods=['GET'])
@cross_origin()
def get_stock_data(company, time_scale, limit):
    data = GetAveragePrice(company, time_scale, limit)
    return jsonify(data)

if __name__ == '__main__':
    app.debug = True
    app.run()