from flask import Flask, render_template, request
from . import bot

app = Flask(__name__)
acc_key = ''

@app.route("/")
def index():
    return render_template("index.html")

#will send acc_key into bot through here
@app.route("/login", methods=["POST"])
def login():
    acc_key = request.form.get("acc_key")
    return render_template("app.html", acc_key=acc_key)

@app.route("/account_info", methods=["POST"])
def account_info():
    portfolio, net_worth, stock_worth = bot.AccountInfo()
    return render_template("account.html", portfolio=portfolio, net_worth=net_worth, stock_worth=stock_worth)

@app.route("/test", methods=["GET", "POST"])
def test():
    return render_template("test.html")