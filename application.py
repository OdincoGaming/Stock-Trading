from flask import Flask, render_template, request
from flask_cors import CORS
from . import bot

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
acc_key = ''

@app.route("/")
@cross_origin()
def index():
    return render_template("index.html")

#will send acc_key into bot through here
@app.route("/login", methods=["POST"])
@cross_origin()
def login():
    acc_key = request.form.get("acc_key")
    return render_template("app.html", acc_key=acc_key)

@app.route("/account_info", methods=["POST"])
@cross_origin()
def account_info():
    portfolio, net_worth, stock_worth = bot.AccountInfo()
    return render_template("account.html", portfolio=portfolio, net_worth=net_worth, stock_worth=stock_worth)

@app.route("/test", methods=["GET", "POST"])
@cross_origin()
def test():
    return render_template("test.html")