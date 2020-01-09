import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    net_worth = 0
    """Show portfolio of stocks"""
    symbols = db.execute("SELECT symbol, shares, total FROM portfolio WHERE id=:id", id=session['user_id'])
    for s in symbols:
        symbol = s["symbol"]
        shares = s["shares"]
        stock = lookup(symbol)
        total = shares * stock["price"]
        net_worth += total
        db.execute("UPDATE portfolio SET price=:price, total=:total WHERE id=:id AND symbol=:symbol",price=usd(stock["price"]),total=usd(total), id=session["user_id"], symbol=symbol)

    cash = db.execute("SELECT cash FROM users WHERE id=:id", id=session['user_id'])
    net_worth += cash[0]['cash']
    portfolio = db.execute("SELECT * from portfolio WHERE id=:id", id=session["user_id"])

    return render_template("index.html", stocks=portfolio,cash=usd(cash[0]['cash']), total= usd(net_worth) )



@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")

    else:
        cash = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
        stock = lookup(request.form.get("symbol"))
        shares = int(request.form.get("shares"))

        if cash[0]['cash'] < stock["price"] * shares:
            return apology("youre too broke, my dude")

        db.execute("INSERT INTO history (symbol, shares, price, id) VALUES(:symbol, :shares, :price, :id)",symbol=stock["symbol"], shares=shares,price=usd(stock["price"]), id=session["user_id"])

        db.execute("UPDATE users SET cash = cash - :spent_cash WHERE id = :id", id=session["user_id"], spent_cash=stock["price"] * float(shares))

                # Select user shares of that symbol
        user_shares = db.execute("SELECT shares FROM portfolio WHERE id = :id AND symbol=:symbol",id=session["user_id"], symbol=stock["symbol"])

        # if user doesn't has shares of that symbol, create new stock object
        if not user_shares:
            db.execute("INSERT INTO portfolio (name, shares, price, total, symbol, id) VALUES(:name, :shares, :price, :total, :symbol, :id)",name=stock["name"], shares=shares, price=usd(stock["price"]),total=usd(shares * stock["price"]),symbol=stock["symbol"], id=session["user_id"])
        else:
            shares_total = user_shares[0]["shares"] + shares
            db.execute("UPDATE portfolio SET shares=:shares WHERE id=:id AND symbol=:symbol",shares=shares_total, id=session["user_id"],symbol=stock["symbol"])

        #db.execute("INSERT INTO portfolio (name, shares, price, total, symbol, id) VALUES(:name, :shares, :price, :total, :symbol, :id)",name=stock["name"], shares=shares, price=usd(stock["price"]),total=usd(shares * stock["price"]),symbol=stock["symbol"], id=session["user_id"])

        return redirect("/")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    return jsonify("TODO")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    history = db.execute("SELECT * from history WHERE id=:id", id=session["user_id"])

    return render_template("history.html", history=history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        rows = lookup(request.form.get("symbol"))

        if not rows:
            return apology("no info available")

        return render_template("quote.html", stock=rows)

    else:
        return render_template("quotes.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        if not request.form.get("username") or not request.form.get("password"):
            return apology("fill out all fields")

        elif request.form.get("password") != request.form.get("confirm_password"):
            return apology("passwords did not match")

        new_user = db.execute("INSERT INTO users (username, hash) \
                             VALUES(:username, :pass_hash)",
                             username=request.form.get("username"),
                             pass_hash = generate_password_hash(request.form.get("password"), method='plain'))

        if not new_user:
            return apology("Username already exist")

        # remember which user has logged in
        session["user_id"] = new_user

        # redirect user to home page
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        return render_template("sell.html")
    else:
        stock = lookup(request.form.get('symbol'))
        shares = int(request.form.get('shares'))
        available_shares = db.execute("SELECT shares from portfolio WHERE id =:id AND symbol=:symbol", id=session['user_id'], symbol=stock['symbol'])
        if not available_shares or int(available_shares[0]['shares']) < shares:
            return apology("you dont have that many")

        db.execute("INSERT INTO history (symbol, shares, price, id) VALUES(:symbol, :shares, :price, :id)",symbol=stock["symbol"], shares=-shares,price=usd(stock["price"]), id=session["user_id"])

        db.execute("UPDATE users SET cash = cash + :purchase WHERE id = :id",id=session["user_id"],purchase=stock["price"] * float(shares))

        total = int(available_shares[0]['shares']) - shares
        if total == 0:
            db.execute("DELETE FROM portfolio \
                        WHERE id=:id AND symbol=:symbol", id=session["user_id"], symbol=stock["symbol"])
        else:
            db.execute("UPDATE portfolio SET total=:total WHERE id=:id AND symbol=:symbol",total=total, id=session["user_id"],symbol=stock["symbol"])
    return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
