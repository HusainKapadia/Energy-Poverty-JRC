from flask import Flask, request, json #import main Flask class and request object
from forex_python.converter import CurrencyRates
from flask_cors import CORS
from datetime import timedelta
from datetime import datetime
import numpy as np
import pandas as pd


def read_data(household=1, typehh=0):
    if not typehh:
        data = pd.read_csv('useful_no_solar/run_household_{}/power2016Household.csv'.format(household), usecols=1)
        base = datetime(2016, 1, 1)
        dt = [base + timedelta(minutes=x) for x in range(len(data))]
        return dt[-10:]

        # total = total.to_frame()
        # total['date'] = dt
        
app = Flask(__name__) #create the Flask app
CORS(app)

@app.route('/consumer_history')
def hhexample():
    return json.dumps(read_data())

@app.route('/newsubmit', methods = ['POST'])
def api_message():
    if request.headers['Content-Type'] == 'application/json':
        return json.dumps(['testing'])
    else:
        return "415 Unsupported Media Type ;)"
        
if __name__ == '__main_':
    app.run(debug=True, port=5000) #run app in debug mode on port 5000