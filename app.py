from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

#just add @cross_origin() decorator beneath any route and-
#above any definition that requires it

@app.route('/')
@cross_origin()
def index():
    return render_template('index.html')

@app.route("/test")
@cross_origin()
def test():
    return render_template("test.html")

if __name__ == '__main__':
    app.debug = True
    app.run()