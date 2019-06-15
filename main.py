from flask import Flask, request, json #import main Flask class and request object
from forex_python.converter import CurrencyRates
from flask_cors import CORS
from datetime import datetime
import numpy as np


app = Flask(__name__) #create the Flask app
CORS(app)

@app.route('/submissions')
def jsonexample():
    return json.dumps([])


@app.route('/newsubmit', methods = ['POST'])
def api_message():
    if request.headers['Content-Type'] == 'application/json':
        return json.dumps(['testing'])
    else:
        return "415 Unsupported Media Type ;)"
        
if __name__ == '__main_':
    app.run(debug=True, port=5000) #run app in debug mode on port 5000